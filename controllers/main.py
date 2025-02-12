from odoo import http

class AppraisalController(http.Controller):
    # @http.route('/appraisal/summary', type='http', auth="user")
    # def summary(self, **kwargs):
    #     appraisals = http.request.env['hr.appraisal'].search([])
    #     return http.request.render('appraisal.summary_template', {
    #         'appraisals': appraisals
    #     })
    @http.route('/appraisal/notify_manager', type='http', auth="user")
    def notify_manager(self, **kwargs):
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        appraisal_url = f"{base_url}/appraisal/summary"
        
        # Construct the email content
        email_body = f"Dear Manager,\n\nPlease review the appraisals at the following link: {appraisal_url}\n\nBest regards,\nYour Company"
        
        # Send the email (assuming you have a method to send emails)
        self.send_email_to_manager(email_body)
