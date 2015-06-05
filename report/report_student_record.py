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
            resource_id_list = pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr, self.uid,[('catagory_id','=',catagory)])
            print "resource_id_list=",resource_id_list

                
            for c in pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr,self.uid,resource_id_list):
                my_dict = {'name':'' ,'dop':'' ,'acc_no':{} }
                my_dict['name'] = c.name
                my_dict['dop'] = c.dop
                #my_dict['acc_no'] = pooler.get_pool(self.cr.dbname).get('lms.cataloge').browse(self.cr,self.uid,acc_no_of_catagory_ids[0]).accession_no 
                print "name=",my_dict['name'] ,"dop",my_dict['dop'],"\n----------------"
                i=0
                j=0
                while i<len(resource_id_list):
                    acc_no_of_catagory_ids = pooler.get_pool(self.cr.dbname).get('lms.cataloge').search(self.cr, self.uid,[('resource_no','=',resource_id_list[i])])
                    print "acc_no_of_catagory_ids=",acc_no_of_catagory_ids
                    for rec in pooler.get_pool(self.cr.dbname).get('lms.cataloge').browse(self.cr,self.uid,acc_no_of_catagory_ids):
                        print "acc_no[",j,"]=",rec.accession_no
                        print "acc_no[",j,"]=",rec.resource_no.name
                        my_dict['acc_no'][j] = rec.accession_no
                        print "my_dict['acc_no'][",j,"]=",my_dict['acc_no'][i]
                        j=j+1
                    i=i+1 
                result.append(my_dict)
                i=0
                while i<len(my_dict['acc_no']):
                    print "mydict[acc_no][",i,"]=",my_dict['acc_no'][i]
                    i=i+1
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