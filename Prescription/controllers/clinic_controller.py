from urllib3 import HTTPResponse
from odoo import http
from odoo.http import request
import json
import importlib
from datetime import datetime,date
from json import JSONEncoder
import dateutil.parser
from odoo.addons.Prescription.controllers.login_controller import validate_token



class ClinicController(http.Controller):
    @validate_token   
    @http.route('/fetchclinic', type='http', method=['GET'], csrf=False)
    def get_client(self, **rec):
        try:
            clinic_rec = http.request.env['clinic.details'].search([])
            client_list = []
            for clinic in clinic_rec:
                vals ={
                    'id':clinic.id,
                    'name':clinic.name,
                    'stock_location':clinic.stock_location.name
                } 
                client_list.append(vals)
            data = {'Code':0, 'Message':'Retrieve all client Records', 'Result': client_list}
            return json.dumps(data,default=str)
        except Exception as e:
            return {'Code':1,'Message':"something is wrong"}


    @validate_token   
    @http.route('/clinic', type='json',method=['POST'],csrf=False)
    def create_clinic(self, **rec):
        try:
            if request.jsonrequest:
                data = request.jsonrequest
                print("*****rec****",data)
                if data['name']:
                    vals={
                        'name':data['name'],
                        'stock_location':data['stock_location']
                    }
            new_data = http.request.env['clinic.details'].sudo().create(vals)
            print("****new_data******",new_data)
           
            args = {'Code':0, 'Message':'Successfully new record created','Result':new_data.id}
            return  args
        except Exception as e:
            return {'Code':1,'Message':"something is wrong"}
        
        # data_in_json = json.load(data)	
        # print("*****rec****",data['name'])
        # return data

    @validate_token   
    @http.route('/updateclinic',type="http",method=['PUT'],csrf=False)
    def update_clinic(self, **rec):
        try:
            if request.httprequest:
                if rec['id']:
                    print("**********id*********",rec)
                    update_data = request.env['clinic.details'].sudo().search([('id','=',rec['id'])])
                    if update_data:
                        update_data.sudo().write(rec)
                        print("********",update_data)
                    data = {'Code':0,'Message':'Successfully updated recored','Result':rec['id']}
            return json.dumps(data)
        except Exception as e:
            return {'Code':1,'Message':"id is wrong"}


    @validate_token   
    @http.route('/deleteclinic/<int:rec_id>/',type="http",method=['DELETE'],csrf=False)
    def delete_clinic(self, rec_id):
        try:
            clinic_rec = request.env["clinic.details"].sudo().browse(rec_id)
            print("**********",clinic_rec)
            id=clinic_rec.id
            clinic_rec.unlink()
            data = {'Code':0,'Message':'Successfully Deleted Record','Result':id}
            return json.dumps(data)
        except Exception as e:
            return {"Code":1,'Message':"id is wrong"}

        
    





