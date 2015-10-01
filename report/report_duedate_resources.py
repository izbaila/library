import pooler
import time
from datetime import date
import datetime
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula
from werkzeug.testsuite import formparser

class report_duedate_resources(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_duedate_resources, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({'get_patron_fine':self.get_patron_fine, 
                                      'get_month' :self.get_month,
                                   })
    def get_month(self,form):
        month = datetime.datetime.now().strftime("%h ,%Y")
        return month
    def get_patron_fine(self,form):
        res= []
        id_issue_borrower = pooler.get_pool(self.cr.dbname).get('lms.issue').search(self.cr,self.uid,[('borrower_id.id','=',form['borrower'])]) #to grab the id of borrower if he had issued any books
        r = pooler.get_pool(self.cr.dbname).get('lms.issue').browse(self.cr ,self.uid ,id_issue_borrower)
        d2 = datetime.datetime.strptime( date.today().strftime('%Y-%m-%d'), "%Y-%m-%d").date() #current date
        serial_no = 0
        for i in r:
            serial_no = serial_no+1
            my_dict = {'s_no':'','borrower':'','resource':'','issue_date':'','due_date':'','fine':''}
            my_dict['borrower'] = i.borrower_id.name 
            my_dict['issue_date'] = i.issue_date
            d1 = datetime.datetime.strptime(i.issue_date, "%Y-%m-%d").date() #date on which the book was issued
            days_past_duedate = abs((d1 - d2).days) 
            for c in i.resource:
                my_dict['resource'] = c.resource_no.name
                if days_past_duedate > 10:
                    print "YOU HAVE BEEN FINED"
                    my_dict['due_date'] = d1 + datetime.timedelta(days=10) #to find what the due date should be according to issue date
                    fine_id = pooler.get_pool(self.cr.dbname).get('lms.fine.dues').search(self.cr,self.uid,[('catagory.type','=',c.resource_no.catagory_id.type)])
                    for fine in self.pool.get('lms.fine.dues').browse(self.cr ,self.uid ,fine_id): #to calculate fine
                        rupee= fine.fine_amount
                        my_dict['fine'] = days_past_duedate*rupee
                        my_dict['s_no'] = serial_no
                        res.append(my_dict)
                        for keys,val in my_dict.items():
                            print keys ,"=>", val
                        
                        
        
        print "function"
        return res
    
report_sxw.report_sxw('report.duedate_resources','lms.issue', 
                      '/addons/cms_library/report/report_duedate_resources_view.rml',
                      parser=report_duedate_resources,
                      header=True)