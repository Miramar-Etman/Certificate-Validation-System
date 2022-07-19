from odoo import models, fields


class CertDept(models.Model):
    _name = "cert.dept"
    _description = "Available Traffic departments"
    _rec_name = "certificate_dept"
    certificate_dept = fields.Char()