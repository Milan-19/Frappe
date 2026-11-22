# Copyright (c) 2026, dev and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EquipmentMaintenanceLog(Document):
    # The validate method runs automatically before saving a document
    def validate(self):
        if self.completion_date and self.completion_date < self.request_date:
            frappe.throw("Completion Date cannot be earlier than Request Date.")


# Expose custom methods to client-side scripts or external REST endpoints
@frappe.whitelist()
def get_open_logs_count(equipment_id):
    # Query database using Frappe's built-in ORM helpers
    count = frappe.db.count(
        "Equipment Maintenance Log",
        filters={"equipment": equipment_id, "docstatus": 0},  # 0 = Draft status
    )
    return count
