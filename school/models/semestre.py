# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class Semestre(models.Model):
    _name = "brains.semestre"
    _description = "Semestre"
    _rec_name = "name_display"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    name = fields.Char(string="Name", required=True, tracking=True)
    code = fields.Char(string="Code", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    name_display = fields.Char(string="Name Display", compute="_compute_name_display", store=True)

    @api.depends('name', 'level_id', 'cursus_id', 'speciality_id')
    def _compute_name_display(self):
        for record in self:
            if record.level_id and record.name and record.cursus_id and record.speciality_id:
                record.name_display = f"{record.level_id.name} - {record.cursus_id.name} - {record.speciality_id.name}"
            else:
                record.name_display = record.name or ''

    level_id = fields.Many2one(
        "brains.level", 
        string="Level", 
        required=True, 
        tracking=True
    )

    cursus_id = fields.Many2one(
        "brains.cursus", 
        string="Cursus", 
        related="level_id.cursus_id", 
        store=True, 
        readonly=True, 
        tracking=True
    )
    speciality_id = fields.Many2one(
        'brains.speciality',
        related="cursus_id.speciality_id",
        string="Speciality",
        store=True,
        readonly=True,
        tracking=True
    )
    year_ids = fields.Many2many(
        "brains.school.year",
        "year_semestre_rel",
        "semestre_id",
        "year_id",
        string="Academic Years",
        tracking=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="State", default="draft", tracking=True)

    def write(self, vals):
        res = super().write(vals)
        if "year_ids" in vals:  # si les années changent
            for semestre in self:
                if semestre.year_ids:
                    semestre.level_id.year_ids = [(6, 0, semestre.year_ids.ids)]
                else:
                    semestre.level_id.year_ids = [(5, 0, 0)]
        return res

    # desactiver un ou plusieurs semestres 
    def desactivate(self):
        for semestres in self:
            if semestres.state == 'active':
                semestres.state = 'inactive'
            else:
                raise UserError("Only active semesters can be set to inactive.")