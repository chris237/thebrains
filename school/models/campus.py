from odoo import fields, models


class Campus(models.Model):
    _name = "school.campus"
    _description = "Campus"

    name = fields.Char(required=True, translate=False)
    code = fields.Char(required=True, translate=False)
    faculty_ids = fields.Many2many(
        comodel_name="school.faculty",
        relation="school_faculty_campus_rel",
        column1="campus_id",
        column2="faculty_id",
        string="Faculties",
    )

    _sql_constraints = [
        ("code_unique", "unique(code)", "The campus code must be unique."),
    ]
