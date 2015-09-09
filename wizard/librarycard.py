import wizard
import time
import netsvc
import osv
import pooler
import contextlib
from osv import fields, osv, orm 

librarycard_form = """<?xml version="1.0"?>
<form title ="Selection form">
     <seperator string="Library Card" colspan="4"/>
     <field name="borrower_id"/>
 </form> 
 """
 
librarycard_fields={
     'borrower_id': {'string':'Patron','type':'many2one','relation':'lms.patron.registration'},
    }

class wizard_librarycard(wizard.interface):

    states={
        'init': {
        'actions':[],
        'result' : {'type' : 'form','arch':librarycard_form,'fields':librarycard_fields,'state':[('end','Cancel'),('print','Print')]}
        },
        'print': {
        'actions':[],
        #'result':{'type':'state','state':'end'}  #for generating wizard
        'result':{'type':'print','report': 'librarycard','state':'end'} #for generating report
        }
    }
wizard_librarycard("wizard_librarycard")