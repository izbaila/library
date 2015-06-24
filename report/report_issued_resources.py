import pooler
import time
import rml_parse
from report import report_sxw
import netsvc

class report_issued_resources(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_issued_resources, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({ 'get_borrower_detail':self.get_borrower_detail,
                                   })
    def get_borrower_detail(self,form):
        result = []
                
        my_dict = {'name':'' ,'type':'' ,'group':'' ,'degree':'' ,'image':'' }
        
        rec_users = pooler.get_pool(self.cr.dbname).get('lms.patron.registration').browse(self.cr ,self.uid ,form['borrower'])
        my_dict['name'] = rec_users.name
        my_dict['type'] = rec_users.type
        if rec_users.type == 'student':
            my_dict['group'] = rec_users.student_id.group
            my_dict['degree'] = rec_users.student_id.degree
            my_dict['image'] = rec_users.student_id.image
        return result

report_sxw.report_sxw('report.issued_resources',
                      'lms.patron.registration', 
                      '/addons/lms/report/report_issued_resources_view.rml',
                      parser=report_issued_resources,
                      header=True)
