import os 
import re 

from django.db import models
from django.contrib.auth.models import User

from myproject.settings import UPLOAD_DIR

# Create your models here.
TAB_SHAPE_CHOICES = (
		('C','C'),
		('Z','Z'),
		('I','I'),
		('none','none'),
);

PACK_CONNECTION_CHOICES = (
		('W','Wires'),
		('WC','Wire & Connector'),
		('PCBS','Two Pin Through Hole'),
		('PCBD','Three Pin Through Hole'),
		('TP','Terminal Pin'),
		('ST','Surface Mount Tabs(in the same direction)'),
		('STO','Surface Mount Tabs(in the opposite direction)'),
		('FM','FM'),
		('RT','Ring Tab'),
		('CD','Axial Leads/Contact Discs'),
		('SP','SP'),
		('BC','BC'),
);

PACK_INSULATION_COICES = (
		('BE','BE'),
		('PC','Plastic Casing'),
		('SC','Snap On Casing'),
		('S','Shrink Wrap'),
		('IP','IP'),
		('MC','Metal Casing'),
);

PACK_CONFIGURATION_COICES = (
		('C','C'),
		('L','L'),
		('LM','LM'),
		('LS','LS'),
		('SK','SK'),
		('SR','SR'),
		('TL','TL'),
);

NEW_OR_EXISTING_CHOICES = (
		('N','New'),
		('E','Existing'),
);

PROJECT_STATUS_CHOICES = (
		('dead','dead'),
		('open','open'),
		('continuing','continuing'),
		('spot business','spot business'),
);

CONTACT_STATUS_CHOICES = (
		('VMI Employee','VMI Employee'),
		('Varta Rep','Varta Rep'),
		('Distributor','Distributor'),
		('Master Distributor','Master Distributor'),
);

DIVISION_CHOICES = (
		('PPS','PPS'),
		('Classic','Classic'),
		('Retail','Retail')
);

REGION_CHOICES = (
		('E','East'),
		('W','West'),
		('C','Central'),
		('H','House/International'),
);

TYPE_CHOICES = (
		('None','None'),
		('Li_Ion','Li-Ion'),
		('Ni_MH','Ni-MH'),
		('Primary','Primary'),
)

CHEMISTRY_CHOICES = (
		('None','None'),
		('LPP','LPP'),
		('LIP','LIP'),
		('LIC','LIC'),
		('NMC','Ni-MH Cylindrical'),
		('NMB','Ni-MH Button'),
		('LiSOCl2','Li-SOCl2'),
		('LiMnO2B','Li-MnO2 Button'),
		('LiMnO2C','Li-MnO2 Cylindrical'),
		('Alkaline','Alkaline'),
		('AgO2','Watch Battery'),
		('HearingAid','Hearing Aid Battery'),
)

MARKET_SEGMENT_CHOICES = (
		('Medical','Medical'),
		('Military','Military'),
		('Consumer','Consumer'),
		('Server','Server'),
		('Automotive','Automotive'),
);

