# List of contributors:
# Segu

{
     'name': 'Cuba - Módulo base para exportar nóminas',
     'version': '0.1',
     'category': 'Uncategorized',
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["l10n_cu_hr_payroll_payment"],
     'data': [
          "security/ir.model.access.csv",
          "views/hr_payslip_view.xml",
          "views/hr_employee_view.xml",
          'wizard/load_init_payslip_run_wizard_views.xml',
     ],
}
