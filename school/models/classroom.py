# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Classroom(models.Model):
    _name = "brains.classroom"
    _description = "Class"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store=True,
        tracking=True,
    )
    code = fields.Char(string="Code", tracking=True)
    campus_id = fields.Many2one(
        "brains.campus",
        string="Campus",
        required=True,
        tracking=True,
    )
    semester_id = fields.Many2one(
        "brains.semestre",
        string="Semester",
        required=True,
        tracking=True,
    )
    year_id = fields.Many2one(
        "brains.school.year",
        string="Academic Year",
        required=True,
        tracking=True,
    )
    level_id = fields.Many2one(
        "brains.level",
        string="Level",
        related="semester_id.level_id",
        store=True,
        readonly=True,
        tracking=True,
    )
    cursus_id = fields.Many2one(
        "brains.cursus",
        string="Cursus",
        related="semester_id.cursus_id",
        store=True,
        readonly=True,
        tracking=True,
    )
    speciality_id = fields.Many2one(
        "brains.speciality",
        string="Speciality",
        related="semester_id.speciality_id",
        store=True,
        readonly=True,
        tracking=True,
    )
    faculty_id = fields.Many2one(
        "brains.faculty",
        string="Faculty",
        related="speciality_id.faculty_id",
        store=True,
        readonly=True,
        tracking=True,
    )
    student_ids = fields.Many2many(
        "hr.employee",
        "brains_classroom_student_rel",
        "classroom_id",
        "student_id",
        string="Students",
        domain=[('is_student', '=', True)],
        tracking=True,
    )
    teacher_ids = fields.Many2many(
        "hr.employee",
        "brains_classroom_teacher_rel",
        "classroom_id",
        "teacher_id",
        string="Teachers",
        domain=[('is_teacher', '=', True)],
        tracking=True,
    )
    timetable_ids = fields.One2many(
        "brains.timetable",
        "classroom_id",
        string="Timetables",
    )

    _sql_constraints = [
        (
            "unique_classroom_per_semester_year_campus",
            "unique(semester_id, year_id, campus_id)",
            "A class already exists for this semester, year and campus.",
        )
    ]

    @api.depends("semester_id", "year_id", "campus_id")
    def _compute_name(self):
        for classroom in self:
            parts = []
            if classroom.semester_id:
                parts.append(classroom.semester_id.name)
            if classroom.year_id:
                parts.append(classroom.year_id.name)
            if classroom.campus_id:
                parts.append(classroom.campus_id.name)
            classroom.name = " - ".join(parts) if parts else False

    @api.constrains("semester_id", "year_id")
    def _check_year_in_semester(self):
        for classroom in self:
            if classroom.semester_id and classroom.year_id:
                if classroom.year_id not in classroom.semester_id.year_ids:
                    raise ValidationError(
                        "The selected academic year is not linked to the semester.",
                    )

    @api.constrains("student_ids")
    def _check_student_roles(self):
        for classroom in self:
            invalid_students = classroom.student_ids.filtered(lambda s: not s.is_student)
            if invalid_students:
                raise ValidationError(
                    "All members assigned to a class as students must have the student role.",
                )

    @api.constrains("teacher_ids")
    def _check_teacher_roles(self):
        for classroom in self:
            invalid_teachers = classroom.teacher_ids.filtered(lambda t: not t.is_teacher)
            if invalid_teachers:
                raise ValidationError(
                    "All members assigned to a class as teachers must have the teacher role.",
                )