STATE_CHOICES = (
		('AL','Alabama'),
		('AK','Alaska'),
		('AS','American Somoa'),
		('AZ','Arizona'),
		('AR','Arkansas'),
		('CA','California'),
		('CO','Colorado'),
		('CT','Connecticut'),
		('DE','Deleware'),
		('DC','District of Columbia'),
		('FM','Federated States of Micronesia'),
		('FL','Florida'),
		('GA','Georgia'),
		('GU','Guam'),
		('HI','Hawaii'),
		('ID','Idaho'),
		('IL','Illinois'),
		('IN','Indiana'),
		('IA','Iowa'),
		('KS','Kansas'),
		('KY','Kentucky'),
		('LA','Louisiana'),
		('ME','Maine'),
		('MH','Marshall Islands'),
		('MD','Maryland'),
		('MA','Massachusetts'),
		('MI','Michigan'),
		('MN','Minnesota'),
		('MS','Mississippi'),
		('MO','Missouri'),
		('MT','Montana'),
		('NE','Nebraska'),
		('NV','Nevada'),
		('NH','New Hampshire'),
		('NJ','New Jersey'),
		('NM','New Mexico'),
		('NY','New York'),
		('NC','North Carolina'),
		('ND','North Dakota'),
		('MP','Northern Mariana Islands'),
		('OH','Ohio'),
		('OK','Oklahoma'),
		('OR','Oregon'),
		('PW','Palau'),
		('PA','Pennsylvania'),
		('PR','Puerto Rico'),
		('RI','Rhode Island'),
		('SC','South Carolina'),
		('SD','South Dakota'),
		('TN','Tennessee'),
		('TX','Texas'),
		('UT','Utah'),
		('VT','Vermont'),
		('VI','Virgin Islands'),
		('VA','Virginia'),
		('WA','Washington'),
		('WV','West Virginia'),
		('WI','Wisconsin'),		
		('AB','Alberta'),
		('BC','British Columbia'),
		('MB','Manitoba'),
		('NB','New Brunswick'),
		('NL','New Foundland and Labrador'),
		('NT','Norther Territory'),
		('NS','Nova Scotia'),
		('NU','Nunavut'),
		('ON','Ontario'),
		('PE','Prince Edward Island'),
		('QC','Quebec'),
		('SK','Saskatchewan'),
		('YT','Yukon'),
		('AG','Aguascalientes'),	
		('BJ','Baja California'),
		('BS','Baja California Sur'),
		('CP','Campeche'),
		('CH','Chiapas'),
		('CI','Chihuahua'),
		('CU','Coahuila'),
		('CL','Colima'),
		('DF','Distrito Federal'),
		('DG','Durango'),
		('GJ','Guanajuato'),
		('HG','Hidalgo'),
		('JA','Jalisco'),
		('EM','Mexico'),
		('MH','Michoacan'),
		('MR','Morelos'),
		('NA','Nayarit'),
		('NL','Nuevo Leon'),
		('OA','Oaxaca'),
		('PU','Puebla'),
		('QA','Queretaro'),
		('QR','Quintana Roo'),
		('SL','San Luis Potosi'),	
		('SO','Sonora'),
		('TA','Tabasco'),
		('TM','Tamaulipas'),
		('TL','Tlaxcala'),
		('VZ','Veracruz'),
		('YC','Yucatan'),
		('ZT','Zacatecas'),
);

class Contact(models.Model):
	"""
	All VMI employees, Reps, Customers, etc. will be contacts.  VMI employees will be Contacts linked to User accounts. 
	
	unicode allows for proper display in the admin
	create increments a 7 digit ID number by 1 unless it is the first contact ever created then it is assigned
		1,000,000
	clean_phone converts phone numbers as strings with spaces and other symbols into integers
	"""
	user = models.ForeignKey(User, unique = True, blank = True, null = True)
	status = models.CharField("Contact Status", 
			choices = CONTACT_STATUS_CHOICES, 
			max_length = 20, 
			null = True, 
			blank = True,
			)
	firstname = models.CharField("First Name", max_length = 48, null = True, blank = True)
	lastname = models.CharField("Last Name", max_length = 48, null = True, blank = True)
	company = models.CharField("Company", max_length = 48, null = True, blank = True)
	title = models.CharField("Job Title", max_length = 48, null = True, blank = True)
	cell = models.DecimalField("Cell Phone Number", max_digits = 10, decimal_places = 0, null = True, blank = True)
	landline = models.DecimalField("Phone Number", max_digits = 10,decimal_places = 0,  null = True, blank = True)
	fax = models.DecimalField("Fax Number", max_digits = 10, decimal_places = 0, null = True, blank = True)
	email = models.EmailField("Email Address", max_length = 128, null = True, blank = True)
	primary_address_line1 = models.CharField("Primary Address Line 1", max_length = 30, null = True, blank = True)
	primary_address_line2 = models.CharField("Primary Address Line 2", max_length = 30, null = True, blank = True)
	primary_city = models.CharField("City", max_length = 30, null = True, blank = True)
	primary_state = models.CharField("State", choices = STATE_CHOICES, max_length = 2, null = True, blank = True)
	primary_post_code = models.CharField("Post Code", max_length = 10, null = True, blank = True)
	secondary_address_line1 = models.CharField("Secondary Address Line1", max_length = 30, null = True, blank = True)
	secondary_address_line2 = models.CharField("Secondary Address Line2", max_length = 30, null = True, blank = True)
	secondary_city = models.CharField("City", max_length = 30, null = True, blank = True)
	secondary_state = models.CharField("State", choices = STATE_CHOICES, max_length = 2, null = True, blank = True)
	secondary_post_code = models.CharField("Post Code", max_length = 10, null = True, blank = True)

	class Meta:
		ordering = ('lastname','firstname')

	def __unicode__(self):
        	return self.firstname 

	def save(self, new):
		"""
		Saves a new contact to the database if
		1) new == True and there is not already a Contact in the database with the same customer and battery info
		Updates an existing contact if
		2) new == False
		FOR NOW I WILL RELY ON GET_OBJECT_OR_404 IN VIEWS TO MAKE SURE THAT WHEN UPDATING A PROJECT, THAT PROJECT ACTUALLY EXISTS 
		"""
		if new == True:
			try:
				obj = Contact.objects.get(
					firstname = self.firstname,
					lastname = self.lastname,
					company = self.company,
					email = self.email
					)
				saved = False
				self.id = obj.id
			except Contact.DoesNotExist:
				super(Contact, self).save()
				saved = True
			return self, saved
		else:
			try:
				assert(self.id)
				super(Contact, self).save()
				saved = True
				return self, saved
			except AssertionError:
				saved = False
				return self, saved
			
