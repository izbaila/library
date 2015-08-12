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
        my_dict = {'name':'', 'father_name':'','program/designation':'','pic':'','type':'','address':'','issue_date':'','expiry_date':''}
        my_dict['name'] = obj.name
        my_dict['type'] = obj.type
        my_dict['address'] = ""
        my_dict['issue_date'] =self.pool.get('lms.library.card').browse(self.cr, self.uid,form['borrower_id']).issue_date
        my_dict['expiry_date'] =self.pool.get('lms.library.card').browse(self.cr, self.uid,form['borrower_id']).expiry_date
        if obj.type == 'student':
            stu_obj = self.pool.get('lms.entryregis').search(self.cr, self.uid,[('id','=',obj.student_id.id)])
            for i in self.pool.get('lms.entryregis').browse(self.cr, self.uid,stu_obj):
                my_dict['father_name'] = i.father_name
                my_dict['pic'] = i.image
                my_dict['program/designation'] = i.degree
                result.append(my_dict)
        else:
            emp_obj = self.pool.get('lms.hr.employee').search(self.cr ,self.uid,[('id','=',obj.employee_id.id)])
            for i in self.pool.get('lms.hr.employee').browse(self.cr, self.uid,emp_obj):
                my_dict['father_name'] = ""
                my_dict['pic'] = ""
                my_dict['program/designation'] = i.department_name
                result.append(my_dict) 
        return result

report_sxw.report_sxw('report.librarycard',
                      'lms.library.card',
                      '/addons/cms_library/report/report_librarycard.rml',
                      parser=report_librarycard,
                      header=True)