url = "http://localhost:8069"
db = "prescription_db"
username = 'admin'
password = 'admin'

import xmlrpc.client as xmlrpclib

# common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
# versions=common.version()
# print("Details",versions)
# ORRR


import xmlrpc.client
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
versions=common.version()
print("details",versions)

uid = common.authenticate(db, username, password, {})
print('UID',uid)

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
pres_ids=models.execute_kw(db, uid, password,'prescriptions.details', 'search',[[]], {})
print("Prescriptions...",pres_ids)

presc_count=models.execute_kw(db, uid, password,'prescriptions.details', 'search_count',[[]])
print("Customers...",presc_count)



search_read_rec=models.execute_kw(db, uid, password,'prescriptions.details', 'search_read',[[]],{'fields': ['id','contact_id'], 'limit': 2})
print("Search_read_record",search_read_rec)
for records in search_read_rec:
    print(records)

# created_new_record = models.execute_kw(db, uid, password, 'prescriptions.details', 'create', [{'mobile': "889977445",'email':'divya@gmail.com'}])
# print("new presc record",created_new_record)

models.execute_kw(db, uid, password, 'prescriptions.details', 'write', [[4], {'mobile': "998877445"}])

models.execute_kw(db, uid, password, 'prescriptions.details', 'unlink', [[4]])