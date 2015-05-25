import pooler
import time
import rml_parse
from report import report_sxw
import netsvc

class report_student_record(rml_parse.rml_parse):
    
        def __init__(self, cr, uid, name, context):
            super(report_student_record, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({ 'get_student':self.get_student })
                       
        def get_student(self,form):
            catagory = pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr,self.uid,form['title']).title 
            #make sure to put the argument in form['student_name'] 
            #the variable in the wizard that have relationship with the actuall(sim.py) class
            print "received value=",catagory
            return catagory   
        
report_sxw.report_sxw('report.student_record','lms.resource', 
                      '/addons/cms_library/report/student_report_view.rml',
                      parser=report_student_record,
                      header=True)

#report_sxw.report_sxw(report.here you will write the name that you have defined in the report declaration
#(i.e name=student_record) in wizard report defination of xml and then,class name of you actual class in sim module,
#then its path of you rml file and it should be in report folder,the name of you class of report,header)