class Battery(models.Model):
	"""
	This will represent the bare cell that makes up the PACK
	"""
	datasheet =  models.FileField("Data Sheet", upload_to = "uploads/", max_length = 20, null = True, blank = True )
	type_description = models.CharField("type description", max_length = 20, null = True, blank = True )
	type_number = models.DecimalField("Type#", max_digits = 5, decimal_places = 0, null = True, blank = True )
	type = models.CharField("type", choices = TYPE_CHOICES, max_length = 20, null = True, blank = True )
	chemistry = models.CharField("chemistry", choices = CHEMISTRY_CHOICES, max_length = 20, null = True, blank = True )
	capacity = models.DecimalField("Capacity", max_digits = 6, decimal_places = 0, null = True, blank = True )
	voltage = models.DecimalField("Voltage", max_digits = 4, decimal_places = 2, null = True, blank = True )
	max_cont = models.DecimalField("Max Continuous Discharge Rate", max_digits = 5, decimal_places = 0, null = True, blank = True )
	max_pulse = models.DecimalField("Max Pulsed Discharge Rate", max_digits = 5, decimal_places = 0, null = True, blank = True )
	min_storage_temp = models.DecimalField("Min Storage Temp", max_digits = 2, decimal_places = 0, null = True, blank = True )
	max_storage_temp  = models.DecimalField("Max Storage Temp", max_digits = 2, decimal_places = 0, null = True, blank = True )
	min_charge_temp = models.DecimalField("Min Charge Temp", max_digits = 2, decimal_places = 0, null = True, blank = True )
	max_charge_temp = models.DecimalField("Max Charge Temp", max_digits = 2, decimal_places = 0, null = True, blank = True )
	min_discharge_temp = models.DecimalField("Min Discharge Temp", max_digits = 2, decimal_places = 0, null = True, blank = True )
	max_discharge_temp = models.DecimalField("Max Discharge Temp", max_digits = 2, decimal_places = 0, null = True, blank = True )
	volume = models.DecimalField("Volume", max_digits = 2, decimal_places = 0, null = True, blank = True )
	weight = models.DecimalField("Weight", max_digits = 2, decimal_places = 0, null = True, blank = True )
	discontinued = models.NullBooleanField("Discontinued", default = False, blank = True )

	def __unicode__(self):
        	return str(self.type_description)

	def save(self):
		"""
		If an edited battery changes the type_number, the old datasheet must be renamed
		If a new battery has the same type_number as an existing battery, it should not be saved
		"""
		try:
			obj = Battery.objects.get(
				id = self.id
				)
			if self.type_number != obj.type_number:
				if re.match(r'^\d{4}$', str(obj.type_number)):
					old_datasheet = os.path.join(UPLOAD_DIR,'0'+str(obj.type_number)+'.pdf')
				if re.match(r'^\d{5}$', str(obj.type_number)):
					old_datasheet = os.path.join(UPLOAD_DIR,str(obj.type_number)+'.pdf')
				if re.match(r'^\d{4}$', str(self.type_number)):
					new_datasheet = os.path.join(UPLOAD_DIR,'0'+str(self.type_number)+'.pdf')
				if re.match(r'^\d{5}$', str(self.type_number)):
					new_datasheet = os.path.join(UPLOAD_DIR,str(self.type_number)+'.pdf')
				os.rename(old_datasheet, new_datasheet)
			super(Battery, self).save()
		except Battery.DoesNotExist:
			try:
				obj = Battery.objects.get(
					type_number = self.type_number
					)
			except Battery.DoesNotExist:
				super(Battery, self).save()
		return self

	def save_datasheet(self, datasheet):
		if re.match(r'^\d{4}$', str(self.type_number)):
			self.datasheet.save('0'+str(self.type_number)+'.pdf', datasheet)
		elif re.match(r'^\d{5}$', str(self.type_number)): 
			self.datasheet.save(str(self.type_number)+'.pdf', datasheet)
		return self
			
