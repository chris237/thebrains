from odoo import fields, models


class Faculty(models.Model):
    _name = "school.faculty"
    _description = "Faculty"

    name = fields.Char(required=True, translate=False)
    reference = fields.Char(required=True, translate=False)
    campus_ids = fields.Many2many(
        comodel_name="school.campus",
        relation="school_faculty_campus_rel",
        column1="faculty_id",
        column2="campus_id",
        string="Campuses",
        help="Select all campuses where this faculty is established.",
    )
    dean_id = fields.Many2one(
        comodel_name="res.partner",
        string="Dean",
        help="Assign the faculty dean if already defined.",
    )

    _sql_constraints = [
        ("reference_unique", "unique(reference)", "The faculty reference must be unique."),
    ]
