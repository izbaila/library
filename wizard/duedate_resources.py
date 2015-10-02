import wizard
import time
import netsvc
import osv
import pooler

fine_form = """<?xml version="1.0"?>
<form title ="History of resources issued by patron">
     <seperator string="Issue resources" colspan="4"/>
     <field name = "borrower"/>
 </form> 
 """
fine_field = {
    'borrower' :{'string':'Borrower Name','type':'many2one','relation':'lms.patron.registration' },
    
                          }
class wizard_duedate_resources(wizard.interface):
    states = {
      'init' : {
         'actions' : [] ,
         'result' : {'type':'form' ,'arch':fine_form,'fields':fine_field,
                     'state':[('end','Cancel'),('print','print')]}
         },
     'print': {
        'actions':[],
        #'result':{'type':'state','state':'end'}
        'result':{'type':'print','report': 'duedate_resources','state':'end'} 
        }
      }
wizard_duedate_resources ("wizard_duedate_resources")