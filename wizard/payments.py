import wizard
import time
import netsvc
import osv
import pooler

payments_form= """<?xml version="1.0"?>
<form title ="History of resources issued by patron">
     <seperator string="Issue resources" colspan="4"/>
     <field name = "payments"/>
 </form>  """
payments_fields ={
   'payments' :{'string':'Borrower Name','type':'selection','selection':[('Paid','Paid'),('Unpaid','Unpaid'),('Paid/Unpaid','Paid/Unpaid')],'required':True}
                  }
class wizard_payments(wizard.interface):
    states = {
              'init' :{
                       'actions' : [],
                       'result' : {'type' : 'form' ,'arch' :payments_form ,'fields':payments_fields,
                                   'state':[('end','Cancel'),('Print','Print')] }
                       },
              'Print':{
                       'actions' :[],
                       'result':{'type':'state','state':'end'}
                       }
              }
wizard_payments ("wizard_payments")
