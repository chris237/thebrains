# -*- coding: utf-8 -*-
from odoo import models, fields

class Cour(models.Model):
    _name = "brains.cours"
    _description = "Course"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    name = fields.Char(string="Name", required=True, tracking=True)
    code = fields.Char(string="Code", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    type_cours = fields.Selection([
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('project', 'Project'),
    ], string="Course Type", required=True, tracking=True)

    credits = fields.Float(string="Credits", required=True, tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)
    responsible_id = fields.Many2one(
        "hr.employee", 
        string="Teacher", 
        tracking=True, 
        ondelete='set null', 
        index=True,
        domain=[('is_teacher', '=', True)]
    )

    level_id = fields.Many2one(
        "brains.level",
        related="semester_id.level_id",
        string="Level",
        store=True,
        readonly=True,
        tracking=True
    )

    cursus_id = fields.Many2one(
        "brains.cursus",
        related="semester_id.level_id.cursus_id",
        string="Cursus",
        store=True,
        readonly=True,
        tracking=True
    )

    specialty_id = fields.Many2one(
        "brains.speciality",
        related="semester_id.level_id.cursus_id.speciality_id",
        string="Speciality",
        store=True,
        readonly=True,
        tracking=True
    )

    semester_id = fields.Many2one(
        "brains.semestre",
        string="Semester",
        required=True,
        tracking=True
    )

    years_id = fields.Many2one(
        "brains.school.year",
        string="Academic Year",
        required=True,
        tracking=True
    )
