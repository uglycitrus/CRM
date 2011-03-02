
from django import forms
from django.forms import ModelForm

from myproject.opmlist.formfields import VKBField
from myproject.opmlist.formfields import New_VKBField
from myproject.opmlist.formfields import TypeField
from myproject.opmlist.formfields import New_TypeField
from myproject.opmlist.formfields import DrawingField

from myproject.settings import UPLOAD_DIR
from myproject.opmlist.models import Contact
from myproject.opmlist.models import Battery
from myproject.opmlist.models import Pack
from myproject.opmlist.models import Sample
from myproject.opmlist.models import Quote
from myproject.opmlist.models import QuoteRow
from myproject.opmlist.models import SPR
from myproject.opmlist.models import SPRRow
from myproject.opmlist.models import Visit
from myproject.opmlist.models import Project
from myproject.opmlist.models import Upload

PROJECT_STATUS_CHOICES = (
		('None','None'),
		('dead','dead'),
		('open','open'),
		('continuing','continuing'),
		('spotBusiness','spot business'),
);

MARKET_SEGMENT_CHOICES = (
		('None','None'),
		('Medical','Medical'),
		('Military','Military'),
		('Consumer','Consumer'),
		('Server','Server'),
		('Automotive','Automotive'),
);

DIVISION_CHOICES = (
		('None','None'),
		('PPS','PPS'),
		('Classic','Classic'),
		('Consumer','Consumer')
);

REGION_CHOICES = (
		('None','None'),
		('E','East'),
		('W','West'),
		('N','North'),
		('S','South'),
		('H','House'),
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
		('Li-SOCl2','Li-SOCl2'),
		('Li-MnO2B','Li-MnO2 Button'),
		('Li-MnO2C','Li-MnO2 Cylindrical'),
		('Alkaline','Alkaline'),
		('AgO2','Watch Battery'),
		('HearingAid','Hearing Aid Battery'),
)

TERMINATION_CHOICES = (
		('None','None'),
		('wires','wires'),
		('wire connectors','wire connectors'),
		('PCBD','PCBD'),
		('PCBS','PCBS'),
		('Solder Tabs','Solder Tabs'),
		('Axial Leads','Axial Leads'),
)

CONFIGURATION_CHOICES = (
		('None','None'),
		('Stack','Stack'),
		('Laying Flat','Laying Flat'),
		('Triangle','Triangle'),
		('Mempac','Mempac'),
)

class SearchForm(forms.Form):
	search = forms.CharField()

class VKBForm(forms.Form):
	vkb_number = New_VKBField()

class LogInForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

class SampleEditForm(ModelForm):
	class Meta:
		model = Sample

class SprEditForm(ModelForm):
	class Meta:
		model = SPR

class QuoteEditForm(ModelForm):
	class Meta:
		model = Quote

class ContactEditForm(ModelForm):
	class Meta:
		model = Contact

class UploadEditForm(ModelForm):
	class Meta:
		model = Upload

class BatteryEditForm(ModelForm):
	class Meta:
		model = Battery

class PackEditForm(ModelForm):
	class Meta:
		model = Pack

class VisitEditForm(ModelForm):
	class Meta:
		model = Visit

class RowEditForm(forms.Form):
	quantity1 = forms.CharField(max_length = 50, required = False)
	margin1 = forms.DecimalField(max_digits = 5, decimal_places = 3, required = False)
	price1 = forms.DecimalField(max_digits = 7, decimal_places = 3, required = False)
	rows = forms.DecimalField(
			widget = forms.HiddenInput,
			required = False,
			)
	battery_description1 = forms.CharField(required = False)
	vkb_number1 = VKBField(required = False)
	type_number1 = TypeField(required = False)

class NonRequiredAddressForm(forms.Form):
	non_required_company = forms.CharField(required = False)
	non_required_attention = forms.CharField(required = False)
	non_required_address_line1 = forms.CharField(required = False)
	non_required_address_line2 = forms.CharField(required = False)
	non_required_city = forms.CharField(required = False)
	non_required_state = forms.CharField(required = False)
	non_required_post_code = forms.CharField(required = False)
	non_required_phone = forms.DecimalField(required = False)
	non_required_id = forms.CharField(
			required = False,
			widget = forms.HiddenInput,
			)
	non_required_phone = forms.DecimalField(
		required = False,
		max_value = 9999999999,
		min_value = 1000000000,
		)
	non_required_fax = forms.DecimalField(
		required = False,
		max_value = 9999999999,
		min_value = 1000000000,
		)
	non_required_email = forms.EmailField(
		required = False,
		)
	
