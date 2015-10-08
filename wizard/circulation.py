import wizard
import time
import netsvc
import osv
import pooler
import contextlib
from osv import fields, osv, orm 

borrowe_form = """<?xml version="1.0"?>
<form title ="Selection form">
     <separator string="Circulation" colspan="4"/>
     <field name = "borrower"/><newline/>
     <field name = "report"/><newline/>
     <separator string = "Enter the duration slot"/><newline/>
     <field name = "start_date"/><newline/>
     <field name = "end_date" />
     
 </form> 
 """
borrowe_field = {
      'borrower' :{'string':'Patron Name','type':'many2one' ,'relation':'lms.patron.registration' ,'required':'True'},
      'report' : {'string':'Report Options', 'type':'selection' , 'required': 'True' ,
                'selection':[('issue','Issued books'),('return','Returned books'),('all_history','Over all history')] },
      'start_date' :{'string':'Start Date' ,'type':'date'},
      'end_date' :{'string':'End Date' ,'type':'date'}

    } 
class wizard_circulation(wizard.interface):
            
    def choice (self ,cr ,uid ,data ,context):
        res = data['form']
        if res != 'False':
            if res['report'] == 'issue':
                return 'issue'
            elif res['report'] == 'return':
                return 'return'
            elif res['report'] == 'all_history':
                return 'all_history'
                
    states = {
      'init' : {
         'actions' : [] ,
         'result' : {'type':'form' ,'arch':borrowe_form,'fields':borrowe_field,
                     'state':[('end','Cancel','gtk-cancel'), ('Print','Print','gtk-go-forward')]}
         },
     'Print' :{
                'actions' :[],
                'result' : {'type':'choice' ,'next_state':choice} 
                },
    'issue': {
        'actions':[],
         'result':{'type':'print','report': 'borrowe_resources','state':'end'} 
        },
    'return': {
        'actions':[],
        'result':{'type':'print','report': 'return_materail','state':'end'} 
        },
    'all_history': {
        'actions':[],
       'result':{'type':'print','report': 'patron_library_history','state':'end'} 
        },
      }
wizard_circulation ("wizard_circulation")