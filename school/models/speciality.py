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

    cursus_ids = fields.One2many("brains.cursus", "speciality_id", string="Cursus")