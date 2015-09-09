import wizard 
import time
import netsvc
import osv
import pooler

no_of_material_form = """<?xml version="1.0"?>
<form title ="No of resources available in library">
     <seperator string="No Of Resources Available In Library" colspan="4"/>
     <field name = "resource"/>
 </form> 
 """

no_of_material_field = {
    'resource' :{'string':'Category','type':'many2one','relation':'lms.categories' },
                          }

class wizard_no_of_material(wizard.interface):
    states = {
      'init' : {
         'actions' : [] ,
         'result' : {'type':'form' ,'arch':no_of_material_form,'fields':no_of_material_field,
                     'state':[('end','Cancel'),('print','Print')]}
         },
     'print': {
        'actions':[],
        'result':{'type':'print','report': 'no_of_material','state':'end'} 
        }
      }
wizard_no_of_material ("wizard_no_of_material")