class Cylindrical(Battery):
	diameter = models.DecimalField("Diameter", max_digits = 2, decimal_places = 0, null = True, blank = True )
	height = models.DecimalField("Height", max_digits = 2, decimal_places = 0, null = True, blank = True )

class Prismatic(Battery):
	length = models.DecimalField("Length", max_digits = 2, decimal_places = 0, null = True, blank = True )
	width = models.DecimalField("Width", max_digits = 2, decimal_places = 0, null = True, blank = True )
	height = models.DecimalField("Height", max_digits = 2, decimal_places = 0, null = True, blank = True )

class Pack(models.Model):
	"""
	This will represent the battery PACK/ VKB#
	"""
	battery = models.ForeignKey(Battery, null = True, blank = True)
	drawing =  models.FileField("Drawing", upload_to = "uploads/", max_length = 20, null = True, blank = True )
	drawing_number = models.DecimalField("Drawing#", max_digits = 6, decimal_places = 0, null = True, blank = True )
	vkb_number = models.DecimalField("VKB#", max_digits = 11, decimal_places = 0, null = True, blank = True )
	type = models.CharField("type", choices = TYPE_CHOICES, max_length = 20, null = True, blank = True )
	chemistry = models.CharField("chemistry", choices = CHEMISTRY_CHOICES, max_length = 20, null = True, blank = True )
	series_cells = models.DecimalField("Cells in Series", max_digits = 2, decimal_places = 0, null = True, blank = True )
	parallel_cells = models.DecimalField("Cells in Parallel", max_digits = 2, decimal_places = 0, null = True, blank = True )
	connection = models.CharField("Connection", choices = PACK_CONNECTION_CHOICES, max_length = 2, null = True, blank = True)
	insulation = models.CharField("Insulation", choices = PACK_INSULATION_COICES, max_length = 2, null = True, blank = True)
	configuration =  models.CharField("Configuration", choices = PACK_CONFIGURATION_COICES, max_length = 2, null = True, blank = True)
	stacks = models.DecimalField("Stacks", max_digits = 2, decimal_places = 0, null = True, blank = True )
	rows = models.DecimalField("Rows", max_digits = 2, decimal_places = 0, null = True, blank = True )
	capacity = models.DecimalField("Capacity", max_digits = 6, decimal_places = 0, null = True, blank = True )
	voltage = models.DecimalField("Voltage", max_digits = 4, decimal_places = 2, null = True, blank = True )
	max_cont = models.DecimalField("Max Continuous Discharge Rate", max_digits = 5, decimal_places = 0, null = True, blank = True )
	max_pulse = models.DecimalField("Max Pulsed Discharge Rate", max_digits = 5, decimal_places = 0, null = True, blank = True )
	mempac = models.NullBooleanField("Mempac", default = False, blank = True)
	slf = models.NullBooleanField("SLF", default = False, blank = True)
	discontinued = models.NullBooleanField("Discontinued", default = False, blank = True )
	
	def __unicode__(self):
        	return str(self.vkb_number)
class Wire(Pack):
	wire_length = models.DecimalField("Rows", max_digits = 3, decimal_places = 0, null = True, blank = True )
	connector = models.CharField("Connector", max_length = 20, null = True, blank = True )
	connector_pins = models.DecimalField("Number of Pins on Connector", max_digits = 2, decimal_places = 0, null = True, blank = True )

class Pin(Pack):
	thickness = models.DecimalField("Thickness", max_digits = 2, decimal_places = 2, null = True, blank = True )
	length = models.DecimalField("Length", max_digits = 3, decimal_places = 0, null = True, blank = True )
	width = models.DecimalField("Width", max_digits = 2, decimal_places = 0, null = True, blank = True )
	battery_height = models.DecimalField("Battery Height", max_digits = 2, decimal_places = 0, null = True, blank = True )
	distance_between_positive_pins = models.DecimalField("Distance Between Positive Pins", max_digits = 2, decimal_places = 0, null = True, blank = True )

class AxialLeads(Pack):
	length_before_crimp = models.DecimalField("Length Before Crimp ", max_digits = 3, decimal_places = 0, null = True, blank = True )
	length_after_crimp = models.DecimalField("Length After Crimp", max_digits = 3, decimal_places = 0, null = True, blank = True )
	lead_diameter = models.DecimalField("Lead Diameter", max_digits = 2, decimal_places = 2, null = True, blank = True )

