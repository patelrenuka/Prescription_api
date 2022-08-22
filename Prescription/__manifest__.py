# -*- coding: utf-8 -*-
{
    'name': "Prescriptions",

    'summary': """
        Prescription Detail""",

    'description': """
       Prescription Detail,
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm'],

    # always loaded
    'data': [
        "view/prescription_view.xml",
        "view/prescription_template_view.xml",
        "view/clinic_view.xml",
        "security/ir.model.access.csv",
        "report/report.xml",
        "report/prescription_report.xml",

    ],
    # only loaded in demonstration mode
    'demo': [

        
    ],
}
