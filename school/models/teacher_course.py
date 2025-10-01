# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TeacherCourse(models.Model):
    _name = "brains.teacher.course"
    _description = "Teacher Course Assignment"

    teacher_id = fields.Many2one(
        "hr.employee",
        string="Teacher",
        required=True,
        domain=[('is_teacher', '=', True)],
        ondelete="cascade",
    )
    course_id = fields.Many2one(
        "brains.cours",
        string="Course",
        required=True,
        ondelete="cascade",
    )
    campus_ids = fields.Many2many(
        "brains.campus",
        "brains_teacher_course_campus_rel",
        "assignment_id",
        "campus_id",
        string="Campuses",
    )

    _sql_constraints = [
        (
            "teacher_course_unique",
            "unique(teacher_id, course_id)",
            "This teacher is already assigned to this course.",
        )
    ]

    @api.constrains("campus_ids", "course_id")
    def _check_campuses_within_course(self):
        for record in self:
            if record.course_id and record.campus_ids:
                invalid_campuses = record.campus_ids - record.course_id.campus_ids
                if invalid_campuses:
                    raise ValidationError(
                        "Selected campuses must be part of the course's campuses."
                    )

    @api.onchange("course_id")
    def _onchange_course_id(self):
        if self.course_id:
            self.campus_ids = self.course_id.campus_ids
        else:
            self.campus_ids = False
