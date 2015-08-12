import wizard
import time
import netsvc
import osv
import pooler

patron_form = """<?xml version="1.0"?>
<form title ="History of resources issued by patron">
     <seperator string="Issue resources" colspan="4"/>
     <field name = "patron"/>
 </form> 
 """
patron_field = {
     'patron': {
                'string':"Patron Type",
                'type':'selection',
                'required':True,
                'selection':[('student','Student'),
                             ('employee','Employee'),
                             ('all','All patrons')
                            ],
                'default': lambda *a:'none'
                },

                          }
class wizard_show_patrons(wizard.interface):
    states = {
      'init' : {
         'actions' : [] ,
         'result' : {'type':'form' ,'arch':patron_form,'fields':patron_field,
                     'state':[('end','Cancel'),('print','print')]}
         },
     'print': {
        'actions':[],
     #   'result':{'type':'state','state':'end'}
        'result':{'type':'print','report': 'show_patrons','state':'end'} 
        }
      }
wizard_show_patrons ("wizard_show_patrons")