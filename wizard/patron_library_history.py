import wizard
import time
import netsvc
import osv
import pooler

patron_resource_form = """<?xml version="1.0"?>
<form title ="History of resources issued by patron">
     <seperator string="Issue resources" colspan="4"/>
     <field name = "borrower"/>
 </form> 
 """
patron_resource_field = {
    'borrower' :{'string':'Borrower Name','type':'many2one','relation':'lms.patron.registration' },
                          }


class wizard_patron_library_history(wizard.interface):
    states = {
      'init' : {
         'actions' : [] ,
         'result' : {'type':'form' ,'arch':patron_resource_form,'fields':patron_resource_field,
                     'state':[('end','Cancel'),('print','print')]}
         },
     'print': {
        'actions':[],
        #'result':{'type':'state','state':'end'}
        'result':{'type':'print','report': 'patron_library_history','state':'end'} 
        }
      }
wizard_patron_library_history("wizard_patron_library_history")