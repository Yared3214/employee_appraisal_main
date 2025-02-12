# 🌟 Employee Appraisal Module for Odoo

### 📌 Overview

The Employee Appraisal Module is a custom Odoo module designed to streamline employee performance evaluations. It provides a structured workflow where HR managers can create and track appraisals while ensuring role-based access and automation.

---

### ✨ Features

✅ Appraisal Management – HR can create and assign appraisals.

✅ Role-Based Workflow – Clear process from initiation to completion.

✅ Automated Notifications & Activities – Keeps everyone updated.

✅ Access Control – Ensures users see only what’s relevant to them.

### 🔹 Workflow:

1️⃣ HR initiates appraisals.

2️⃣ Managers review and evaluate appraisals.

3️⃣ CEO confirm final evaluations.

4️⃣ Employees receive their final appraisal results.

---


## 🚀 Installation

### 🔹 Prerequisites
- Ensure you have Odoo installed.

- Developer Mode should be enabled.

### 🔹 Steps
1️⃣ Clone or download the module into your Odoo custom addons directory:

```sh
git clone https://github.com/your-repo/employee_appraisal.git
```
2️⃣ Restart your Odoo server:

```sh
odoo-bin -c odoo.conf -u employee_appraisal
```
3️⃣ Navigate to Apps → Update Apps List.

4️⃣ Search for Employee Appraisal and click Install.

---

## 🎯 Usage Guide

### 📌 Creating an Appraisal
- HR can create a new appraisal under Appraisals → Create.
  
- Assign a manager and define evaluation criteria.
  
### 📌 Appraisal Workflow
🔹 Managers evaluate employees and send appraisals to deputies.

🔹 Deputies (CEO) confirm the appraisal.

🔹 Employees receive the final approved appraisal.

---

## 🔐 Security & Permissions

| Role             | Access Rights                        |
|------------------|--------------------------------------|
| **HR**           | Full access to all appraisals        |
| **Managers**     | View only assigned appraisals        |
| **CEO**          | Confirm final evaluations            |
| **Employees**    | View appraisals after final approval |

---

## ⚙️ Technical Details
### 🔸 Models Used:
- hr.appraisal – Stores appraisal records.
  
- hr.employee – Links employees to their managers.
  
- mail.activity – Handles automated notifications.
  
### 🔸 Workflow States:

```css
Draft → Sent to Manager → Sent to Deputy → Completed
```
### 🔸 Automated Actions:
✅ Activities are created when appraisals move between states.

✅ Notifications are sent to responsible users.

---

## 🎨 Customization

This module is fully customizable to fit your organization's needs:

- Modify evaluation criteria.
  
- Adjust user roles and permissions.
  
- Create custom email templates for notifications.

  ---
  
## 📜 License
Released under the MIT License – feel free to modify and use it as needed.

## 👤 Author
Developed by Yared Bitewlign

📧 Contact: yaredbitewlign@gmail.com

💡 Contributions are welcome! Feel free to submit pull requests or open issues.
