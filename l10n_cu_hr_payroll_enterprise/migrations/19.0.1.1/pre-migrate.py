def migrate(cr, version):
    """hr.payslip.total fue renombrado a total_ps (commit 8010e9e, migración a 19.0).

    La tabla nunca llegó a sincronizarse porque las vistas seguían pidiendo el
    campo viejo y el -u fallaba antes de llegar a crear la columna. Se renombra
    la columna física para no perder los totales ya calculados/pagados.
    """
    cr.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'hr_payslip' AND column_name = 'total'
    """)
    if not cr.fetchone():
        return

    cr.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'hr_payslip' AND column_name = 'total_ps'
    """)
    if cr.fetchone():
        return

    cr.execute('ALTER TABLE hr_payslip RENAME COLUMN total TO total_ps')
