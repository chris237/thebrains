# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Timetable(models.Model):
    _name = "brains.timetable"
    _description = "Class Timetable"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _order = "start_datetime"

    name = fields.Char(
        string="Description",
        compute="_compute_name",
        store=True,
        tracking=True,
    )
    classroom_id = fields.Many2one(
        "brains.classroom",
        string="Class",
        required=True,
        tracking=True,
        ondelete="cascade",
    )
    course_id = fields.Many2one(
        "brains.cours",
        string="Course",
        required=True,
        tracking=True,
    )
    teacher_id = fields.Many2one(
        "hr.employee",
        string="Teacher",
        required=True,
        domain=[('is_teacher', '=', True)],
        tracking=True,
    )
    campus_id = fields.Many2one(
        "brains.campus",
        related="classroom_id.campus_id",
        string="Campus",
        store=True,
        readonly=True,
        tracking=True,
    )
    level_id = fields.Many2one(
        "brains.level",
        related="classroom_id.level_id",
        string="Level",
        store=True,
        readonly=True,
        tracking=True,
    )
    semester_id = fields.Many2one(
        "brains.semestre",
        related="classroom_id.semester_id",
        string="Semester",
        store=True,
        readonly=True,
        tracking=True,
    )
    cursus_id = fields.Many2one(
        "brains.cursus",
        related="classroom_id.cursus_id",
        string="Cursus",
        store=True,
        readonly=True,
        tracking=True,
    )
    year_id = fields.Many2one(
        "brains.school.year",
        related="classroom_id.year_id",
        string="Academic Year",
        store=True,
        readonly=True,
        tracking=True,
    )
    speciality_id = fields.Many2one(
        "brains.speciality",
        related="classroom_id.speciality_id",
        string="Speciality",
        store=True,
        readonly=True,
        tracking=True,
    )
    start_datetime = fields.Datetime(
        string="Start",
        required=True,
        tracking=True,
    )
    end_datetime = fields.Datetime(
        string="End",
        required=True,
        tracking=True,
    )
    location = fields.Char(string="Location", tracking=True)
    notes = fields.Text(string="Notes", tracking=True)

    _sql_constraints = [
        (
            "teacher_course_unique_slot",
            "unique(classroom_id, course_id, teacher_id, start_datetime, end_datetime)",
            "This timetable entry is already defined.",
        )
    ]

    @api.depends("classroom_id", "course_id", "start_datetime")
    def _compute_name(self):
        for timetable in self:
            parts = []
            if timetable.classroom_id:
                parts.append(timetable.classroom_id.name)
            if timetable.course_id:
                parts.append(timetable.course_id.name)
            if timetable.start_datetime:
                parts.append(fields.Datetime.to_string(timetable.start_datetime))
            timetable.name = " - ".join(parts) if parts else False

    @api.constrains("start_datetime", "end_datetime")
    def _check_chronology(self):
        for timetable in self:
            if timetable.start_datetime and timetable.end_datetime:
                if timetable.start_datetime >= timetable.end_datetime:
                    raise ValidationError("The end time must be after the start time.")

    @api.constrains("course_id", "semester_id", "year_id")
    def _check_course_semester_year(self):
        for timetable in self:
            if timetable.course_id and timetable.semester_id:
                if timetable.course_id.semester_id != timetable.semester_id:
                    raise ValidationError(
                        "The course must belong to the same semester as the class.",
                    )
            if timetable.course_id and timetable.year_id:
                if timetable.course_id.years_id != timetable.year_id:
                    raise ValidationError(
                        "The course must belong to the same academic year as the class.",
                    )
            if timetable.course_id and timetable.campus_id:
                if timetable.campus_id not in timetable.course_id.campus_ids:
                    raise ValidationError(
                        "The course is not available for the selected campus.",
                    )

    @api.constrains("teacher_id", "course_id")
    def _check_teacher_course_assignment(self):
        for timetable in self:
            if timetable.teacher_id and timetable.course_id:
                assignments = timetable.course_id.teacher_course_ids.filtered(
                    lambda assignment: assignment.teacher_id == timetable.teacher_id
                )
                if not assignments:
                    if timetable.course_id.responsible_id != timetable.teacher_id:
                        raise ValidationError(
                            "The teacher is not assigned to the selected course.",
                        )
                else:
                    if timetable.campus_id and not any(
                        timetable.campus_id in assignment.campus_ids
                        for assignment in assignments
                    ):
                        raise ValidationError(
                            "The teacher is not assigned to this course for the selected campus.",
                        )

    @api.constrains("classroom_id", "start_datetime", "end_datetime")
    def _check_classroom_overlap(self):
        for timetable in self:
            if timetable.classroom_id and timetable.start_datetime and timetable.end_datetime:
                domain = [
                    ("classroom_id", "=", timetable.classroom_id.id),
                    ("id", "!=", timetable.id),
                    ("start_datetime", "<", timetable.end_datetime),
                    ("end_datetime", ">", timetable.start_datetime),
                ]
                conflict = self.search_count(domain)
                if conflict:
                    raise ValidationError(
                        "The class already has a timetable entry during this period.",
                    )

    @api.constrains("teacher_id", "start_datetime", "end_datetime")
    def _check_teacher_overlap(self):
        for timetable in self:
            if timetable.teacher_id and timetable.start_datetime and timetable.end_datetime:
                domain = [
                    ("teacher_id", "=", timetable.teacher_id.id),
                    ("id", "!=", timetable.id),
                    ("start_datetime", "<", timetable.end_datetime),
                    ("end_datetime", ">", timetable.start_datetime),
                ]
                conflict = self.search_count(domain)
                if conflict:
                    raise ValidationError(
                        "The teacher is already scheduled during this period.",
                    )

    @api.onchange("course_id")
    def _onchange_course_id(self):
        if self.course_id:
            if self.course_id.responsible_id:
                self.teacher_id = self.course_id.responsible_id
            domain = [
                ("semester_id", "=", self.course_id.semester_id.id),
            ]
            if self.course_id.years_id:
                domain.append(("year_id", "=", self.course_id.years_id.id))
            return {
                "domain": {
                    "classroom_id": domain,
                }
            }
        return {}

    @api.onchange("classroom_id")
    def _onchange_classroom_id(self):
        if self.classroom_id:
            domain = [
                ("semester_id", "=", self.classroom_id.semester_id.id),
            ]
            if self.classroom_id.year_id:
                domain.append(("years_id", "=", self.classroom_id.year_id.id))
            return {
                "domain": {
                    "course_id": domain,
                }
            }
        return {}
