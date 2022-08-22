from email.policy import default

from attr import field
from odoo import fields,models,api
    

class medicine_detail(models.Model):
    _name = "details.medicine"

    relation_ids = fields.Many2one("product.template", string="Medicines_detail",
                                  help="Relationship with the Product")
    dosage = fields.Integer(string="Dosage")
    frequency = fields.Integer(string="Frequency")
    route_of_administration = fields.Char(string="Route of Administration")
    instruction = fields.Char(string="Instruction")
    prescription_tem_id = fields.Many2one("prescription.templates",string="prescription template")
    
    # priority = fields.Selection([('red','Red'),
    #                             ('green','Green'),
    #                             ('yellow',"Yellow")])
    priority = fields.Char(string="Priority",compute='_compute_progress')
    # prescription_id =fields.Many2one("prescriptions.details",string="Prescription")
    # counted_date = fields.Date(string="Valid Till",related="prescriptions_details.counted_date")
   


   
   
                




class prescription_template(models.Model):
    _name = "prescription.templates"

    name = fields.Char(string="name")
    # prescription_id =fields.Many2one("prescriptions.details",string="Prescription")
    medicines_ids = fields.One2many("details.medicine","prescription_tem_id",string="Mediciness")
    
    
    
    
        

    
