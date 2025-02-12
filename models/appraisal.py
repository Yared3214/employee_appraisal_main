import logging
from datetime import timedelta
from odoo import models, fields, api


class Appraisal(models.Model):
    _name = 'hr.appraisal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Appraisal'

    appraisal_id = fields.Many2one('hr.appraisal', string="Appraisal", ondelete="cascade")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    employee_user_id = fields.Many2one(
        "res.users", 
        string="Employee User",
        compute="_compute_employee_user",
        store=True
    )
    manager_id = fields.Many2one('hr.employee', string='Manager', required=True)
    manager_email = fields.Char(related='manager_id.work_email', string="Manager Email", store=True)
    appraisal_date = fields.Date(string="Appraisal Date", required=True)
    next_appraisal_date = fields.Date(string="Next Appraisal Date", required=True)
    job_position = fields.Many2one('hr.job', string="Job Position", required=True)
    department = fields.Many2one('hr.department', string="Department", required=True)
    hr_main_measurement_ids = fields.One2many('hr.employee.main.measurement', 'appraisal_id', string='Main Measurements')
    manager_main_measurement_ids = fields.One2many('manager.employee.main.measurement', 'appraisal_id', string='Main Measurement')
    send_to_role = fields.Char(
        string="Send To Role",
        compute="_compute_send_to_role",
        store=False  # No need to store, as it's dynamically computed
    )
    deputy_id = fields.Many2one(
    'hr.employee',
    string='Deputy (CEO)',
    compute='_compute_deputy',
    store=True,
    readonly=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent_to_manager', 'Sent to Manager'),
        ('viewed_by_manager', 'Viewed by Manager'),
        ('sent_to_deputy', 'Sent to Deputy'),
        ('completed', 'Completed')
    ], default='draft', string="State", tracking=True)
    state_visibility = fields.Char(
        string="State Visibility",
        compute="_compute_state_visibility",
        store=False
    )
    is_user_hr = fields.Boolean(
        compute="_compute_is_user_hr",
        store=True
    )
    

    @api.depends("employee_id")
    def _compute_employee_user(self):
        for record in self:
            record.employee_user_id = record.employee_id.user_id.id if record.employee_id else False

    def _compute_is_user_hr(self):
        user = self.env.user
        for record in self:
            record.is_user_hr = user.has_group('employee_appraisal_main.group_human_resources')

    @api.depends('employee_id.company_id')
    def _compute_deputy(self):
        for record in self:
            deputy = self.env['hr.employee'].search([('job_id.name', '=', 'CEO')], limit=1)
            record.deputy_id = deputy.id if deputy else False



    def _compute_send_to_role(self):
        for record in self:
            user = self.env.user
            if user.employee_id and user.employee_id.job_id.name == 'CEO':
                record.send_to_role = 'employee'
            elif user.employee_id and user.employee_id.job_id.name == 'HR': 
                record.send_to_role = 'manager'
            elif user.employee_id.job_id.name != 'CEO' and user.employee_id.job_id.name != 'HR': 
                record.send_to_role = 'deputy'
            else: 
                record.send_to_role = ''
        
    def _compute_state_visibility(self):
        for record in self:
            user = self.env.user
            if user.employee_id and user.employee_id.job_id.name == 'CEO':
                record.state_visibility = 'employee'
            elif user.employee_id and user.employee_id.job_id.name == 'HR': 
                record.state_visibility = 'manager'
            elif user.employee_id.job_id.name != 'CEO' and user.employee_id.job_id.name != 'HR': 
                record.state_visibility = 'deputy'
            else: 
                record.state_visibility = ''

    def create_appraisal_activity_to_manager(self):
        if not self.employee_id:
            raise ValueError("Employee not found in context or values.")
        
        if not self.manager_id:
            raise ValueError("The employee does not have an assigned manager.")
        
        if self.employee_id == self.manager_id:
            raise ValueError("You cannot send an appraisal to yourself as a deputy.")
        # Prepare activity values
        activity_vals = {
            'res_model': 'hr.appraisal',
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,  # Example activity type
            'summary': ('Appraisal Form Review'),
            'note': ('Please review the appraisal form for %s.') % self.employee_id.name,
            'user_id': self.manager_id.user_id.id,  # Assign to the manager
            'res_id': self.id,  # Assuming this method is called within the appraisal record
            'res_model_id': self.env['ir.model']._get('hr.appraisal').id,
            'date_deadline': fields.Date.today()  # Example deadline
        }

        # self.env['mail.activity'].with_context(short_name=False).create(activity_vals)
        self.activity_schedule(
            activity_type_id=activity_vals['activity_type_id'],
            summary=activity_vals['summary'],
            note=activity_vals['note'],
            user_id=activity_vals['user_id'],
            date_deadline=activity_vals['date_deadline'],
        )
        self.message_post(body="Appraisal sent to Manager")
        self.state = 'sent_to_manager'
    
    def create_appraisal_activity_to_deputy(self):
        for record in self:
            if not record.deputy_id:
                raise ValueError("No deputy (CEO) is assigned for this appraisal.")
            # Prepare activity values
            activity_vals = {
            'res_model': 'hr.appraisal',
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,  # Example activity type
            'summary': ('Appraisal Form Review'),
            'note': ('Please review the appraisal form for %s.') % self.employee_id.name,
            'user_id': self.deputy_id.user_id.id,  # Assign to the deputy
            'res_id': self.id,  # Assuming this method is called within the appraisal record
            'res_model_id': self.env['ir.model']._get('hr.appraisal').id,
            'date_deadline': fields.Date.today()  # Example deadline
            }

            self.activity_schedule(
            activity_type_id=activity_vals['activity_type_id'],
            summary=activity_vals['summary'],
            note=activity_vals['note'],
            user_id=activity_vals['user_id'],
            date_deadline=activity_vals['date_deadline'],
        )
            self.message_post(body="Appraisal sent to Deputy")
            self.state = 'sent_to_deputy'
    def create_appraisal_activity_to_employee(self):
        for record in self:
            if not record.employee_id.user_id:
                raise ValueError(f"Employee {record.employee_id.name} has no assigned user.")
            # Prepare activity values
            activity_vals = {
            'res_model': 'hr.appraisal',
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,  # Example activity type
            'summary': 'Appraisal Form Review',
            'note': f"Please review the appraisal form for {record.employee_id.name}.",
            'user_id': record.employee_id.user_id.id,  # Assign to the employee
            'res_id': record.id,  # Appraisal record ID
            'res_model_id': self.env['ir.model']._get('hr.appraisal').id,
            'date_deadline': fields.Date.today(),  # Example deadline
            }

            # Schedule the activity for the employee
            record.activity_schedule(
            activity_type_id=activity_vals['activity_type_id'],
            summary=activity_vals['summary'],
            note=activity_vals['note'],
            user_id=activity_vals['user_id'],
            date_deadline=activity_vals['date_deadline'],
            )

            # Post a message in the chatter
            record.message_post(body="Appraisal sent to Employee.")

            # Update the state
            record.state = 'completed'

                
        
