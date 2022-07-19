from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    related_certificate_id = fields.One2many(comodel_name="cert.info",inverse_name="customer_ids")