class RequiredAddressForm(forms.Form):
	required_company = forms.CharField()
	required_attention = forms.CharField()
	required_address_line1 = forms.CharField()
	required_address_line2 = forms.CharField(required = False)
	required_city = forms.CharField()
	required_state = forms.CharField()
	required_post_code = forms.CharField()
	required_phone = forms.DecimalField(
		required = False,
		max_value = 9999999999,
		min_value = 1000000000,
		)
	required_fax = forms.DecimalField(
		required = False,
		max_value = 9999999999,
		min_value = 1000000000,
		)
	required_email = forms.EmailField(
		required = False,
		)

	required_id = forms.CharField(
			required = False,
			widget = forms.HiddenInput,
			)

class ProjectSearchForm(forms.Form):
	status = forms.CharField(required = False, 
			max_length = 15, 
			widget = forms.Select(choices = PROJECT_STATUS_CHOICES)
			)
	battery = forms.CharField(required = False, max_length = 20)
	division = forms.CharField(required = False, max_length = 7, widget = forms.Select(choices = DIVISION_CHOICES))
	region = forms.CharField(required = False, max_length = 20, widget = forms.Select(choices = REGION_CHOICES))
	customer = forms.CharField(required = False)
	battery_description = forms.CharField(required = False)
	sales_potential = forms.DecimalField(required = False)
	market_segment = forms.CharField(required = False, 
			max_length = 7, 
			widget = forms.Select(choices = MARKET_SEGMENT_CHOICES)
			)

class ProjectEditForm(forms.Form):
	status = forms.CharField(required = False, 
			max_length = 15, 
			widget = forms.RadioSelect(choices = PROJECT_STATUS_CHOICES)
			)
	division = forms.CharField(required = False, 
			max_length = 7, 
			widget = forms.RadioSelect(choices = DIVISION_CHOICES)
			)
	region = forms.CharField(required = False, 
			max_length = 20, 
			widget = forms.RadioSelect(choices = REGION_CHOICES)
			)
	market_segment = forms.CharField(required = False, 
			max_length = 15, 
			widget = forms.RadioSelect(choices = MARKET_SEGMENT_CHOICES)
			)
	customer = forms.CharField(required = False)
	battery_description = forms.CharField(required = False)
	vkb_number = VKBField()
	type_number = TypeField()
	sales_potential = forms.DecimalField(required = False)
	project_manager_name = forms.CharField(required = False)
	project_manager_id = forms.CharField(
			required = False,
			widget = forms.HiddenInput,
			)
	sales_rep_name = forms.CharField(required = False)
	sales_rep_id = forms.CharField(
			required = False,
			widget = forms.HiddenInput,
			)
	primary_contact_name = forms.CharField(required = False)
	primary_contact_id = forms.CharField(
			required = False,
			widget = forms.HiddenInput,
			)
	prototype_verification = forms.DateField(
			('%m/%d/%Y',),
			required = False,
			widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
				'class':'input',
				'readonly':'readonly',
				})
			)
	design_verification = forms.DateField(
			('%m/%d/%Y',),
			required = False,
			widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
				'class':'input',
				'readonly':'readonly',
				})
			)
	manufacturing_verification = forms.DateField(
			('%m/%d/%Y',),
			required = False,
			widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
				'class':'input',
				'readonly':'readonly',
				})
			)
	production_verification = forms.DateField(
			('%m/%d/%Y',),
			required = False,
			widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
				'class':'input',
				'readonly':'readonly',
				})
			)
	end_of_life = forms.DateField(
			('%m/%d/%Y',),
			required = False,
			widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
				'class':'input',
				'readonly':'readonly',
				})
			)

	notes = forms.CharField(
			required = False,
			widget=forms.Textarea,
			)

class ContactSearchForm(forms.Form):
	name = forms.CharField(required = False)
	phone = forms.CharField(required = False)
	email = forms.EmailField(required = False)

##class SampleEditForm(forms.Form):
##	battery_description = forms.CharField(required = False)
##	vkb_number = VKBField()
##	type_number = TypeField()
##	engineer = forms.CharField(required = False)
##	inside_sales = forms.CharField(required = False)
##	date = forms.DateField(
##			('%m/%d/%Y',),
##			required = False,
##			widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
##				'class':'input',
##				'readonly':'readonly',
##				})
##			)
##	battery = forms.CharField(
##			widget = forms.Textarea
##			)

##class SprEditForm(forms.Form):
##	date = forms.DateField(required = False)
##	fob = forms.CharField(max_length = 50, required = False)
##	terms = forms.CharField(max_length = 50, required = False)
##	account_type = forms.CharField(max_length = 50, required = False)
##	application =  forms.CharField(max_length = 50, required = False)
##	proposed_quantity = forms.DecimalField(max_digits = 9, decimal_places = 0, required = False)
##	valid_through= forms.DateField(required = False)
##	notes =  forms.CharField(
##			max_length = 50,
##			required = False,
##			widget=forms.Textarea,
##			)
##	product_to_be_sold =  forms.CharField(max_length = 50, required = False)
##	

