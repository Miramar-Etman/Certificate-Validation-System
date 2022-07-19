from odoo import models, fields


class CertType(models.Model):
    _name = "cert.type"
    _description = "Available certificates"
    _rec_name = "certificate_type"
    certificate_type = fields.Char()
