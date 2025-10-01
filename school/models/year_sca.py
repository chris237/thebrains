# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SchoolYear(models.Model):
    _name = "brains.school.year"
    _description = "School Year"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _order = "date_start desc"

    name = fields.Char(
        string="Academic Year",
        required=True,
        tracking=True,
        help="Example: 2024-2025"
    )

    code = fields.Char(
        string="Code",
        required=True,
        tracking=True,
        help="Short code: AY24-25"
    )

    date_start = fields.Date(
        string="Start Date",
        required=True,
        tracking=True
    )

    date_end = fields.Date(
        string="End Date",
        required=True,
        tracking=True
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )

    # semestre_ids = fields.One2many(
    #     "brains.semestre",
    #     "year_id",
    #     string="Semesters",
    #     tracking=True
    # )

    semestre_ids = fields.Many2many(
        "brains.semestre",
        "year_semestre_rel",       # nom de la table relationnelle
        "year_id",                 # colonne vers brains.school.year
        "semestre_id",             # colonne vers brains.semestre
        string="Semesters",
        tracking=True
    )

    level_ids = fields.Many2many(
        "brains.level",
        "level_year_rel",
        "year_id",
        "level_id",
        string="Levels",
        tracking=True
    )

    cursus_ids = fields.Many2many(
        "brains.cursus",
        "cursus_year_rel",
        "year_id",
        "cursus_id",
        string="Cursus",
        tracking=True
    )

    # pour éviter les chevauchements
    _sql_constraints = [
        ('date_check', 'CHECK(date_start < date_end)', 'La date de début doit être antérieure à la date de fin !'),
        ('unique_year', 'unique(name)', 'L\'année scolaire doit être unique !'),
    ]


    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # Propager automatiquement les années vers levels et semestres après création
            record._propagate_years_to_levels_and_semesters()
        return records

    def write(self, vals):
        res = super().write(vals) 
        # Propager les années si les cursus sont modifiés
        if 'cursus_ids' in vals or 'level_ids' in vals or 'semestre_ids' in vals:
            for year in self:
                year._propagate_years_to_levels_and_semesters()
        return res

    def _propagate_years_to_levels_and_semesters(self):
        """Propage l'année scolaire vers tous les niveaux et semestres liés aux cursus"""
        for year in self:
            # Récupérer tous les levels et semestres liés aux cursus sélectionnés
            all_levels = self.env['brains.level']
            all_semesters = self.env['brains.semestre']
            for cursus in year.cursus_ids:
                all_levels |= cursus.level_ids
                all_semesters |= cursus.semester_ids

            # Propager l'année courante
            if year.id:
                year_ids = [year.id]
            else:
                year_ids = []

            if year_ids:
                all_levels.write({'year_ids': [(6, 0, year_ids)]})
                all_semesters.write({'year_ids': [(6, 0, year_ids)]})
            else:
                all_levels.write({'year_ids': [(5, 0, 0)]})
                all_semesters.write({'year_ids': [(5, 0, 0)]})