##class QuoteEditForm(forms.Form):
##	date = forms.DateField()
##	inquiry_date = forms.DateField()
##	fob = forms.CharField(max_length = 50, required = False)
##	terms = forms.CharField(max_length = 50, required = False)
##	signature1 = forms.CharField(max_length = 50, required = False)
##	signature1_title = forms.CharField(max_length = 50, required = False)
##	signature1_id = forms.CharField(
##			required = False,
##			widget = forms.HiddenInput,
##			)
##	signature2 = forms.CharField(max_length = 50, required = False)
##	signature2_title = forms.CharField(max_length = 50, required = False)
##	signature2_id = forms.CharField(
##			required = False,
##			widget = forms.HiddenInput,
##			)
##	signature3 = forms.CharField(max_length = 50, required = False)
##	signature3_title = forms.CharField(max_length = 50, required = False)
##	signature3_id = forms.CharField(
##			required = False,
##			widget = forms.HiddenInput,
##			)
##	rows = forms.DecimalField(
##			widget = forms.HiddenInput,
##			required = False,
##			)

##class QuoteRowEditForm(forms.Form):
##	battery_description1 = forms.CharField(required = False)
##	vkb_number1 = VKBField(required = False)
##	type_number1 = TypeField(required = False)
##	quantity1 = forms.DecimalField(max_digits = 9, decimal_places = 0)
##	price1 = forms.DecimalField(max_digits = 7, decimal_places = 3)

##class ContactEditForm(forms.Form):
##	firstname = forms.CharField(required = False)
##	lastname = forms.CharField(required = False)
##	company = forms.CharField(required = False)
##	title = forms.CharField(required = False)
##	cell = forms.DecimalField(required = False)
##	landline = forms.DecimalField(required = False)
##	fax = forms.DecimalField(required = False)
##	email = forms.EmailField(required = False)
##	primary_address_line1 = forms.CharField(required = False)
##	primary_address_line2 = forms.CharField(required = False)
##	primary_city = forms.CharField(required = False)
##	primary_state = forms.CharField(required = False)
##	primary_post_code = forms.CharField(required = False)
##	secondary_address_line1 = forms.CharField(required = False)
##	secondary_address_line2 = forms.CharField(required = False)
##	secondary_city = forms.CharField(required = False)
##	secondary_state = forms.CharField(required = False)
##	secondary_post_code = forms.CharField(required = False)

##class PackEditForm(forms.Form):
##	vkb_number = New_VKBField()
##	drawing_number = DrawingField()
##	capacity = forms.DecimalField(required = False)
##	voltage = forms.DecimalField(required = False)
##	series_cells = forms.DecimalField(required = False)
##	parallel_cells  = forms.DecimalField(required = False)
##	max_cont = forms.DecimalField(required = False)
##	max_pulse = forms.DecimalField(required = False)
##	drawing = forms.FileField( required = False)
##	configuration = forms.CharField(required = False, 
##			max_length = 15, 
##			widget = forms.RadioSelect(choices = CONFIGURATION_CHOICES)
##			)
##	chemistry = forms.CharField(required = False, 
##			max_length = 15, 
##			widget = forms.RadioSelect(choices = CHEMISTRY_CHOICES)
##			)
##	type = forms.CharField(required = False, 
##			max_length = 15, 
##			widget = forms.RadioSelect(choices = TYPE_CHOICES)
##			)
##	termination = forms.CharField(required = False, 
##			max_length = 15, 
##			widget = forms.RadioSelect(choices = TERMINATION_CHOICES)
##			)
	
##class BatteryEditForm(forms.Form):
##	type_number = New_TypeField()
##	datasheet = forms.FileField(required = False) 
##	type_description = forms.CharField(required = False) 
##	chemistry = forms.CharField(required = False, 
##			max_length = 15, 
##			widget = forms.RadioSelect(choices = CHEMISTRY_CHOICES)
##			)
##	type = forms.CharField(required = False, 
##			max_length = 15, 
##			widget = forms.RadioSelect(choices = TYPE_CHOICES)
##			)
##	capacity = forms.DecimalField(required = False) 
##	voltage = forms.DecimalField(required = False) 
##	max_cont = forms.DecimalField(required = False) 
##	max_pulse = forms.DecimalField(required = False) 
##	min_storage_temp = forms.DecimalField(required = False) 
##	max_storage_temp = forms.DecimalField(required = False) 
##	min_discharge_temp = forms.DecimalField(required = False) 
##	max_discharge_temp = forms.DecimalField(required = False) 
##	min_charge_temp = forms.DecimalField(required = False) 
##	max_charge_temp = forms.DecimalField(required = False) 
##	discontinued = forms.BooleanField(
##			required = False,
##			)
##
##class UploadEditForm(forms.Form):
##	file = forms.FileField( required = False )
##	file_title = forms.CharField(required = False )
