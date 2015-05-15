import time
import netsvc
import osv
import datetime
import pooler
from osv import fields, osv, orm 

class lms_hr_employee(osv.osv):
    _name = "lms.hr.employee"
    _description = "it form relationship with patron registration"
    _columns = {
        'name' : fields.char('Teacher Name' ,size=256, required=True),
        'department_name' : fields.char('Department Name' ,size=256),
        }
lms_hr_employee()

class lms_entryregis(osv.osv):
    _name = "lms.entryregis"
    _description = "it form relationship with patron registration"
    _columns = {
        'name' : fields.char('Student Name' ,size=256, required=True),
        'father_name' : fields.char('Father Name' ,size=256),
        }   
lms_entryregis()

class lms_patron_registration(osv.osv):
  
    #functions for buttons
    def set_registration(self, cr, uid, ids,context):
        #this function is for changing the state of the button to waiting state
        self.write( cr, uid, ids, {'state' : 'Waiting_Approve'})
        return True
    
    def cancel(self, cr, uid, ids,context):
        #this function is for changing the state of the button to waiting state
        self.write( cr, uid, ids, {'state' : 'Cancelled' })
        return True
 
    def approve_registration(self, cr, uid, ids,context={}):
        #this function is for setting values of the variables
        self.write(cr,uid,ids,{'state' : 'Active'})
        return True
        
    
    def show(self, cr, uid, ids, fields, data, context):  # this function is for combining title and edition
        result = {}
        ans = self.browse(cr, uid, ids)
        for checking_detail in ans:
            if checking_detail.type == 'student':
                result[checking_detail.id] = str(checking_detail.student_id.name) +" S/O "+str(checking_detail.student_id.father_name)
            elif checking_detail.type == 'employee':
                result[checking_detail.id] = str(checking_detail.employee_id.name)+ " from " +str(checking_detail.employee_id.department_name)+" department"
            return result
        
    _name = "lms.patron.registration"
    _description = "this class is use for patrons registrations with library "
    _columns = {
        'student_id' : fields.many2one('lms.entryregis', 'Student Name'),
        'employee_id' : fields.many2one('lms.hr.employee','Employee Name'),
        'dor' : fields.date('Date of registration'),
        'expiry_date' : fields.date('Expiry Date'),
        'type' : fields.selection([('employee','Employee'),('student','Student')],'Type', required= True),
        'name' : fields.function(show, method=True, string='Full name', type='char', size=128),
        'state' : fields.selection([('Draft','Draft'),('Active','Active'),('Pass out','Pass out'),('Cancelled','Cancelled'),('Waiting_Approve','Waiting Approve')],'Status'),
        }
    _defaults = {
        'state' : lambda *a : 'Draft',
        'type' : lambda *a : 'student',
        'dor': lambda *a: datetime.date.today().strftime('%Y-%m-%d'),
        }
    
lms_patron_registration()

class lms_publisher(osv.osv):
    _name = "lms.publisher"
    _decription = "it forms relation with resource"
    _rec_name = 'name'
    _columns = {
        'name' : fields.char('Publisher Name' ,size=256 ,required=True),
        'description' : fields.char('Publisher Description' ,size=256),
        }
lms_publisher()

class lms_categories(osv.osv):
    _name = "lms.categories"
    _description = "this class is for maintaining the record for categories"
    _rec_name= 'type'
    _columns = {
        'name' : fields.char('Category Name' , size=256, required=True),
        'description' : fields.char('Category Description' , size=256),
        'type' : fields.selection([('book','book'),('magazine','Magazine'),('journal','Journal'),('audio/visual','Audio/Visual'),('newspaper','Newspaper')],'Type', required= True)
              }
lms_categories()

class lms_subjects(osv.osv):
    _name = "lms.subjects"
    _description = "this class is use to maintain the subject that are in library"
    _rec_name = 'name'
    _columns = {
        'name' : fields.char('Subject Name' , size=256, required=True),
        'description' : fields.char('Subject Description' , size=256)
            }
lms_subjects()

class lms_author(osv.osv):
    _name = "lms.author"
    _description = "this class is use to maintain the information about author"
    _rec_name ='name'
    _columns = {
        'name' : fields.char('Author Name' , size=256, required=True),
        'description' : fields.char('Author Description' , size=256),
        'author_image' : fields.binary('Image'),
            }
lms_author()

class lms_edition(osv.osv):
    _name = "lms.edition"
    _description = "this form relation with resource"
    _columns = {
        'name' : fields.char('Edition Name', size=256, required=True),
        'description' : fields.char('Edition Description', size=256)
        }
lms_edition()

