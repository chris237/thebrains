# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Speciality(models.Model):
    _name = "brains.speciality"
    _description = "Speciality"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    name = fields.Char(string="Name", required=True, tracking=True)
    guardiadhip = fields.Char(string="Guardianship", tracking=True)

    faculty_id = fields.Many2one("brains.faculty", string="Faculty", required=True)

    campus_ids = fields.Many2many(
        "brains.campus",
        "brains_speciality_campus_rel",
        "speciality_id",
        "campus_id",
        string="Campuses",
        required=True,
    )

    cursus_ids = fields.One2many("brains.cursus", "speciality_id", string="Cursus")

    @api.onchange("faculty_id")
    def _onchange_faculty_id(self):
        """Reset the selected campuses when the faculty changes.

        Only campuses linked to the chosen faculty should remain selected to
        avoid inconsistent data when the user changes the faculty.
        """
        if self.faculty_id:
            allowed_campuses = self.faculty_id.campus_ids
            self.campus_ids = self.campus_ids & allowed_campuses
        else:
            self.campus_ids = False

    @api.constrains("campus_ids", "faculty_id")
    def _check_campus_faculty_alignment(self):
        for speciality in self:
            if not speciality.campus_ids:
                raise ValidationError(
                    "Veuillez sélectionner au moins un campus pour la filière."
                )

            invalid_campuses = speciality.campus_ids.filtered(
                lambda campus: speciality.faculty_id not in campus.faculty_ids
            )
            if invalid_campuses:
                raise ValidationError(
                    "Les campus sélectionnés doivent être rattachés à la faculté choisie."
                )

