import wizard
import time
import netsvc
import osv
import pooler

borrowe_resource_form = """<?xml version="1.0"?>
<form title ="History of resources issued by patron">
     <separator string="Issue resources" colspan="4"/>
     <field name = "borrower"/>
 </form> 
 """
borrowe_resource_field = {
    'borrower' :{'string':'Borrower Name','type':'many2one','relation':'lms.patron.registration' },
                          }
class wizard_borrrowe_resources(wizard.interface):
    states = {
      'init' : {
         'actions' : [] ,
         'result' : {'type':'form' ,'arch':borrowe_resource_form,'fields':borrowe_resource_field,
                     'state':[('end','Cancel'),('print','print')]}
         },
     'print': {
        'actions':[],
        #'result':{'type':'state','state':'end'}
        'result':{'type':'print','report': 'borrowe_resources','state':'end'} 
        }
      }
wizard_borrrowe_resources ("wizard_borrrowe_resources")