class Tab(Pack):
	shape = models.CharField("chemistry", choices = TAB_SHAPE_CHOICES, max_length = 4, null = True, blank = True )
	length = models.DecimalField("Rows", max_digits = 2, decimal_places = 0, null = True, blank = True )
	width = models.DecimalField("Rows", max_digits = 2, decimal_places = 0, null = True, blank = True )
	thickness = models.DecimalField("Thickness", max_digits = 2, decimal_places = 0, null = True, blank = True )
	surface_mount = models.BooleanField("Surface Mount", default = False)

class Project(models.Model):
	"""
	This is most import part of the database
	My entire goal is to make our Projects more manageable
	The contacts, batteries/packs, and documents are all here to support Project Management
	"""
	status = models.CharField("Status", choices = PROJECT_STATUS_CHOICES, max_length = 15)
	division = models.CharField("PPS or OEM", choices = DIVISION_CHOICES, max_length = 7)
	region = models.CharField("Region", choices = REGION_CHOICES, max_length = 1)
	customer = models.CharField("Customer", max_length = 50)
	battery_description = models.CharField("Battery Description", max_length = 100)
	battery_pack = models.ForeignKey(Pack, related_name = "project_pack", null = True, blank = True)
	battery = models.ForeignKey(Battery, related_name = "project_battery", null = True, blank = True)
	market_segment = models.CharField("Market Segment", choices = MARKET_SEGMENT_CHOICES, max_length = 15)
	prototype_verification = models.DateField(null = True, blank = True)
	design_verification = models.DateField(null = True, blank = True)
	manufacturing_verification = models.DateField(null = True, blank = True)
	production_verification = models.DateField(null = True, blank = True)
	end_of_life = models.DateField(null = True, blank = True)
	sales_potential = models.DecimalField("Sales Potential in Dollars", max_digits = 6, decimal_places = 1, null = True, blank = True)
	primary_contact = models.ForeignKey(Contact, related_name = "primary_contact", null = True, blank = True)
	project_manager = models.ForeignKey(Contact, related_name = "project_manager", null = True, blank = True)
	sales_rep = models.ForeignKey(Contact, related_name = "sales rep", null = True, blank = True)
	notes = models.CharField("Notes", max_length = 1000)

	class Meta:
		ordering = ('-sales_potential','customer')

	def __unicode__(self):
        	return self.customer

	def save(self, new):
		"""
		Saves a new project to the database if
		1) new == True and there is not already a Project in the database with the same customer and battery info
		Updates an existing project if
		2) new == False
		FOR NOW I WILL RELY ON GET_OBJECT_OR_404 IN VIEWS TO MAKE SURE THAT WHEN UPDATING A PROJECT, THAT PROJECT ACTUALLY EXISTS 
		"""
		if new == True:
			try:
				obj = Project.objects.get(
					customer = self.customer,
					battery_description = self.battery_description,
					battery_pack = self.battery_pack,
					battery = self.battery,
					)
				saved = False
				self.id = obj.id

			except Project.DoesNotExist:
				super(Project, self).save()
				saved = True
			return self, saved
		else:
			try:
				assert(self.id)
				super(Project, self).save()
				saved = True
				return self, saved
			except AssertionError:
				saved = False
				return self, saved

