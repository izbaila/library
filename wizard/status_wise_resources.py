import wizard
import time
import netsvc
import osv
import pooler

status_form = """<?xml version="1.0"?>
<form title ="History of resources issued by patron">
     <seperator string="Issue resources" colspan="4"/>
     <field name = "status"/>
 </form> 
 """
status_fields = {
 #   'status' :{'string':'Resource Status','type':'many2one','relation':'lms.cataloge' },
    'status': {
                'string':"Resource Status",
                'type':'selection',
                'selection':[('Active','Active'),
                             ('Deactive','Deactive'),
                             ('Issued','Issued'),
                             ('Returned','Returned'),
                             ('Reserved','Reserved')],
                'default': lambda *a:'none'
                },
                          }
class wizard_status_wise_resources(wizard.interface):
    states = {
      'init' : {
         'actions' : [] ,
         'result' : {'type':'form' ,'arch':status_form,'fields':status_fields,
                     'state':[('end','Cancel'),('print','print')]}
         },
     'print': {
        'actions':[],
        #'result':{'type':'state','state':'end'}
        'result':{'type':'print','report': 'status_wise_resources','state':'end'} 
        }
      }
wizard_status_wise_resources ("wizard_status_wise_resources")