from httplib2 import Response
from odoo import http
from odoo.http import request
import json
import importlib
from datetime import datetime,date
import dateutil.parser
from odoo.addons.Prescription.controllers.login_controller import validate_token





class MedicineController(http.Controller):
    @validate_token
    @http.route('/fetchmedicine', type='http', method=['GET'])
    def get_medicine(self):
        try:
            medicine_rec = http.request.env['details.medicine'].search([])
            medicine_list = []
            for medicine in medicine_rec:
                vals ={
                    'id':medicine.id,
                    'prescription_tem_id':medicine.prescription_tem_id.name,
                    'relation_ids':medicine.relation_ids.name,
                    'dosage':medicine.dosage,
                    'frequency':medicine.frequency,
                    'route_of_administration':medicine.route_of_administration,
                    'instruction':medicine.instruction
                } 
                medicine_list.append(vals)
                # print("**********medicine_list",medicine_list)
            data = {'Code':0, 'Message':'Retrieve all medicine Records','Result': medicine_list }
           
            return json.dumps(data,default=str)
        except Exception as e:
            return {'Code':1,'Message':"something is wrong"}
            # 0 means True ,
            # 1 means False


    @validate_token
    @http.route('/medicine', type='json',method=['POST'],csrf=False)
    def create_medicine(self, **rec):
        try:
            if request.jsonrequest:
                data = request.jsonrequest
                if data['relation_ids']:
                    vals={
                        'prescription_tem_id':data['prescription_tem_id'],
                        'relation_ids':data['relation_ids'],
                        'dosage':data['dosage'],
                        'frequency':data['frequency'],
                        'route_of_administration':data['route_of_administration'],
                        'instruction':data['instruction']
                    }
            new_data = http.request.env['details.medicine'].sudo().create(vals)
            print("****new_data******",new_data)
            Response.status="201 Created"
            args = {'Code':0, 'Message':'Successfully new record created ','Result':new_data.id}
            
            return  args
        except Exception as e:
            return {'Code':1,'message':"something is wrong"}
    

    @validate_token
    @http.route('/updatemedicine',type="http",method=['PUT'],csrf=False)
    def update_medicine(self, **rec):
        try:
            if request.httprequest:
                if rec['id']:
                    print("**********id*********",rec)
                    update_data = request.env['details.medicine'].sudo().search([('id','=',rec['id'])])
                    if update_data:
                        update_data.sudo().write(rec)
                        print("********",update_data)
                    data = {'Code':0,'Message':'Successfully Updated Record','Result':rec['id']}
            return json.dumps(data)
        except Exception as e:
            return {'Code':1,'Message':"id is wrong"}


    @validate_token
    @http.route('/delete_medicine/<int:rec_id>',type="http",method=['DELETE'],csrf=False)
    def delete_medicine(self,rec_id):
        try:
            prescription_rec = request.env['details.medicine'].sudo().browse(rec_id)
            id = prescription_rec.id
            prescription_rec.unlink()
            data ={'Code':0, 'Message':'Successfully Record is Deleted','Result':id}
            return json.dumps(data)
        except Exception as e:
            return {'Code':1,'Message':"id is wrong"}



 