class Sample(models.Model):
	"""
	VMI Sample Processing Forms must be generated for every sample sent to a customer
	This class will make it easier to generate these forms and allow employees to search through the forms 
	Data which is supplied by the Project or by the user 
	"""
	project = models.ForeignKey(Project, null = True, blank = True)
	author = models.ForeignKey(Contact, related_name = 'sample_author', null = True, blank = True)
	authored_date = models.DateField(null = True, blank = True)
	editor = models.ForeignKey(Contact, related_name = 'sample_editor', null = True, blank = True)
	edited_date = models.DateField(null = True, blank = True)
	ship_to_contact = models.ForeignKey(Contact, related_name = 'ship_to', null = True, blank = True)
	end_user_contact = models.ForeignKey(Contact, related_name = 'end_user', null = True, blank = True)
	date = models.DateField(null = True)
	sample_number = models.DecimalField("Sample#", max_digits = 7, decimal_places = 0, null = True, blank = True)
	battery_description = models.CharField("Battery Description", max_length = 100)
	battery_pack = models.ForeignKey(Pack, related_name = "sample_pack", null = True, blank = True)
	battery = models.ForeignKey(Battery, related_name = "sample_battery", null = True, blank = True)
	ship_to_company = models.CharField("Ship to Company", max_length = 48, null = True, blank = True)
	ship_to_attention = models.CharField("Ship to Attention", max_length = 97, null = True, blank = True)
	ship_to_address_line1 = models.CharField("Ship to Address Line 1", max_length = 30, null = True, blank = True)
	ship_to_address_line2 = models.CharField("Ship to Address Line 2", max_length = 30, null = True, blank = True)
	ship_to_city = models.CharField("Ship to City", max_length = 30, null = True, blank = True)
	ship_to_state = models.CharField("Ship to State", choices = STATE_CHOICES, max_length = 2, null = True, blank = True)
	ship_to_post_code = models.CharField("Ship to Post Code", max_length = 10, null = True, blank = True)
	ship_to_phone = models.DecimalField("Ship to Phone Number", max_digits = 10, decimal_places = 0, null = True, blank = True)
	end_user_company = models.CharField("End User Company", max_length = 48, null = True, blank = True)
	end_user_attention = models.CharField("End User Attention", max_length = 97, null = True, blank = True)
	end_user_address_line1 = models.CharField("End User Address Line 1", max_length = 30, null = True, blank = True)
	end_user_address_line2 = models.CharField("End User Address Line 2", max_length = 30, null = True, blank = True)
	end_user_city = models.CharField("End User City", max_length = 30, null = True, blank = True)
	end_user_state = models.CharField("End User State", choices = STATE_CHOICES, max_length = 2, null = True, blank = True)
	end_user_post_code = models.CharField("End User Post Code", max_length = 10, null = True, blank = True)
	end_user_phone = models.DecimalField("End User Phone Number", max_digits = 10, decimal_places = 0, null = True, blank = True)
	engineer = models.CharField("Engineer", max_length = 48, null = True, blank = True)
	inside_sales = models.CharField("Inside Sales", max_length = 48, null = True, blank = True)
	courier = models.CharField("Courier", max_length = 48, null = True, blank = True)
	account_number = models.DecimalField("Account#", max_digits = 10, decimal_places = 0, null = True, blank = True)
	tracking_number = models.DecimalField("Tracking#", max_digits = 10, decimal_places = 0, null = True, blank = True)

	class Meta:
		ordering = ('-sample_number','ship_to_company')

	def __unicode__(self):
        	return self.ship_to_company + self.battery_description

	@staticmethod
	def get_sample_number():
		if Sample.objects.count() == 0:
			sample_number = 1
		else:
			last_sample_number = Sample.objects.order_by('-sample_number')[0].sample_number
			sample_number = last_sample_number + 1
		return sample_number

	def save(self, new):
		"""
		Saves a new sample to the database if
		1) new == True and there is not already a Sample in the database with the same customer and battery info
		Updates an existing sample if
		2) new == False
		FOR NOW I WILL RELY ON GET_OBJECT_OR_404 IN VIEWS TO MAKE SURE THAT WHEN UPDATING A PROJECT, THAT PROJECT ACTUALLY EXISTS 
		"""
		if new == True:
			try:
				obj = Sample.objects.get(
					date = self.date,
					battery_description = self.battery_description,
					ship_to_company = self.ship_to_company,
					)
				saved = False
				self.id = obj.id
			except Sample.DoesNotExist:
				super(Sample, self).save()
				saved = True
			return self, saved
		else:
			try:
				assert(self.id)
				super(Sample, self).save()
				saved = True
				return self, saved
			except AssertionError:
				saved = False
				return self, saved
