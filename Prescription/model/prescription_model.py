from email.policy import default, strict
from sre_constants import SRE_FLAG_DEBUG
import string
from json import JSONEncoder
from dbus import ValidationException
from numpy import empty
from soupsieve import select
from odoo import fields,models,api
from datetime import datetime,date


class prescriptions(models.Model, JSONEncoder):
    _name = "prescriptions.details"

    contact_id = fields.Many2one("res.partner",string="Patient")
    age = fields.Integer(string="Age")
    gender = fields.Char(string="Gender")
    mobile  = fields.Integer(string="Mobile")
    email = fields.Char(string="Email")
    weight = fields.Integer(string="Weight(KG)")
    symptoms = fields.Html()
    diagnosis = fields.Html(string="Diagnosis")
    user_id = fields.Many2one("res.users",default=lambda self: self.env.user.id, string="Consulting Doctor")
    session = fields.Char(string="Session")
    date = fields.Date(string="Date",default=datetime.today())
    valid_date = fields.Date(string="Valid Till")
    prescription_tem_id = fields.Many2one("prescription.templates",string="prescription template")
    diet_plan = fields.Html(string="Diet Plan")
    clinic_id = fields.Many2one("clinic.details",string="Clinic")
    medicine_pres_ids =fields.One2many("details.medicine_prescription","prescription_id",string="Medicine")

    counted_date = fields.Integer(string="total days",compute="_compute_total_days",default=0)
    total = fields.Integer(string="Total",related='medicine_pres_ids.total')
    total_medicine=fields.Integer(string="Total Medicine",compute="_compute_medicine_count")
    
    available_med = fields.Char(string="Available Medicine",compute="_compute_available_med")

    @api.onchange('contact_id')
    def _onchange_contact_id(self):
        if self.contact_id:
           if self.contact_id.phone and self.contact_id.email:
               self.mobile = self.contact_id.phone
               self.email = self.contact_id.email

    @api.depends('valid_date', 'date')
    def _compute_total_days(self):
        for rec in self: 
            if rec.valid_date and rec.date:
                total_days = rec.valid_date - rec.date
                rec.counted_date = total_days.days
            else:
                rec.counted_date = 0


    @api.depends('total','counted_date')
    def _compute_medicine_count(self):
        for rec in self:
            if rec.total and rec.counted_date:
                total_med = rec.total * rec.counted_date
                rec.total_medicine = total_med
            else:
                rec.total_medicine = 0

    @api.onchange('prescription_tem_id')
    def onchange_prescription_tem_id(self):
        if self.prescription_tem_id:
            self.medicine_pres_ids  = False
            if self.prescription_tem_id.medicines_ids:
                for medicines_id in self.prescription_tem_id.medicines_ids:
                    med_pres = self.env['details.medicine_prescription'].create({'prescription_id': self.id, 'relation_ids': medicines_id.relation_ids.id, 
                                        'dosage': medicines_id.dosage, 'frequency': medicines_id.frequency, 'instruction': medicines_id.instruction})
                    # stock_qty = self.compute_available_med(medicines_id.relation_ids.id)
                    # req_qty = self.counted_date * medicines_id.dosage * medicines_id.frequency
                    # print("*****************stock_qty", stock_qty)
                    # print("*****************req_qty", req_qty)
                    # if req_qty > stock_qty :
                    #     med_pres.status = 1
                    # elif req_qty < stock_qty:
                    #     med_pres.status = 2
                    # else:
                    #     med_pres.status = 0
                    self.compute_stock_availability()
                    # print("******************************",abc_id)
                    #self.medicine_pres_ids = [(4,abc_id)]

    # @api.depends('stock_qty')
    def compute_available_med(self,stock_qty):
        print("*****stock_qty",stock_qty)
        if self.clinic_id:
            print("***********clinic",self.clinic_id)
            if self.clinic_id.stock_location:
                for rec in self.clinic_id.stock_location:
                    stock_qty = self.env['stock.quant'].search([('location_id','=',rec.id),('product_id','=',stock_qty)])
                    print('*****location_id',stock_qty.quantity)
                    return stock_qty.quantity


    @api.onchange('clinic_id')
    def onchange_clinic_id(self):
        self.compute_stock_availability()

    @api.depends('stock_qty')
    def compute_stock_availability(self):
        for medicines_id in self.medicine_pres_ids:
            stock_qty = self.compute_available_med(medicines_id.relation_ids.id)
            req_qty = self.counted_date * medicines_id.dosage * medicines_id.frequency
            print("*****************stock_qty", stock_qty)
            print("*****************req_qty", req_qty)
            if req_qty > stock_qty :
                medicines_id.status = 1
            elif req_qty < stock_qty:
                medicines_id.status = 2
            else:
                medicines_id.status = 0







 
    
class medicine_detail_prescription(models.Model):
    _name = "details.medicine_prescription"

    relation_ids = fields.Many2one("product.template", string="Medicines_detail",
                                help="Relationship with the Product")
    dosage = fields.Integer(string="Dosage")
    frequency = fields.Integer(string="Frequency")
    route_of_administration = fields.Char(string="Route of Administration")
    instruction = fields.Char(string="Instruction")
    prescription_tem_id = fields.Many2one("prescription.templates",string="prescription template")
    total = fields.Integer(string="Total")
    prescription_id =fields.Many2one("prescriptions.details",string="Prescription")
    status = fields.Integer(string="Status")

    @api.depends('dosage','frequency')
    def _compute_progress(self):
        for rec in self: 
            if rec.dosage and rec.frequency:
                rec.total = rec.dosage * rec.frequency
            else:
                rec.total = 0