# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'School',
    'category': 'Human Resources',
    'sequence': 2,
    'summary': 'Built a new school calendar',
    'description': """
This module .
""",
    'depends': ['base','mail', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/campus.xml',
        'views/employee.xml',
        'views/teacher_course.xml',
        'views/speciality.xml',
        'views/cursus.xml',
        'views/level.xml',
        'views/semestre.xml',
        'views/year_sca.xml',
        'views/cours.xml',
        'views/menu.xml',
    ],
    'images': [
          'static/src/img/gespros_logo.png',
    ],
    'application': True,
    'license': 'LGPL-3',
    'assets': {
    }
}