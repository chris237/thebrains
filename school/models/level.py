# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import UserError

class LevelOfStudy(models.Model):
    _name = "brains.level"
    _description = "Level of Study"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    name = fields.Char(string="Name", required=True, tracking=True)
    code = fields.Char(string="Code", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="State", default="draft", tracking=True)

    cursus_id = fields.Many2one(
        "brains.cursus", 
        string="Cursus", 
        required=True, 
        tracking=True
    )

    years_level = fields.Selection(
        selection=[
            ('1', 'I'),
            ('2', 'II'),
            ('3', 'III'),
            ('4', 'IV'),
            ('5', 'V'),
        ],
        string="Year Level",
        required=True,
        tracking=True
    )

    semester_ids = fields.One2many(
        "brains.semestre", 
        "level_id", 
        string="Semesters", 
        tracking=True
    )

    # 🔗 Nouveau : relation Many2many avec les années académiques
    year_ids = fields.Many2many(
        "brains.school.year",
        "level_year_rel",
        "level_id",
        "year_id",
        string="Academic Years",
        tracking=True,
        help="Années académiques dans lesquelles ce niveau est actif"
    )

    # desactiver un ou plusieurs levels
    def desactivate(self):
        for level in self:
            if level.state == 'active':
                level.state = 'inactive'
                level.semester_ids.write({'state': 'inactive'})
            else:
                raise UserError("Only active levels can be set to inactive.")