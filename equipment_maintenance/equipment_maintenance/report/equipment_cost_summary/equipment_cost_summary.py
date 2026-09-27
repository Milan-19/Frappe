# Copyright (c) 2026, dev and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [
        {
            "label": "Equipment",
            "fieldname": "equipment",
            "fieldtype": "Link",
            "options": "Equipment",
            "width": 180,
        },
        {
            "label": "Total Maintenance Log Count",
            "fieldname": "log_count",
            "fieldtype": "Int",
            "width": 150,
        },
    ], frappe.db.sql(
        """
		SELECT equipment, COUNT(name) as log_count
		FROM `tabEquipment Maintenance Log`
		GROUP BY equipment
		""",
        as_dict=True,
    )
    return columns, data


def execute_snapshot_report(filters: dict | None = None):
    """Return columns and data for the report.

    This is the main entry point for snapshot report. When 'Synced
    Report' is enabled in report, framework will call this method
    every time the report is refreshed or a filter is updated. It
    accepts the same filters as normal execute. But a utility method -
    get_latest_sync, is also imported.

    """
    from frappe.database.duckdb.database import get_latest_sync

    columns, data = [], []
    return columns, data
