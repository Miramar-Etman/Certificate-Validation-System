from odoo import models, fields, api, _
from datetime import *
from odoo.exceptions import ValidationError,UserError


class CertInfo(models.Model):
    _name = "cert.info"
    _description = "Certificates Information"
    _rec_name = "serial_number"
    vehicle_type = fields.Selection(
        [("Car", "Car"), ("Bus", "Bus"), ("Minibus", "Minibus"), ("Microbus", "Microbus")],
        default="Car")
    price = fields.Integer()
    chassis_number = fields.Char(size=17)
    car_brand = fields.Selection([("Mercedes", "Mercedes"), ("BMW", "BMW"), ("Toyota", "Toyota")])
    motor_number = fields.Integer()
    serial_number = fields.Char(string="Serial Number", readonly=True, required=True, copy=False, default=lambda self: _('New'))
    customer_ids = fields.Many2one(comodel_name="res.partner")
    print_state_current = fields.Selection([("print_cert", "print_cert"),
                                            ("no_print", "no_print")])

    @staticmethod
    def model_year():
        """
        Returns:
        all years between current year and 20 years before:
        """
        model = [(num, str(num)) for num in range(datetime.now().year - 19, datetime.now().year + 1)]
        return model

    car_model = fields.Selection(selection="model_year")
    traffic_department_id = fields.Many2one(comodel_name="cert.dept")
    certificate_type_id = fields.Many2one(comodel_name="cert.type")
    logs_ids = fields.One2many(comodel_name="print.log",inverse_name="customer_id")
    # override create function to change sequence number
    @api.model
    def create(self, vals):
        if vals.get('serial_number', _('New')) == _('New'):
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('cert.info.sequence') or _('New')
        result = super(CertInfo,self).create(vals)
        return  result

    def change_state(self):
        if self.print_state_current == "print_cert" or self.print_state_current == False:
                self.print_state_current= "no_print"
                self.logs_ids.create({
                    "customer_id": self.id,
                    "description": f"{self.customer_ids.display_name} Print status was changed to {self. print_state_current} at {datetime.now()}"})
                return self.env.ref('vehiclecert.certificate_template').report_action(self)


    def reprint_cert(self):
        if self.print_state_current == "no_print" or self.print_state_current ==False:
            self.print_state_current = "print_cert"
