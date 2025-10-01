# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Campus(models.Model):
    _name = "brains.campus"
    _description = "Campus"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    name = fields.Char(string="Name", required=True, tracking=True)
    address = fields.Char(string="Adress", tracking=True)
    longitude = fields.Float(string="Longitude")
    latitude = fields.Float(string="Latitude")

    secretary_ids = fields.Many2many(
        "hr.employee", string="Secrétaires",
        # domain="[('position_ids.name', '=', 'Secrétaire')]"
    )
    director_id = fields.Many2one(
        "hr.employee", string="Directeur",
        # domain="[('position_ids.name', '=', 'Directeur')]"
    )
    deputy_director_id = fields.Many2one(
        "hr.employee", string="Directeur adjoint",
        # domain="[('position_ids.name', '=', 'Directeur adjoint')]"
    )

    employee_ids = fields.One2many(
        "brains.employee.campus", "campus_id", string="Affectations"
    )

    faculty_ids = fields.Many2many(
        "brains.faculty",
        "brains_campus_faculty_rel",
        "campus_id",
        "faculty_id",
        string="Faculties",
    )


class EmployeePosition(models.Model):
    _name = "brains.employee.position"
    _description = "Poste"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Poste", required=True, tracking=True)


class Employee(models.Model):
    _name = "brains.employee"
    _description = "Employé"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    honorific = fields.Selection([
        ('dr', 'Dr.'),
        ('ing', 'Ing.'),
        ('mr', 'Mr.'),
        ('me', 'Me'),
        ('mme', 'Mme'),
        ('mlle', 'Mlle')
    ], string="Titre", tracking=True)

    name = fields.Char(string="Nom", required=True, tracking=True)
    prename = fields.Char(string="Prénom", tracking=True)
    email = fields.Char(string="Email" , tracking=True)
    phone = fields.Char(string="Téléphone", tracking=True)
    is_teacher = fields.Boolean(string="Est enseignant ?")

    position_ids = fields.Many2many(
        "hr.job", string="Postes", tracking=True
    )

    campus_affectation_ids = fields.One2many(
        "brains.employee.campus", "employee_id", string="Affectations"
    )

class EmployeeHenrit(models.Model):
    _inherit = "hr.employee"

    campus_affectation_ids = fields.One2many(
        "brains.employee.campus", "employee_id", string="Affectations"
    )
    is_teacher = fields.Boolean(string="Is Teacher ?")
    is_student = fields.Boolean(string="Is Student ?")

    

    @api.constrains("is_teacher", "is_student")
    def _check_teacher_student_exclusivity(self):
        for rec in self:
            if rec.is_teacher and rec.is_student:
                raise ValidationError(
                    "Someone can't be both a teacher and a student."
                )

    
    @api.onchange("is_teacher", "is_student")
    def _onchange_teacher_student(self):
        if self.is_teacher:
            self.is_student = False
        elif self.is_student:
            self.is_teacher = False

class EmployeeCampus(models.Model):
    _name = "brains.employee.campus"
    _description = "Affectation Employé-Campus"

    employee_id = fields.Many2one("hr.employee", string="Employe", required=True, ondelete="cascade")
    campus_id = fields.Many2one("brains.campus", string="Campus", required=True)
    position_id = fields.Many2one("hr.job", string="Poste", required=True)

class Faculty(models.Model):
    _name = "brains.faculty"
    _description = "facultes"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name of the faculty", tracking=True, required=True)
    employee_id = fields.Many2one(
        "hr.employee", string="Names of department heads",  tracking=True, required=True,
        domain="[('is_teacher', '=', True)]"
    )
    employee_email = fields.Char(related="employee_id.email", string="Email", store=True)
    employee_phone = fields.Char(related="employee_id.phone", string="Phone", store=True)

    campus_ids = fields.Many2many(
        "brains.campus",
        "brains_campus_faculty_rel",
        "faculty_id",
        "campus_id",
        string="Campuses",
        required=True,
    )
    speciality_ids = fields.One2many(
        "brains.speciality", "faculty_id", string="Speciality"
    )
    