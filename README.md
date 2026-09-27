# 🛠️ Equipment Maintenance Tracker (`equipment_maintenance`)

> A custom, full-stack enterprise extension built on the **Frappe Framework**. Designed to demonstrate end-to-end domain modeling, server-side ORM logic, client-side event scripting, business workflows, and reporting in Frappe—with direct architectural parallels to **Odoo**.

---

## 🔁 Odoo to Frappe Conceptual Mapping

For technical reviewers evaluating full-stack ERP framework fluency, here is how the core architecture of this app maps from Odoo to Frappe:

| Odoo Concept | Frappe Implementation | Implementation in this App |
| :--- | :--- | :--- |
| `models.Model` | **DocType** | `Equipment`, `Equipment Maintenance Log` |
| `fields.One2many` / Line Items | **Child DocType / Table Field** | `Maintenance Task Item` embedded in parent log |
| `fields.Many2one` | **Link Field** | `equipment` field linking Log to Equipment master |
| `@api.constrains` | **`validate()` Controller Method** | Server-side validation preventing invalid completion dates |
| `@api.model` / RPC Endpoints | **`@frappe.whitelist()` API** | `get_open_logs_count()` endpoint exposed to AJAX/REST |
| `self.env['model'].search()` | **`frappe.db.get_list()` / ORM** | Python ORM queries inside Python controllers |
| OWL Component Patch / Form JS | **`frappe.ui.form.on()` Scripting** | Client-side button insertion & async RPC handling |
| `ir.cron` Scheduled Actions | **`hooks.py` Scheduler Events** | Daily background checks for overdue maintenance |
| `ir.model.access.csv` & Rules | **DocPerm / Role-Based Access** | Granular permissions for Technicians vs Managers |

---

## 🚀 Key Features & Technical Highlights

### 1. Data Modeling & Relationships (DocTypes)
- **`Equipment`** *(Master DocType)*: Tracks physical assets, serial numbers, and operational status.
- **`Equipment Maintenance Log`** *(Main Transaction)*: Captures repair requests linked to an equipment asset via a **Link Field**.
- **`Maintenance Task Item`** *(Child DocType)*: Line-item table tracking specific repair tasks, costs, and status.

### 2. Server-Side Logic & ORM (`Python`)
- Implemented **`validate()`** hooks on `Equipment Maintenance Log` to enforce business constraints prior to database commits.
- Created whitelisted endpoints using **`@frappe.whitelist()`** for client-side API interaction.
- Utilized Frappe's native ORM helpers (`frappe.get_doc`, `frappe.db.count`, `frappe.db.sql`).

```python
# equipment_maintenance/doctype/equipment_maintenance_log/equipment_maintenance_log.py
import frappe
from frappe.model.document import Document

class EquipmentMaintenanceLog(Document):
    def validate(self):
        """Server-side constraint check prior to save."""
        if self.completion_date and self.completion_date < self.request_date:
            frappe.throw("Completion Date cannot be earlier than Request Date.")

@frappe.whitelist()
def get_open_logs_count(equipment_id):
    """Exposed RPC method for client-side call."""
    return frappe.db.count("Equipment Maintenance Log", filters={
        "equipment": equipment_id,
        "docstatus": 0
    })
```

### 3. Client-Side Scripting (`JavaScript`)
- Extended Form behavior using `frappe.ui.form.on()` handlers.
- Injected custom action buttons dynamically and handled asynchronous server response handling via `frappe.call()`.

```javascript
// equipment_maintenance/doctype/equipment_maintenance_log/equipment_maintenance_log.js
frappe.ui.form.on('Equipment Maintenance Log', {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Check Open Requests'), function() {
                frappe.call({
                    method: 'equipment_maintenance.equipment_maintenance.doctype.equipment_maintenance_log.equipment_maintenance_log.get_open_logs_count',
                    args: { equipment_id: frm.doc.equipment },
                    callback: function(r) {
                        if (r.message !== undefined) {
                            frappe.msgprint(`This equipment has ${r.message} pending draft maintenance log(s).`);
                        }
                    }
                });
            });
        }
    }
});
```

### 4. Workflow & Business Process Management
- Configured a multi-step **Workflow** (`Draft` → `Pending Approval` → `Approved`).
- Restricted approval state transitions using role-based permissions (`Maintenance Manager`).

### 5. Custom Script Report
- Developed a **Script Report** (`Equipment Cost Summary`) executing SQL aggregations to display total maintenance logs and expenditure per equipment unit.

---

## 💻 Installation & Local Development

### Prerequisites
- Frappe Bench environment running **Frappe v15+**
- Developer mode enabled (`bench set-config --global developer_mode 1`)

### Setup Instructions

```bash
# 1. Get the app repository into your bench
bench get-app https://github.com/your-username/equipment_maintenance.git

# 2. Install the app on your site
bench --site your-site.test install-app equipment_maintenance

# 3. Migrate database and clear cache
bench --site your-site.test migrate
bench clear-cache
```

---

## 📄 License
MIT
