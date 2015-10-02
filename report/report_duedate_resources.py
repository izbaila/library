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
        sno = 0
        my_dict = {'s_no':'','borrower':'','resource':'','issue_date':'','due_date':'','fine':''}
        borrower_id = pooler.get_pool(self.cr.dbname).get('lms.std.issued').search(self.cr,self.uid,[('borrower_id.id','=',form['borrower'])])
        day2 = datetime.datetime.strptime( date.today().strftime('%Y-%m-%d'), "%Y-%m-%d").date() #current date
        for i in pooler.get_pool(self.cr.dbname).get('lms.std.issued').browse(self.cr ,self.uid ,borrower_id):
            sno = sno + 1
            day1 = datetime.datetime.strptime(i.issued_date, "%Y-%m-%d").date() #date on which the book was issued
            days_past_duedate = abs((day1 - day2).days)
            if days_past_duedate > 10:
                my_dict['s_no'] = sno 
                my_dict['resource'] = i.resource_no.name
                my_dict['borrower'] = i.borrower_id.name
                my_dict['issue_date'] = i.issued_date
                my_dict['due_date'] = day1 + datetime.timedelta(days=10) #to find what the due date should be according to issue date
                if i.returned_state == 'Returned':
                    my_dict['fine'] = 0
                else:
                    fine_id = pooler.get_pool(self.cr.dbname).get('lms.fine.dues').search(self.cr,self.uid,[('catagory.type','=',i.resource_no.catagory_id.type)])
                    for fine in self.pool.get('lms.fine.dues').browse(self.cr ,self.uid ,fine_id): #to calculate fine
                        rupee = fine.fine_amount
                        my_dict['fine'] = days_past_duedate*rupee
                        res.append(my_dict)
        return res
    
report_sxw.report_sxw('report.duedate_resources','lms.issue', 
                      '/addons/cms_library/report/report_duedate_resources_view.rml',
                      parser=report_duedate_resources,
                      header=True)