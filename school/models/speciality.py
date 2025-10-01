# -*- coding: utf-8 -*-
from odoo import models, fields

class Speciality(models.Model):
    _name = "brains.speciality"
    _description ="Speciality"
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
    )

    cursus_ids = fields.One2many("brains.cursus", "speciality_id", string="Cursus")