class lms_rack(osv.osv):
    _name = "lms.rack"
    _description = "it forms relation with subject"
    _columns = {
        'name' : fields.char('Rack Name' ,size=256, required=True),
        'rack_no' : fields.integer('Rack Number' , required=True),
        'rack_location' : fields.char('Rack Location' ,size=256),
        'subject_name' : fields.many2one('lms.subjects', 'Subject Name')
    }
lms_rack()    

class lms_resource(osv.osv):
    
    def combine(self, cr, uid, ids, fields, arg, context):  # this function is for combining title and edition
        result = {}
        ans = self.browse(cr, uid, ids)
        for checking_detail in ans:
            result[checking_detail.id] = str(checking_detail.edition.name) + " " + str( checking_detail.title)
        return result
    
    _name = "lms.resource"
    _description = "this module contains the information of resource"
    _rec_name = 'name'
    _columns = {
        'name' : fields.function(combine, method=True, string='Resource', type='char', size=128),
        'description' : fields.char('Resource Description', size=256),
        'language_id' : fields.selection([('english','English'),('urdu','Urdu'),('arabic','Arabic')],'Language', required= True),
        'subject_id' : fields.many2one('lms.subjects' , 'Subject', required= True),
        'catagory_id' : fields.many2one('lms.categories' , 'Catagory', required= True),
        'publisher' : fields.many2many('lms.publisher', 'p_name','attr_name','testing_var', 'Publisher', required= True),
        'barcode' : fields.char('Barcode', size=256),
        'serial_no' : fields.char('Serial No', size=256),
        'isbn' : fields.char('ISBN', size=256),
        'title' : fields.char('Title', size=256, required= True),
        'additional_information' : fields.char('Additional Information', size=256),
        'translator' : fields.char('Translator', size=256),
        'source' : fields.char('Source', size=256),
        'pages' : fields.integer('Pages'),
        'volume_no' : fields.char('Volume no', size=256),
        'dop' : fields.date('Date of Publication', size=256, required= True),
        'annual_cost' : fields.integer('Annual Cost'),
        'unit_cost' : fields.integer('Unit Cost', required= True),
        'binding' : fields.char('Binding', size=256),
        'quantity' : fields.char('Quantity', size=256, required= True),
        'accompaning_material' : fields.char('Accompaning Material', size=256),
        'not_catalogue' : fields.boolean('Catalouge', required= True),
        'author_id' : fields.many2many ('lms.author' , 'name' , 'author_name' , 'r_name' , 'Author', required= True),
        'edition' : fields.many2one('lms.edition', 'Edition', required=True),
        'subtitle' :fields.char('Subtitle' ,size=256),
        'bill_no' :fields.char('Bill Number' ,size=256, required= True),
        'major_type' : fields.selection([('magazine','Magazine'),('journal','Journal')],'Magazine/Journal'),
        'frequency' :fields.char('Frequency' ,size=256),
        'date_np' :fields.date('Newspaper Date'),
        'newspaper_image' :fields.binary('Newspapers Image / Clip Image'),
        'type_of_medium' :fields.char('Type Of Medium' ,size=256),
        'format' :fields.selection([('mp3','.Mp3'),('mp4','.Mp4'),('avi','.Avi'),('flv','.Flv'),('wma','.Wma')],'Format'),
        'bill_date' :fields.date('Bill Date'),
        'bill_amount' :fields.integer('Bill Amount'),
        'suplier_vender' :fields.char('Suplier / Vender' ,size=256),
        'field_of_specialization' : fields.char('Field Of Specialization' ,size=256),
        'program' : fields.char('Program' ,size=256),
        'newspaper' : fields.char('Newspaper' ,size=256)
            } 
    _sql_constraints = [
            ('name', 'unique (name)',  'Duplicate values not allowed !'),
            ('barcode', 'unique(barcode)', 'Duplication of barcode not allowed')
            ]
lms_resource()

class lms_cataloge(osv.osv):
    
    _name = "lms.cataloge"
    _description = "it forms relation with resource for cataloguing purpose"
    _columns = {
        'name' : fields.char('Cataloge Name', size=256,required = True ),
        'resource_no' : fields.many2one('lms.resource' ,'Resource Name',required = True ),
        'rack_no' : fields.many2one('lms.rack','Rack number',required = True),
        'issued_allowed_notallowed' : fields.boolean('Issuable'),
        'accession_no' : fields.char("Accession Number" ,size=256 ,required = True),
        'name' : fields.char('Cataloge Name', size=256),
        'resource_no' : fields.many2one('lms.resource' ,'Resource Number',required = True ),
        'rack_no' : fields.many2one('lms.rack','Rack Number',required = True),
        'issued_allowed_notallowed' : fields.boolean('Issue-Able'),
        'accession_no' : fields.char("Accession Number" ,size=256 ,required = True),
#       'state' : fields.selection([('Draft','Draft'),('Available','Available'),('Wareout','Wareout'),('Issued','Issued'),],'State'),
        'active_deactive' : fields.boolean('Active/Deactive'),
        'purchase_date' : fields.date('Purchase Date'),
        'wareout_date' : fields.date('Wareout Date'),
        'cataloge_date' : fields.date('Cataloge date'),
        }
    _defaults = {
 #       'state' : lambda *a : 'Draft',
        'active_deactive' : lambda *a : True,
        }
