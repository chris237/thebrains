# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import UserError


class Cursus(models.Model):
    _name = "brains.cursus"
    _description = "Cursus"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="State", default="draft", tracking=True)

    name = fields.Char(string="Name", required=True, tracking=True)
    code = fields.Char(string="Code", required=True, tracking=True)
    number_of_years = fields.Selection(
        selection=[
            ('1', 'I'),
            ('2', 'II'),
            ('3', 'III'),
            ('4', 'IV'),
            ('5', 'V'),
        ],
        string="Number of Years",
        required=True,
        tracking=True
    )
    description = fields.Text(string="Description", tracking=True)
    level_ids = fields.One2many(
        "brains.level", "cursus_id", string="Levels", tracking=True
    )
    semester_ids = fields.One2many(
        "brains.semestre", "cursus_id", string="Semesters", tracking=True
    )

    speciality_id = fields.Many2one('brains.speciality', string="Speciality", help="Help text", tracking=True, ondelete='cascade', check_company=True)

    years_ids = fields.Many2many(
        "brains.school.year",
        "cursus_year_rel",
        "cursus_id",
        "year_id",
        string="Academic Years",
        tracking=True
    )

    def desactive(self):
        for cursus in self:
            if cursus.state == 'active':
                cursus.state = 'inactive'
                cursus.level_ids.write({'state': 'inactive'})
                cursus.semester_ids.write({'state': 'inactive'})
            else:
                raise UserError("Only active cursus can be set to inactive.")

    def action_generate_levels(self):
        self.ensure_one()  # Ensure only one record is processed

        if self.state != "draft":
            
            raise UserError("Levels can only be generated when the cursus is in draft state.")
        else:
            """Génère les levels et leurs semestres automatiquement selon le nombre d'années du cursus"""
            roman_map = {
                '1': 'I',
                '2': 'II',
                '3': 'III',
                '4': 'IV',
                '5': 'V',
            }
            for cursus in self:
                # Supprime les anciens levels + semestres liés
                cursus.level_ids.unlink()

                semestre_counter = 1  # compteur global pour tout le cursus

                # Génère les nouveaux levels
                for i in range(1, int(cursus.number_of_years) + 1):
                    level = self.env["brains.level"].create({
                        "name": f"{cursus.name} {roman_map[str(i)]}",
                        "code": f"{cursus.code}{i}",
                        "years_level": str(i),
                        "cursus_id": cursus.id,
                    })

                    # Générer 2 semestres par niveau avec numérotation continue
                    for _ in range(2):
                        self.env["brains.semestre"].create({
                            "name": f"{level.name} - Semestre {semestre_counter}",
                            "code": f"{level.code}S{semestre_counter}",
                            "level_id": level.id,
                        })
                        semestre_counter += 1
                self.state = 'active'
                self.semester_ids.write({'state': 'active'})
                self.level_ids.write({'state': 'active'})

    def write(self, vals):
        res = super().write(vals)
        if "years_ids" in vals:
            for cursus in self:
                cursus._propagate_years_to_levels_and_semesters()
        return res

    def _propagate_years_to_levels_and_semesters(self):
        """Propage les années académiques du cursus vers ses levels et semestres"""
        for cursus in self:
            if cursus.years_ids:
                # Associer les années aux niveaux
                for level in cursus.level_ids:
                    level.year_ids = [(6, 0, cursus.years_ids.ids)]
                # Associer les années aux semestres
                for semestre in cursus.semester_ids:
                    semestre.year_ids = [(6, 0, cursus.years_ids.ids)]
            else:
                # Si on vide years_ids → on vide aussi dans levels et semestres
                for level in cursus.level_ids:
                    level.year_ids = [(5, 0, 0)]
                for semestre in cursus.semester_ids:
                    semestre.year_ids = [(5, 0, 0)]