from matplotlib.font_manager import json_dump
from odoo import http
from odoo.http import request
import json
import importlib
from datetime import datetime,date
from json import JSONEncoder
import dateutil.parser
from odoo.addons.Prescription.controllers.login_controller import validate_token
 


class PrescriptionController(http.Controller):
    @validate_token
    @http.route('/fetchprescription', type='http', method=['GET'])
    def get_prescription(self):
        print("**************..........**********")
        try:
            rec = request.env['prescriptions.details'].search([])
            prescription_list = []
            for prescription in rec:
                vals ={
                    'id':prescription.id,
                    'contact_id':prescription.contact_id.name,
                    'age':prescription.age,
                    'email':prescription.email,
                    'gender':prescription.gender,
                    'mobile':prescription.mobile,
                    'weight':prescription.weight,
                    'symptoms':prescription.symptoms,
                    'diagnosis':prescription.diagnosis,
                    'user_id':prescription.user_id.name,
                    'date':prescription.date,
                    'valid_date':prescription.valid_date,
                    'prescription_tem_id':prescription.prescription_tem_id.name,
                    'diet_plan':prescription.diet_plan,
                    'clinic_id':prescription.clinic_id.name,
                    'medicine_pres_ids':prescription.medicine_pres_ids,
                } 
                prescription_list.append(vals)
            data = {'Code':0, 'Message':'Retrieve all prescription Records', 'Result': prescription_list}
            return json.dumps(data,default=str)
        except Exception as e:
            return {'Code':1,'Message':"something is wrong"}


    @validate_token
    @http.route('/prescription',type = "json",method=['POST'],csrf=False)
    def create_prescription(self, **rec):
        try:
            if request.jsonrequest:
                data = request.jsonrequest
                if data['contact_id']:
                    vals={
                        'contact_id':data['contact_id'],
                        'age':data['age'],
                        'email':data['email'],
                        'gender':data['gender'],
                        'mobile':data['mobile'],
                        'weight':data['weight'],
                        'symptoms':data['symptoms'],
                        'diagnosis':data['diagnosis'],
                        'user_id':data['user_id'],
                        'date':datetime.strptime(data['date'], "%d/%m/%Y"),
                        'valid_date':datetime.strptime(data['valid_date'], "%d/%m/%Y"),
                        'prescription_tem_id':data['prescription_tem_id'],
                        'diet_plan':data['diet_plan'],
                        'clinic_id':data['clinic_id'],
                    }
                
            new_data = http.request.env['prescriptions.details'].sudo().create(vals)
            print("****new_data******",new_data)
            args = {'Code':0, 'Message':'successfully New record created','Result':new_data.id}
            return  args  
        except Exception as e:
            return {'Code':1,'Message':"something is wrong",'Error':e}


    @validate_token
    @http.route('/updateprescription',type="http",method=['PUT'],csrf=False)
    def update_prescription(self, **rec):
        try:
            if request.httprequest:
                if rec['id']:
                    print("**********id*********",rec)
                    update_data =request.env['prescriptions.details'].sudo().search([('id','=',rec['id'])])
                    if update_data:
                        update_data.sudo().write(rec)
                        print("********",update_data)
                    args = {'Code':0,'Message':'Successfully Update recored','result':rec['id']}
            return json.dumps(args)
        except Exception as e:
            return {'Code':1,'Message':"id is wrong"}


    @validate_token
    @http.route('/deleteprescription/<int:rec_id>/',type="http",method=['DELETE'],csrf=False)
    def delete_prescription(self, rec_id):
        try:
            prescription_rec = request.env["prescriptions.details"].sudo().browse(rec_id)
            print("**********",prescription_rec)
            id=prescription_rec.id
            prescription_rec.unlink()
            data = {'Code':0,'Message':'Successfully deleted record','Result':id}
            return json.dumps(data)
        except Exception as e:
            return {'Code':1,'Message':"id is wrong"}











    

    # @http.route('/deleteprescription',type="http",method=['DELETE'],csrf=False)
    # def unlink_prescription(self, **rec):
    #     if request.httprequest:
    #         if rec['id']:
    #             unlink_data = request.env['prescriptions.details'].sudo().search([('id','=',rec['id'])])
    #             unlink_data.unlink(rec.id)
    #             data = {'success':True,'message':'Success'}
    #     return json.dumps(data)