lms_cataloge()

class lms_cataloging(osv.osv):
    
    def continue_cataloging(self, cr, uid, ids,context):
        self.write( cr, uid, ids, {'state' : 'Confirm' } )
        for checker in self.pool.get('lms.cataloging').browse(cr,uid,ids):
            no_of_catalogue = checker.no_of_cataloge
            counter=no_of_catalogue
        if  no_of_catalogue <=0:
            raise osv.except_osv(('Error'), ('Further cataloging is not possible no of catalog has to be greater than one '))
        while counter!=0:
            counter=counter-1
            acc_obj = self.pool.get('lms.cataloging')
            acc_no = acc_obj.generate_accession_num(cr,uid,ids)
            self.pool.get('lms.cataloge.line').create(cr, uid, {'resource_id': checker.resource_no.id ,'rack_no':checker.rack_no.id,'acc_no':acc_no,'purchase_date':checker.purchase_date,'name':ids[0]})            
        return True
    
    def generate_accession_num(self,cr,uid,ids):
        for checker in  self.browse(cr, uid, ids):
            cat_id = checker.resource_no.catagory_id.id
            sql = """SELECT count(*) FROM lms_cataloge_line INNER JOIN lms_resource 
                    ON lms_resource.id = lms_cataloge_line.resource_id
                    WHERE lms_resource.catagory_id = """+str(cat_id)+""""""
            cr.execute(sql)
            quantity=0
            quantity = cr.fetchone()
            if quantity:
                quantity = quantity[0] + 1
                #cat_name is use to fetch the catagory type
                ac_no = checker.resource_no.catagory_id.name[:1].upper() + "-"+ str(quantity)
            return ac_no
  
    def confirm_cataloging(self, cr, uid, ids,context):
        ids = self.pool.get('lms.cataloge.line').search(cr, uid,[('name','=',ids[0])])
        for checker in self.pool.get('lms.cataloge.line').browse(cr,uid,ids):
            self.pool.get('lms.cataloge').create(cr, uid,{'name':checker.name.name,'accession_no':checker.acc_no,'resource_no':checker.resource_id.id,'rack_no':checker.rack_no.id,'purchase_date':checker.purchase_date})
        return True

    def reset_cataloging(self, cr, uid, ids,context):
        list_of_ids = self.pool.get('lms.cataloge.line').search(cr, uid,[('name','=',ids[0])])
        if list_of_ids != 0:
            self.pool.get('lms.cataloge.line').unlink(cr,uid,list_of_ids)
            return True
        return None
    
    _name = "lms.cataloging"
    _description = "it forms relation with resource for cataloging purpose"
    _rec_name = 'name'
    _columns = {
        'name' : fields.char('Cataloge Name', size=256),
        'resource_no' : fields.many2one('lms.resource' ,'Resource Name',required = True ),
        'rack_no' : fields.many2one('lms.rack','Rack Number',required = True),
        'cataloge_date' : fields.date('Cataloge Date', size=256 ,required = True),
        'no_of_cataloge' : fields.integer('No Of Cataloge'),
        'state' : fields.selection([('Draft','Draft'),('Confirm','Confirm'),],'State',required = True),
        'catalog_id' : fields.one2many('lms.cataloge.line','name','Cataloge Id'),
        'accession_no' :fields.char('Accession Number' ,size=256),
        'purchase_date' : fields.date('Purchase Date', size=256),
        }
    _defaults = {
        'state' : lambda *a : 'Draft',
        'cataloge_date' : lambda *a: datetime.date.today().strftime('%Y-%m-%d'),
         }
     
lms_cataloging()

class lms_cataloge_lines(osv.osv):
     
    _name = "lms.cataloge.line"
    _description = "it form the cataloges"
    _columns = {
        'name' : fields.many2one('lms.cataloging','Cataloging'),
        'resource_id' : fields.many2one('lms.resource','Resource Number'),
        'rack_no' : fields.many2one('lms.rack' ,'Rack Number'),
        'acc_no' : fields.char('Accession Number' ,size=256),
        'purchase_date' : fields.date('Purchase Date'),
        }
lms_cataloge_lines()
