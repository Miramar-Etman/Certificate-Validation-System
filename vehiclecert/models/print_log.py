from odoo import models, fields



class PrintLog(models.Model):
    _name = "print.log"
    description = fields.Text()
    user_name= fields.Char(related='customer_id.display_name')
    _rec_name = "description"

    #Relational fields
    customer_id = fields.Many2one(comodel_name="cert.info")