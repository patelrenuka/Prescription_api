from odoo import fields,models,api

class clinic(models.Model):
    _name  = "clinic.details"

    name = fields.Char(string="Name")
    stock_location = fields.Many2one("stock.location",string="Stock Location")
    medicines_ids = fields.One2many("details.medicine","prescription_tem_id",string="Mediciness")
    

    