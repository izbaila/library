import pooler
import time
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula

class report_librarycard(rml_parse.rml_parse):
    
    def __init__(self, cr, uid, name, context):
            super(report_librarycard, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({ 'get_patron_for_cards':self.get_patron_for_cards,
                                   })

    def get_patron_for_cards(self,form):
        result = []
        obj = self.pool.get('lms.patron.registration').browse(self.cr, self.uid,form['borrower_id'])
        if obj.type == 'student':
            objss = self.pool.get('lms.library.card').browse(self.cr, self.uid, form['borrower_id'])
            record = self.pool.get('lms.entryregis').browse(self.cr,self.uid,obj.student_id.id)
            my_dict = {'name':'', 'father_name':'','program/designation':'','pic':'','type':'','address':'','issue_date':'','expiry_date':''}
            my_dict['name'] = record.name
            my_dict['program'] = record.degree
            my_dict['father_name'] = record.father_name
            my_dict['pic'] = record.image
            my_dict['type'] = "STUDENT"
            my_dict['address'] = "Hayatabad Phase 7 Institute of Management Sciences"
            my_dict['issue_date'] = objss.issue_date
            my_dict['expiry_date'] = objss.expiry_date
            result.append(my_dict)
        if obj.type == 'employee':
            objss = self.pool.get('lms.library.card').browse(self.cr, self.uid, form['borrower_id'])
            record = self.pool.get('lms.hr.employee').browse(self.cr,self.uid,obj.employee_id.id)
            my_dict = {'student_name':'', 'father_name':'','program/designation':'','pic':'', 'type':'','address':'','issue_date':'','expiry_date':''}
            my_dict['name'] = record.name
            my_dict['program/designation'] = record.department_name
            my_dict['father_name'] = "Someone"
            my_dict['pic'] = ""
            my_dict['type'] = "EMPLOYEE"
            my_dict['address'] = "Hayatabad Phase 7 Institute of Management Sciences"
            my_dict['issue_date'] = objss.issue_date
            my_dict['expiry_date'] = objss.expiry_date
            result.append(my_dict)
        return result

report_sxw.report_sxw('report.librarycard',
                      'lms.library.card',
                      '/addons/cms_library/report/report_librarycard.rml',
                      parser=report_librarycard,
                      header=True)