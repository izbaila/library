import pooler
import time
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula

class report_show_patrons(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_show_patrons, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({'get_detail_patrons':self.get_detail_patrons, 
                                      'no_of_patrons':self.no_of_patrons,
                                   })
    def no_of_patrons(self,form):
        res = ""
        if form['patron'] =='student':
            sql = """ SELECT COUNT(*) FROM lms_patron_registration
                WHERE lms_patron_registration.type = 'student'  """
            self.cr.execute(sql)
            no = self.cr.fetchone()
            res = 'Total no of registered '+ form['patron']+'s in library= '+str(no[0])
        elif form['patron'] =='employee':
            sql = """ SELECT COUNT(*) FROM lms_patron_registration
                WHERE lms_patron_registration.type = 'employee'  """
            self.cr.execute(sql)
            no = self.cr.fetchone()
            res = 'Total no of registered '+ form['patron']+'s in library= '+str(no[0])
        else:
            sql = """ SELECT COUNT(*) FROM lms_patron_registration """
            self.cr.execute(sql)
            no = self.cr.fetchone()
            res = 'Total no of registered library patrons= '+str(no[0])            
        return res
    
    def get_detail_patrons(self,form):
        res = []
        serial_no=0
        if form['patron'] == 'student':
            patron_ids = self.pool.get('lms.patron.registration').search(self.cr ,self.uid ,[('type','=','student')])
            for i in self.pool.get('lms.patron.registration').browse(self.cr ,self.uid ,patron_ids):
                my_dict = {'s_no':'' ,'name':'' ,'dep/degree':''  ,'dor':'' ,'expiry_date':'','type':''}
                serial_no =serial_no +1
                my_dict['type'] = i.type
                my_dict['s_no'] = serial_no
                my_dict['name'] = i.name
                my_dict['dep/degree'] = i.student_id.degree+ " group : " + str(i.student_id.group)
                my_dict['dor'] = i.dor
                my_dict['expiry_date'] = i.expiry_date
                res.append(my_dict) 
        elif form['patron'] == 'employee':
            patron_ids = self.pool.get('lms.patron.registration').search(self.cr ,self.uid ,[('type','=','employee')])
            for i in self.pool.get('lms.patron.registration').browse(self.cr ,self.uid ,patron_ids):
                my_dict = {'s_no':'' ,'name':'' ,'dep/degree':''  ,'dor':'' ,'expiry_date':'','type':''}
                serial_no =serial_no +1
                my_dict['type'] = i.type
                my_dict['s_no'] = serial_no
                my_dict['name'] = i.employee_id.name
                my_dict['dep/degree'] = i.employee_id.department_name
                my_dict['dor'] = i.dor
                my_dict['expiry_date'] = i.expiry_date 
                res.append(my_dict) 
        else:
            patron_ids = self.pool.get('lms.patron.registration').search(self.cr ,self.uid ,[('id','!=',None)])
            for i in self.pool.get('lms.patron.registration').browse(self.cr ,self.uid ,patron_ids):
                my_dict = {'s_no':'' ,'name':'' ,'dep/degree':''  ,'dor':'' ,'expiry_date':'' ,'type':''}
                serial_no =serial_no +1
                my_dict['type'] = i.type
                my_dict['s_no'] = serial_no
                if i.type == 'student':
                    my_dict['name'] = i.name
                    my_dict['dep/degree'] = i.student_id.degree+ " group : " + str(i.student_id.group)
                else:
                    my_dict['name'] = i.employee_id.name
                    my_dict['dep/degree'] = i.employee_id.department_name 
                my_dict['dor'] = i.dor
                my_dict['expiry_date'] = i.expiry_date 
                res.append(my_dict)
        return res

    
report_sxw.report_sxw('report.show_patrons','lms.patron.registration', 
                      '/addons/lms/report/report_show_patrons_view.rml',

                      parser=report_show_patrons,
                      header=True)