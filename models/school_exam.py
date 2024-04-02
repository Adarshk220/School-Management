# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolExam(models.Model):
    """Model for exam management"""
    _name = "school.exam"
    _description = "School Exam"
    _inherit = "mail.thread"

    name = fields.Char(string="Exam")
    student_exam_class_id = fields.Many2one("school.class", string="Class")
    student_exam_ids = fields.One2many("school.exam.paper", "student_exam_id", string="Exams")
    status = fields.Selection(selection=[
        ("draft", "Draft"),
        ("registration", "Registration")], tracking=True, default="draft")
    company_id = fields.Many2one("res.company", string="School", tracking=True,
                                 default=lambda self: self.env.company.id)

    def button_exam_registration(self):
        """Function for the button, to change the status of Exam to registration"""
        students = self.env['school.student'].search([('student_class_id', '=', self.student_exam_class_id.id)])
        papers = self.student_exam_ids
        for student in students:
            student.exam_paper_ids = [fields.Command.create({
                'subject_name_id': paper.subject_name_id.id,
                'pass_mark': paper.pass_mark,
                'max_mark': paper.max_mark,
            }) for paper in papers]

        self.status = 'registration'


class SchoolExamPaper(models.Model):
    """Model for exam management"""
    _name = "school.exam.paper"
    _description = "School Exam Paper"

    subject_name_id = fields.Many2one("school.subject", string="Subject")
    pass_mark = fields.Float(string="Pass Mark")
    max_mark = fields.Float(string="Maximum Mark")
    student_exam_id = fields.Many2one("school.exam", string="Exam")
    student_paper_id = fields.Many2one("school.student", string="Papers")
