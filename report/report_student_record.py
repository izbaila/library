import pooler
import time
import rml_parse
from report import report_sxw
import netsvc

class report_student_record(rml_parse.rml_parse):
    
        def __init__(self, cr, uid, name, context):
            super(report_student_record, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({ 'get_resource':self.get_resource,
                                      'get_catagory': self.get_catagory,
                                    })
                       
        def get_resource(self,form):
            result = []
            catagory = form['catagory']
            catagory_id_list = pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr, self.uid,[('catagory_id','=',catagory)])
            print "catagory_id_list=",catagory_id_list
            i=0
            while i<len(catagory_id_list):
                acc_no_of_catagory_ids = pooler.get_pool(self.cr.dbname).get('lms.cataloge').search(self.cr, self.uid,[('resource_no','=',catagory_id_list[i])])
                print "acc_no_of_catagory_ids=",acc_no_of_catagory_ids
                for rec in pooler.get_pool(self.cr.dbname).get('lms.cataloge').browse(self.cr,self.uid,acc_no_of_catagory_ids):
                    print "acc_no[",i,"]=",rec.accession_no
                    print "acc_no[",i,"]=",rec.resource_no.name
                i=i+1 
                
            for c in pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr,self.uid,catagory_id_list):
                my_dict = {'name':'' ,'dop':'' ,'acc_no':'' }
                my_dict['name'] = c.name
                my_dict['dop'] = c.dop
                my_dict['acc_no'] = pooler.get_pool(self.cr.dbname).get('lms.cataloge').browse(self.cr,self.uid,acc_no_of_catagory_ids[0]).accession_no 
                result.append(my_dict)
            return result

        def get_catagory(self,form):
            catagory = pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr,self.uid,form['catagory']).catagory_id.type
            return catagory
        
report_sxw.report_sxw('report.student_record',
                      'lms.resource', 
                      '/addons/cms_library/report/spine.rml',
                      parser=report_student_record,
                      header=True)

#report_sxw.report_sxw(report.here you will write the name that you have defined in the report declaration
#(i.e name=student_record) in wizard report defination of xml and then,class name of you actual class in sim module,
#then its path of you rml file and it should be in report folder,the name of you class of report,header)