class Quote(models.Model):
	"""
	I would like to extend this to the point where it can generate forms like Quotation Forms
	Quotes layout the skeleton of a quotation form which will then be filled in with rows
	The skeleton will include all information onther than batteries, quantities, and prices
	"""
	project = models.ForeignKey(Project)
	author = models.ForeignKey(Contact, related_name = 'author')
	authored_date = models.DateField(null = True)
	editor = models.ForeignKey(Contact, related_name = 'editor')
	edited_date = models.DateField(null = True)
	inquiry_date = models.DateField(null = True)
	quote_number = models.DecimalField("Quote#", max_digits = 4, decimal_places =0)
	date = models.DateField(null = True)
	recipient = models.ForeignKey(Contact, related_name = "quote_recipient", null = True, blank = True)
	fob = models.CharField("Customer Company", max_length = 48, null = True, blank = True)
	terms = models.CharField("Customer Company", max_length = 48, null = True, blank = True)
	customer_company = models.CharField("Customer Company", max_length = 48, null = True, blank = True)
	customer_attention = models.CharField("Customer Attention", max_length = 97, null = True, blank = True)
	customer_address_line1 = models.CharField("Customer Address Line 1", max_length = 30, null = True, blank = True)
	customer_address_line2 = models.CharField("Customer Address Line 2", max_length = 30, null = True, blank = True)
	customer_city = models.CharField("Customer City", max_length = 30, null = True, blank = True)
	customer_state = models.CharField("Customer State", choices = STATE_CHOICES, max_length = 2, null = True, blank = True)
	customer_post_code = models.CharField("Customer Post Code", max_length = 10, null = True, blank = True)
	customer_phone = models.DecimalField("Customer Phone Number", max_digits = 10, decimal_places = 0, null = True, blank = True)
	customer_fax = models.DecimalField("Customer Fax", max_digits = 10, decimal_places = 0, null = True, blank = True)
	customer_email = models.EmailField("Customer Email", null = True, blank = True)
	signature1 = models.ForeignKey(Contact, related_name = "quote_signer1", null = True, blank = True)
	signature1_name = models.CharField("Signature1", max_length = 48, null = True, blank = True)
	signature1_title = models.CharField("Signature1 Title", max_length = 48, null = True, blank = True)
	signature2 = models.ForeignKey(Contact, related_name = "quote_signer2", null = True, blank = True)
	signature2_name = models.CharField("Signature2", max_length = 48, null = True, blank = True)
	signature2_title = models.CharField("Signature2 Title", max_length = 48, null = True, blank = True)
	signature3 = models.ForeignKey(Contact, related_name = "quote_signer3", null = True, blank = True)
	signature3_name = models.CharField("Signature3", max_length = 48, null = True, blank = True)
	signature3_title = models.CharField("Signature3 Title", max_length = 48, null = True, blank = True)
	

	class Meta:
		ordering = ('-quote_number','recipient')

	def __unicode__(self):
        	return 'q#'+str(self.quote_number)

	@staticmethod
	def get_quote_number():
		if Quote.objects.count() == 0:
			quote_number = 1
		else:
			last_quote_number = Quote.objects.order_by('-quote_number')[0].quote_number
			quote_number = last_quote_number + 1
		return quote_number
	
class QuoteRow(models.Model):
	"""
	Each Quote will have a number of rows which will link to the quote form with the quote number
	QuoteRows hold the info on batteries, quantities, and prices
	"""
	quote = models.ForeignKey(Quote)
	battery_description = models.CharField("Battery Description", max_length = 100)
	battery_pack = models.ForeignKey(Pack, related_name = "quote_pack", null = True, blank = True)
	battery = models.ForeignKey(Battery, related_name = "quote_battery", null = True, blank = True)
	quantity = models.DecimalField("Quantity", max_digits = 9, decimal_places =0)
	price = models.DecimalField("Price", max_digits = 7, decimal_places = 3)

	def __unicode__(self):
        	return str(self.quantity) +'pcs--$'+str(self.price)

