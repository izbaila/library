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
            resource_ids = pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr, self.uid,[('catagory_id','=',catagory)])
  
            for resource_id in resource_ids:
                cataloge_ids = pooler.get_pool(self.cr.dbname).get('lms.cataloge').search(self.cr, self.uid,[('resource_no','=',resource_id)])
                cataloge_objs = pooler.get_pool(self.cr.dbname).get('lms.cataloge').browse(self.cr,self.uid,cataloge_ids)
                
                i = 0
                my_dict = {}
                
                my_dict = {'name_1':'' ,'dop_1':'' ,'acc_no_1':'','name_2':'' ,'dop_2':'' ,'acc_no_2':'','name_3':'' ,'dop_3':'' ,'acc_no_3':'' }
                for cataloge_obj in cataloge_objs:
                    my_dict['name_' + str((i%3)+1)] = cataloge_obj.resource_no.name
                    my_dict['dop_' + str((i%3)+1)] = cataloge_obj.resource_no.dop
                    my_dict['acc_no_' + str((i%3)+1)] = cataloge_obj.accession_no
                    
                    if (i+1) % 3 == 0:
                        result.append(my_dict)
                        my_dict = {'name_1':'' ,'dop_1':'' ,'acc_no_1':'','name_2':'' ,'dop_2':'' ,'acc_no_2':'','name_3':'' ,'dop_3':'' ,'acc_no_3':'' }
                    i = i + 1
                
                if (i-1) % 3 != 0:
                    result.append(my_dict)

                return result
   
        def get_catagory(self,form):
            catagory = pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr,self.uid,form['catagory']).catagory_id.type
            return catagory
        
report_sxw.report_sxw('report.student_record',
                      'lms.resource', 
                      '/addons/lms/report/student_report_view.rml',
                      parser=report_student_record,
                      header=True)