class HrEmployeeMainMeasurement(models.Model):
    _name = 'hr.employee.main.measurement'
    _description = 'HR Employee Main Measurement'
    

    appraisal_id = fields.Many2one('hr.appraisal', string='Appraisal', required=True, ondelete='cascade')
    main_name = fields.Char(string='Main Measurement', required=True)
    detail_name = fields.Char(string='Detail Measurement', required=True)
    weight = fields.Integer(string='Weight', required=True)
    point = fields.Float(string='Point', required=True)
             
    # detail_measurement_ids = fields.One2many('employee.detail.measurement', 'main_measurement_id', string='Detail Measurements')


class ManagerEmployeeMainMeasurement(models.Model):
    _name = 'manager.employee.main.measurement'
    _description = 'Manager Employee Main Measurement'
    

    appraisal_id = fields.Many2one('hr.appraisal', string='Appraisal', required=True, ondelete='cascade')
    main_name = fields.Char(string='Main Measurement', required=True)
    detail_name = fields.Char(string='Detail Measurement', required=True)
    weight = fields.Integer(string='Weight', required=True)
    point = fields.Float(string='Point', required=True)


# class EmployeeDetailMeasurement(models.Model):
#     _name = 'employee.detail.measurement'
#     _description = 'Employee Detail Measurement'

#     main_measurement_id = fields.Many2one('employee.main.measurement', string='Main Measurement', required=True, ondelete='cascade')
#     name = fields.Char(string='Detail Measurement', required=True)
#     weight = fields.Integer(string='Weight', required=True)
#     point = fields.Float(string='Point', required=True)