class SPR(models.Model):
	"""
	I would like to extend this to the point where it can generate forms like Quotation Forms
	Quotes layout the skeleton of a quotation form which will then be filled in with rows
	The skeleton will include all information onther than batteries, quantities, and prices
	"""
	
	related_spr = models.ForeignKey('self', related_name = "Related SPR", null = True, blank = True)
	replace_spr = models.ForeignKey('self', related_name = "Replace SPR", null = True, blank = True)
	project = models.ForeignKey(Project)
	author = models.ForeignKey(Contact, related_name = 'spr_author')
	authored_date = models.DateField(null = True)
	editor = models.ForeignKey(Contact, related_name = 'spr_editor')
	edited_date = models.DateField(null = True)
	spr_number = models.DecimalField("SPR#", max_digits = 4, decimal_places = 0, null = True, blank = True)
	recipient = models.ForeignKey(Contact, related_name = "spr_recipient", null = True, blank = True)

	fob = models.CharField("FOB point", max_length = 48, null = True, blank = True)
	terms = models.CharField("terms", max_length = 48, null = True, blank = True)
	valid_through = models.CharField("valid through", max_length = 48, null = True, blank = True)
	account_type = models.CharField("account type", max_length = 48, null = True, blank = True)
	application = models.CharField("application", max_length = 48, null = True, blank = True)
	notes = models.CharField("notes", max_length = 48, null = True, blank = True)
	pricebook_volume_bracket = models.CharField("pricebook volume bracket", max_length = 48, null = True, blank = True)
	pricebook_effective_date = models.CharField("pricebook effective date", max_length = 48, null = True, blank = True)
	proposed_quantity = models.CharField("proposed quantity", max_length = 48, null = True, blank = True)
	product_to_be_sold = models.CharField("product to be sold", max_length = 48, null = True, blank = True)
	spr_to = models.CharField("to", max_length = 48, null = True, blank = True) 
	spr_from = models.CharField("from", max_length = 48, null = True, blank = True) 

	customer_company = models.CharField("Customer Company", max_length = 48, null = True, blank = True)
	customer_attention = models.CharField("Customer Attention", max_length = 97, null = True, blank = True)
	customer_address_line1 = models.CharField("Customer Address Line 1", max_length = 30, null = True, blank = True)
	customer_address_line2 = models.CharField("Customer Address Line 2", max_length = 30, null = True, blank = True)
	customer_city = models.CharField("Customer City", max_length = 30, null = True, blank = True)
	customer_state = models.CharField("Customer State", choices = STATE_CHOICES, max_length = 2, null = True, blank = True)
	customer_post_code = models.CharField("Customer Post Code", max_length = 10, null = True, blank = True)
	customer_phone = models.DecimalField("Customer Phone Number", max_digits = 10, decimal_places = 0, null = True, blank = True)
	customer_email = models.EmailField("Customer Email", null = True, blank = True)
	
	class Meta:
		ordering = ('-spr_number','recipient')

	def __unicode__(self):
        	return str(self.spr_number)
	
	@staticmethod
	def get_spr_number():
		if SPR.objects.count() == 0:
			spr_number = 1
		else:
			last_spr_number = SPR.objects.order_by('-spr_number')[0].spr_number
			spr_number = last_spr_number + 1
		return spr_number

class SPRRow(models.Model):
	"""
	Each Quote will have a number of rows which will link to the quote form with the quote number
	QuoteRows hold the info on batteries, quantities, and prices
	"""
	spr = models.ForeignKey(SPR)
	battery_description = models.CharField("Battery Description", max_length = 100)
	battery_pack = models.ForeignKey(Pack, related_name = "spr_pack", null = True, blank = True)
	battery = models.ForeignKey(Battery, related_name = "spr_battery", null = True, blank = True)
	quantity = models.DecimalField("Quantity1", max_digits = 9, decimal_places = 0)
	price = models.DecimalField("Price1", max_digits = 7, decimal_places = 3)
	margin = models.DecimalField("Margin1", max_digits = 5, decimal_places = 2, null = True, blank = True)


class Visit(models.Model):
	"""
	This will hold all the information in a call report
	"""
	author = models.ForeignKey(Contact, related_name = 'visit_author')
	authored_date = models.DateField(null = True)
	editor = models.ForeignKey(Contact, related_name = 'visit_editor')
	edited_date = models.DateField(null = True)
	call_location = models.ForeignKey(Contact, related_name = "location")
	territory_number = models.DecimalField("Territory#", max_digits = 4, decimal_places = 0)
	sales_rep = models.ForeignKey(Contact, related_name = "vist_sales_rep")
	new_or_existing = models.CharField("New Or Existing", choices = NEW_OR_EXISTING_CHOICES, max_length = 1)

class Upload(models.Model):
	"""
	Uploaded files have a 
	file_name where they are saved on the server and
	file_title which explains what the file is
	"""
	file = models.FileField("File Name", upload_to = "uploads", max_length = 20)
	file_title = models.CharField("File Title", max_length = 75)

class Link(models.Model):
	"""
	This will link an uploaded file to a model(project, contact, etc.)
	"""
	upload = models.ForeignKey(Upload)

class Link2Project(Link):
	key = models.ForeignKey(Project)

class Link2Contact(Link):
	key = models.ForeignKey(Contact)
	
class Link2Battery(Link):
	key = models.ForeignKey(Battery)
	
class Link2Pack(Link):
	key = models.ForeignKey(Pack)
	
class Link2Quote(Link):
	key = models.ForeignKey(Quote)
	
class Link2SPR(Link):
	key = models.ForeignKey(SPR)
	
class Link2Visit(Link):
	key = models.ForeignKey(Visit)
	
class Link2Sample(Link):
	key = models.ForeignKey(Sample)
	
	
