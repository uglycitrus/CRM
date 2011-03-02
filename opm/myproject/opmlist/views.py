#import from python
import datetime
import time
import re
import os

from datetime import timedelta

#import from django 
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import Context, loader, RequestContext
from django.contrib.auth.decorators import login_required

#import models
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
from myproject.opmlist.models import Link
from myproject.opmlist.models import Link2Project
from myproject.opmlist.models import Link2Battery

#import forms
from myproject.opmlist.forms import ContactSearchForm
from myproject.opmlist.forms import ContactEditForm
from myproject.opmlist.forms import ProjectSearchForm
from myproject.opmlist.forms import ProjectEditForm
from myproject.opmlist.forms import SampleEditForm
from myproject.opmlist.forms import NonRequiredAddressForm
from myproject.opmlist.forms import RequiredAddressForm
from myproject.opmlist.forms import QuoteEditForm
from myproject.opmlist.forms import RowEditForm
from myproject.opmlist.forms import SprEditForm
from myproject.opmlist.forms import LogInForm
from myproject.opmlist.forms import SearchForm
from myproject.opmlist.forms import BatteryEditForm
from myproject.opmlist.forms import VKBForm
from myproject.opmlist.forms import PackEditForm
from myproject.opmlist.forms import UploadEditForm
 

 #LogIn & LogOut VIEWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def login_view(request):
	# forward the user to the welcome page if they are logged in
	if request.user.is_authenticated():
		return HttpResponseRedirect( reverse('project_list') )
	# if they're not logged in already they must complete the sign in form
	form = LogInForm()
	if request.method == 'POST':
		form = LogInForm(request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(username = username, password = password)
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('project_list'))
			else:
				raise "Account is disabled"
				return render_to_response('login.html', {'form':form, 'user':user})
		else:
			return render_to_response('login.html', {'form':form})
	else:
		return render_to_response('login.html', {'form':form})

def logout_view(request):
	logout(request)
	# redirect the user back to the login page	
	return HttpResponseRedirect( reverse('login') )


#PROJECT VIEWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def project_list(request):
	"""
	Initially displays no projects - just a blank form
	If there is a GET request then the page will display a sortable paginated list of projects
	If search form is left blank, all projects will be returned
	Otherwise a list (actually a Queryset) of all projects meeting the search criteria will be returned
	"""
	tab = 'project'
	user = request.user
	form = ProjectSearchForm()
	list = Project.objects.all()
		
	if request.method == 'GET':
		form = ProjectSearchForm(request.GET)
		if form.is_valid():
			status = request.GET.get('status') 
			division = request.GET.get('division') 
			region = request.GET.get('region')
			market_segment = request.GET.get('market_segment')
			customer = request.GET.get('customer')
			battery_search = request.GET.get('battery')
			sales_potential = request.GET.get('sales_potential')
			list = ProjectSearch(list, status, division, region, market_segment, customer, battery_search, sales_potential)
		return render_to_response('project_list.html',{'tab':tab, 'list':list, 'user':user, 'form':form}, context_instance=RequestContext(request))
	return render_to_response('project_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user}, context_instance=RequestContext(request))

@login_required
def project_new(request):
	"""
	Display page with form until there is a POST request
	Handle the form - and return a "new_project" 
	If the "new_project" is actually new save it and redirect to project list
	Else remain on page with form, and give an error message
	"""
	tab = 'project'
	user = request.user
	form = ProjectEditForm()
	if request.method == 'POST':
		form = ProjectEditForm(request.POST)
		new_project = ProjectEditFormHandler(form)
		if new_project:
			new_project, saved = new_project.save(new = True)
			if saved:
				return HttpResponseRedirect(reverse('project_list'))
			else:
				return render_to_response('project_new.html',{'tab':tab, 'form':form, 'user':user})
	return render_to_response('project_new.html',{'tab':tab, 'form':form, 'user':user})

@login_required
def project_edit(request, id):
	"""
	404 if no project is found
	Initialize form data based on existing data on the project
	Display page with form until there is a POST request
	Handle the form - and return an "edited_project" 
	If the "edited_project" actually exists, update it, and redirect to project list
	Else remain on page with form, and give an error message
	"""
	project = get_object_or_404(Project, id = id)
	tab = 'project'
	user = request.user
	initial = InitializeProjectEditForm(project)
	form = ProjectEditForm(initial = initial)
	if request.method == 'POST':
		form = ProjectEditForm(request.POST)
		edited_project = ProjectEditFormHandler(form)
		if edited_project:
			edited_project.id = project.id
			edited_project.save(new = False)
			return HttpResponseRedirect(reverse('project_list'))
	return render_to_response('project_edit.html',{'tab':tab, 'form':form, 'user':user, 'project':project})

@login_required
def project_view(request, id):
	tab = 'project'
	user = request.user
	project = Project.objects.get(id = id)
	return render_to_response('project_view.html',{'tab':tab, 'user':user, 'project':project})

#BATTERY VIEWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def pack_new(request):
	tab = 'battery'
	user = request.user
	form = PackEditForm()
	vkb_form = VKBForm()
	if request.method == 'POST':
		form = PackEditForm(request.POST, request.FILES)
		vkb_form = VKBForm(request.POST)
		if form.is_valid() and vkb_form.is_valid():
			drawing = request.FILES['drawing']
			pack = None
			pack = PackEditFormHandler(pack, form, vkb_form, drawing)
			pack.save()
			pack.drawing.save(pack.vkb_number+'.pdf', drawing)
			return HttpResponseRedirect(reverse('pack_list', args = [pack.battery.type_number]))
	return render_to_response('pack_new.html', {'tab':tab,'form': form, 'vkb_form':vkb_form, 'user':user})

@login_required
def pack_list(request, type_number):
	tab = 'battery'
	user = request.user
	battery = Battery.objects.get(type_number = type_number)
	projects = Project.objects.filter(battery = battery)
	list = battery.pack_set.all()
	return render_to_response('pack_list.html', {'tab':tab,'list':list,'battery':battery, 'projects':projects}, context_instance=RequestContext(request))

@login_required
def pack_edit(request, vkb_number):
	tab = 'battery'
	user = request.user
	pack = Pack.objects.get(vkb_number = vkb_number)
	projects = Project.objects.filter(Q(battery_pack = pack))
	form, vkb_form = InitializePackEditForm(pack)
	if request.method == 'POST':
		form = PackEditForm(request.POST, request.FILES)
		vkb_form = VKBForm(request.POST)
		if form.is_valid() and vkb_form.is_valid():
			if request.FILES: drawing = request.FILES['drawing']
			else: drawing = None
			pack = PackEditFormHandler(pack, form, vkb_form, drawing)
			pack.save()
			if drawing:
				pack.drawing.save(vkb_number, drawing)
			return HttpResponseRedirect(reverse('pack_list', args = [pack.battery.type_number]))
	return render_to_response('pack_edit.html', {'tab':tab,'form': form, 'vkb_form': vkb_form, 'user':user, 'projects':projects, 'pack':pack})

@login_required
def battery_new(request):
	tab = 'battery'
	user = request.user
	form = BatteryEditForm()
	if request.method == 'POST':
		form = BatteryEditForm(request.POST, request.FILES)
		if form.is_valid():
			battery = None
			datasheet = request.FILES['datasheet']
			battery = BatteryEditFormHandler(form, battery, datasheet)
			if battery:
				battery.save()
				battery.save_datasheet(datasheet)
				return HttpResponseRedirect(reverse('battery_list', args=['None','None']))
	return render_to_response('battery_new.html', {'tab':tab,'form': form, 'user':user})

@login_required
def battery_edit(request, id):
	tab = 'battery'
	user = request.user
	battery = Battery.objects.get(id = id)
	initial = InitializeBatteryEditForm(battery)
	form = BatteryEditForm(initial = initial)
	if request.method == 'POST':
		form = BatteryEditForm(request.POST, request.FILES)
		if form.is_valid():
			if request.FILES: datasheet = request.FILES['datasheet']
			else: datasheet = None
			battery = BatteryEditFormHandler(form, battery, datasheet)
			if battery:
				battery.save()
				if datasheet: battery.save_datasheet(datasheet)
				return HttpResponseRedirect(reverse('battery_list', args=['None','None']))
	return render_to_response('battery_edit.html', {'tab':tab,'form': form, 'user':user})


@login_required
def battery_list(request, value, selection):
	tab = 'battery'
	form = SearchForm()
	user = request.user
	if value == 'type':
		if selection == 'Discontinued':
			list = Battery.objects.filter(discontinued = True)
		else:	
			list = Battery.objects.filter(type = selection)
	elif value == 'chemistry':
		list = Battery.objects.filter(chemistry = selection)
	else:
		list = Battery.objects.all()
	if request.method == 'GET':
		form = SearchForm(request.GET)
		if form.is_valid():
			search = request.GET.get('search')
			list = BatterySearch(search)
	return render_to_response('battery_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user}, context_instance=RequestContext(request))
#CONTACT VIEWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def contact_list(request):
	tab='contact'
	user = request.user
	form = SearchForm()
	list = Contact.objects.all()
	if request.method == 'GET':
		form = SearchForm(request.GET)
		if form.is_valid():
			search = request.GET.get('search') 
			list = ContactSearch(search)
		return render_to_response('contact_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user}, context_instance=RequestContext(request))
	else:
		return render_to_response('contact_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user}, context_instance=RequestContext(request))

@login_required
def contact_new(request):
	tab='contact'
	user = request.user
	form = ContactEditForm()
	if request.method == 'GET':
		form = ContactEditForm(request.GET)
		if form.is_valid():
			new_contact = ContactEditFormHandler(form)
			new_contact.save(new = True)
			return HttpResponseRedirect(reverse('contact_list'))
	return render_to_response('contact_new.html',{'tab':tab, 'form':form, 'user':user})

@login_required
def contact_new_popup(request):
	"""
	exactly the same as contact_new just different template
	"""
	tab='contact'
	user = request.user
	form = ContactEditForm()
	if request.method == 'POST':
		form = ContactEditForm(request.POST)
		if form.is_valid():
			new_contact = ContactEditFormHandler(form)
			new_contact.save(new = True)
			return HttpResponse('''
				<script type="text/javascript">
					window.close();
				</script>''')
	return render_to_response('contact_new_popup.html',{'tab':tab, 'form':form, 'user':user})

@login_required
def contact_edit(request, id):
	"""
	"""
	tab='contact'
	user = request.user
	contact = Contact.objects.get(id = id)
	initial = InitializeContactEditForm(contact)
	form = ContactEditForm(initial = initial)
	if request.method == 'POST':
		form = ContactEditForm(request.POST)
		if form.is_valid():
			edited_contact = ContactEditFormHandler(form)
			edited_contact.id = contact.id
			edited_contact.save(new = False)
			return HttpResponseRedirect(reverse('contact_list'))
	return render_to_response('contact_edit.html',{'tab':tab, 'form':form, 'user':user,'projects':projects, 'contact':contact})

@login_required
def contact_view(request, id):
	tab='contact'
	user = request.user
	contact = Contact.objects.get(id = id)
	projects = Project.objects.filter(Q(primary_contact = contact)|Q(sales_rep = contact)|Q(project_manager = contact))
	return render_to_response('contact_view.html',{'tab':tab, 'user':user,'projects':projects, 'contact':contact})

@login_required
def contact_add_popup(request, contact_type):
	"""
	exactly the same as contact_list just different template and initially none() rather than all()
	"""
	tab='contact'
	user = request.user
	form = SearchForm()
	list = []
	if request.method == 'GET':
		form = SearchForm(request.GET)
		if form.is_valid():
			search = request.GET.get('search') 
			list = ContactSearch(search)
	return render_to_response('contact_add_popup.html',{'tab':tab, 'list':list, 'form':form, 'user':user, 'contact_type':contact_type})

#SAMPLE VIEWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def sample_list(request):
	"""
	Initially displays all Samples in a sortable paginated list of projects
	If there is a GET request then the page will display a list (actually a Queryset) of all projects meeting the search criteria
	"""
	tab = 'sample'
	user = request.user
	form = SearchForm(request.GET)
	search = request.GET.get('search') 
	list = SampleSearch(search)
	return render_to_response('sample_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user}, context_instance=RequestContext(request))


@login_required
def sample_new_independent(request):
	tab = 'sample'
	user = request.user
	today = datetime.date.today()
	form = SampleEditForm(initial = {
		'date' : today.strftime("%m/%d/%Y")
		})
	ship_to_form = RequiredAddressForm()
	end_user_form = NonRequiredAddressForm()
	sample = None

	if request.method == 'POST':
		form = SampleEditForm(request.POST)
		ship_to_form = RequiredAddressForm(request.POST)
		end_user_form = NonRequiredAddressForm(request.POST)
		if form.is_valid() and ship_to_form.is_valid() and end_user_form.is_valid():
			new_sample = SampleFormHandler(sample, form, ship_to_form, end_user_form)
			if new_sample:
				new_sample.authored_date = today
				new_sample.edited_date = today
				new_sample.author = Contact.objects.get(user = user)
				new_sample.editor = Contact.objects.get(user = user)
				new_sample.sample_number = Sample.get_sample_number()
				new_sample.save(new=True)
				response = SampleWordDoc(new_sample)
				return response
	return render_to_response('sample_new.html',{'tab':tab, 'form':form, 'user':user, 'end_user_form':end_user_form, 'ship_to_form':ship_to_form })

@login_required
def sample_new(request, project_id):
	tab = 'sample'
	user = request.user
	get_object_or_404(Project, id = project_id)
	project = Project.objects.get(id = project_id)
	today = datetime.date.today()
	sample = None
	form = SampleEditForm()
	ship_to_form = RequiredAddressForm()
	end_user_form = NonRequiredAddressForm()
	if request.method == 'POST':
		form = SampleEditForm(request.POST)
		ship_to_form = RequiredAddressForm(request.POST)
		end_user_form = NonRequiredAddressForm(request.POST)
		if form.is_valid() and ship_to_form.is_valid() and end_user_form.is_valid():
			new_sample = SampleFormHandler(sample, form, ship_to_form, end_user_form)
			if new_sample:
				new_sample.project = project
				new_sample.authored_date = today
				new_sample.edited_date = today
				new_sample.author = Contact.objects.get(user = user)
				new_sample.editor = Contact.objects.get(user = user)
				new_sample.sample_number = Sample.get_sample_number()
				new_sample.save(new=True)
				response = SampleWordDoc(new_sample)
				return response
	return render_to_response('sample_new.html',{'tab':tab, 'form':form, 'user':user, 'end_user_form':end_user_form, 'ship_to_form':ship_to_form })

@login_required
def sample_edit_or_view(request, id):
	tab = 'sample'
	user = request.user
	sample = Sample.objects.get(id = id)
	today = datetime.date.today()
	form, ship_to_form, end_user_form = InitializeSampleEditForm(sample)
	if user == sample.author.user:
		if request.method == 'POST':
			form = SampleEditForm(request.POST)
			ship_to_form = RequiredAddressForm(request.POST)
			end_user_form = NonRequiredAddressForm(request.POST)
			if form.is_valid() and ship_to_form.is_valid() and end_user_form.is_valid():
				new_sample = SampleFormHandler(sample, form, ship_to_form, end_user_form)
				if new_sample:
					new_sample.id = sample.id
					new_sample.project = sample.project
					new_sample.edited_date = today
					new_sample.editor = Contact.objects.get(user = user)
					new_sample.save(new=False)
					response = SampleWordDoc(new_sample)
					return response
		else:
			return render_to_response('sample_edit.html',{'tab':tab, 'form':form, 'user':user, 'sample':sample, 'end_user_form':end_user_form, 'ship_to_form':ship_to_form })

	else:
		return render_to_response('sample_view.html',{'tab':tab, 'user':user, 'sample':sample})




#QUOTE VIEWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def quote_list(request):
	tab = 'quote'
	user = request.user
	form = SearchForm()
	list = QuoteRow.objects.order_by('quote').all()
	if request.method == 'GET':
		form = SearchForm(request.GET)
		if form.is_valid():
			search = request.GET.get('search') 
			list = QuoteSearch(search)
	return render_to_response('quote_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user}, context_instance=RequestContext(request))

@login_required
def quote_new(request, project_id):
	project = get_object_or_404(Project, id = project_id)
	tab = 'quote'
	user = request.user
	form, customer_form = InitializeProjectForm(project)
	row_form = RowEditForm()
	if request.method == 'POST':
		form = QuoteEditForm(request.POST)
		customer_form = RequiredAddressForm(request.POST)
		if form.is_valid() and customer_form.is_valid():
			quote = QuoteEditFormHandler(form, customer_form)
			new_quote.save()

			for i in range(rows):
				battery_description = request.POST.get('battery_description'+str(i+1))
				if request.POST.get('type_number'+str(i+1)): 
					type_number = request.POST.get('type_number'+str(i+1))
					battery = Battery.objects.get(type_number = type_number)
				else:
					battery = None
				if request.POST.get('vkb_number'+str(i+1)):
					vkb_number = request.POST.get('vkb_number'+str(i+1))
					battery_pack = Pack.objects.get(vkb_number = vkb_number)
					battery = battery_pack.battery
				else:
					battery_pack = None
				if not request.POST.get('type_number'+str(i+1)) and not request.POST.get('vkb_number'+str(i+1)):
					battery = None
					battery_pack = None
				quantity = request.POST.get('quantity'+str(i+1))
				price = request.POST.get('price'+str(i+1))
				new_quote_row = QuoteRow(
					quote = new_quote,
					battery_description = battery_description,
					battery = battery,
					battery_pack = battery_pack,
					quantity = quantity,
					price = price,
					)
				new_quote_row.save()

			rows = new_quote.quoterow_set.all().reverse()
			c = Context({'quote':new_quote, 'rows':rows})
			t = loader.get_template('xml/quote-base.xml')
			render_xml = t.render(c)
			response = HttpResponse(render_xml, mimetype='application/ms-word')
			response['Content-Disposition'] = 'attachment; filename='+customer_company+' '+str(new_quote.edited_date)+'-quote.doc'
			return response
	return render_to_response('quote_new.html',{'tab':tab, 'form':form, 'customer_form':customer_form, 'row_form':row_form, 'user':user})

@login_required
def quote_edit_or_view(request, id):
	tab = 'quote'
	user = request.user
	quote = Quote.objects.get(id = id)
	rows = quote.quoterow_set.all().reverse()
	row_count = rows.count()
	if user.groups.all()[0] == quote.author.user.groups.all()[0]:
		customer_form = RequiredAddressForm(initial = {
			'required_company' : quote.customer_company,
			'required_attention' : quote.customer_attention,
			'required_address_line1' : quote.customer_address_line1,
			'required_address_line2' : quote.customer_address_line2,
			'required_city' : quote.customer_city,
			'required_state' : quote.customer_state,
			'required_post_code' : quote.customer_post_code,
			'required_phone' : quote.customer_phone,
			'required_id' : quote.customer_attention,
			})
		form = QuoteEditForm(initial = {
			'date' : quote.edited_date,
			'inquiry_date' : quote.inquiry_date,
			'terms' : quote.terms,
			'fob' : quote.fob,
			'rows' : str(row_count),
			'signature1' : quote.signature1_name,
			'signature1_title' : quote.signature1_title,
			'signature2' : quote.signature2_name,
			'signature2_title' : quote.signature2_title,
			'signature3' : quote.signature3_name,
			'signature3_title' : quote.signature3_title,
			})

		if request.method == 'POST':
			form = QuoteEditForm(request.POST)
			customer_form = RequiredAddressForm(request.POST)
			if form.is_valid() and customer_form.is_valid():
				date = form.cleaned_data['date'] 
				inquiry_date = form.cleaned_data['inquiry_date'] 
				rows = form.cleaned_data['rows']
				fob = form.cleaned_data['fob']
				terms = form.cleaned_data['terms']
				customer_company = customer_form.cleaned_data['required_company'] 
				customer_attention = customer_form.cleaned_data['required_attention'] 
				customer_address_line1 = customer_form.cleaned_data['required_address_line1'] 
				customer_address_line2 = customer_form.cleaned_data['required_address_line2'] 
				customer_city = customer_form.cleaned_data['required_city'] 
				customer_state = customer_form.cleaned_data['required_state'] 
				customer_post_code = customer_form.cleaned_data['required_post_code'] 
				customer_phone = customer_form.cleaned_data['required_phone'] 
				customer_fax = customer_form.cleaned_data['required_fax'] 
				customer_email = customer_form.cleaned_data['required_email'] 
				signature1 = form.cleaned_data['signature1']
				signature1_title = form.cleaned_data['signature1_title']
				signature2 = form.cleaned_data['signature2']
				signature2_title = form.cleaned_data['signature2_title']
				signature3 = form.cleaned_data['signature3']
				signature3_title = form.cleaned_data['signature3_title']
				edited_quote = Quote(
					id = quote.id,
					project = quote.project,
					quote_number = quote.quote_number,
					date = date,
					author = Contact.objects.get(user = user),
					editor = Contact.objects.get(user = user),
					authored_date = date,
					edited_date = date,
					fob = fob,
					terms = terms,
					inquiry_date = inquiry_date,
					signature1_name = signature1,
					signature1_title = signature1_title,
					signature2_name = signature2,
					signature2_title = signature2_title,
					signature3_name = signature3,
					signature3_title = signature3_title,
					customer_company = customer_company,
					customer_attention = customer_attention,
					customer_address_line1 = customer_address_line1,
					customer_address_line2 = customer_address_line2,
					customer_city = customer_city,
					customer_state = customer_state,
					customer_post_code = customer_post_code,
					customer_phone = customer_phone,
					customer_fax = customer_fax,
					customer_email = customer_email,
					)
				edited_quote.save()

				for i in range(row_count):
					battery_description = request.POST.get('battery_description'+str(i+1))
					type_number = request.POST.get('type_number'+str(i+1))
					vkb_number = request.POST.get('vkb_number'+str(i+1))
					if type_number:
						match = Battery.objects.filter(type_number = type_number)
						if match:
							battery = match[0]
						else:
							battery = None
					else:
						battery = None
					if vkb_number:
						match = Pack.objects.filter(vkb_number = vkb_number)
						if match:
							battery_pack = match[0]
						else:
							battery_pack = None
					else:
						battery_pack = None
					if not request.POST.get('type_number'+str(i+1)) and not request.POST.get('vkb_number'+str(i+1)):
						battery = None
						battery_pack = None
					quantity = request.POST.get('quantity'+str(i+1))
					price = request.POST.get('price'+str(i+1))
					id = request.POST.get('row_id'+str(i+1))
					edited_quote_row = QuoteRow(
						id = id,
						quote = edited_quote,
						battery_description = battery_description,
						battery = battery,
						battery_pack = battery_pack,
						quantity = quantity,
						price = price,
						)
					edited_quote_row.save()

				rows = edited_quote.quoterow_set.all().reverse()
				c = Context({'quote':edited_quote, 'rows':rows})
				t = loader.get_template('xml/quote-base.xml')
				render_xml = t.render(c)
				response = HttpResponse(render_xml, mimetype='application/ms-word')
				quote_number = quote.quote_number
				response['Content-Disposition'] = 'attachment; filename='+customer_company+' '+str(edited_quote.edited_date)+'-quote.doc'
				return response
		else:
			return render_to_response('quote_edit.html',{'tab':tab, 'form':form, 'user':user, 'rows' :rows, 'customer_form':customer_form})
	else:
		return render_to_response('quote_view.html',{'tab':tab, 'user':user, 'quote':quote, 'rows':rows})
#SPR VIEWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def spr_list(request):
	tab = 'spr'
	user = request.user
	form = SearchForm()
	list = SPRRow.objects.order_by('spr').all()
	if request.method == 'GET':
		form = SearchForm(request.GET)
		if form.is_valid():
			search = request.GET.get('search') 
			if search:
				if re.match(r'^\d*$', search):
					battery, pack = [], []
					pack = Pack.objects.filter(Q(vkb_number__icontains = search)|Q(drawing_number__icontains = search))
					battery = Battery.objects.filter(type_number__icontains = search)
					if battery:
						for i in battery:
							if list.filter(battery = i):
								list = list.filter(battery = i)
					if pack:
						for i in pack:
							if list.filter(battery_pack = i):
								list = list.filter(battery_pack = i)
					if not battery and not pack:
						list = []
				else:
					battery = Battery.objects.filter(type_description__icontains = search)
					if battery:
						for i in battery:
							list = list.filter(battery = i)
					else:
						list = SPRRow.objects.none()
						list = SPRRow.objects.filter(
							battery_description__icontains = search
							)
						spr_list = SPR.objects.filter(
							Q(product_to_be_sold__icontains = search)|
							Q(customer_company__icontains = search)|
							Q(customer_attention__icontains = search)|
							Q(customer_address_line1__icontains = search)|
							Q(customer_address_line2__icontains = search)|
							Q(customer_city__icontains = search)|
							Q(customer_state__icontains = search)
							)
						if spr_list:
							for i in spr_list:
								list = list|i.sprrow_set.all()
						list = list.order_by('spr')
		return render_to_response('spr_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user}, context_instance=RequestContext(request))
	else:
		return render_to_response('spr_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user}, context_instance=RequestContext(request))

@login_required
def spr_new(request, project_id):
	tab = 'spr'
	user = request.user
	get_object_or_404(Project, id = project_id)
	today = datetime.date.today()
	project = Project.objects.get(id = project_id)
	if project.primary_contact:
		initial = {
		'required_company' : project.primary_contact.company,
		'required_attention' : project.primary_contact.firstname+" "+project.primary_contact.lastname,
		'required_address_line1' : project.primary_contact.primary_address_line1,
		'required_address_line2' : project.primary_contact.primary_address_line2,
		'required_city' : project.primary_contact.primary_city,
		'required_state' : project.primary_contact.primary_state,
		'required_post_code' : project.primary_contact.primary_post_code,
		'required_phone' : project.primary_contact.landline,
		'required_id' : project.primary_contact.id,
		}
	else:
		initial = {}
	customer_form = RequiredAddressForm(initial = initial)
	row_form = RowEditForm()
	form = SprEditForm(initial = {
		'date' : today,
		'valid_through' : today + timedelta(365),
		'terms' : 'Net 30',
		'fob' : 'Harrisburg, PA',
		'rows' : 1,
		})

	if request.method == 'POST':
		form = SprEditForm(request.POST)
		customer_form = RequiredAddressForm(request.POST)
		if form.is_valid() and customer_form.is_valid() and row_form.is_valid():
			date = form.cleaned_data['date'] 
			valid_through = form.cleaned_data['valid_through'] 
			application = form.cleaned_data['application'] 
			product_to_be_sold = form.cleaned_data['product_to_be_sold'] 
			notes = form.cleaned_data['notes'] 
			account_type = form.cleaned_data['account_type'] 
			proposed_quantity = form.cleaned_data['proposed_quantity'] 
			fob = form.cleaned_data['fob']
			terms = form.cleaned_data['terms']
			rows = row_form.cleaned_data['rows']
			customer_company = customer_form.cleaned_data['required_company'] 
			customer_attention = customer_form.cleaned_data['required_attention'] 
			customer_address_line1 = customer_form.cleaned_data['required_address_line1'] 
			customer_address_line2 = customer_form.cleaned_data['required_address_line2'] 
			customer_city = customer_form.cleaned_data['required_city'] 
			customer_state = customer_form.cleaned_data['required_state'] 
			customer_post_code = customer_form.cleaned_data['required_post_code'] 
			customer_phone = customer_form.cleaned_data['required_phone'] 
			spr_number = SPR.get_spr_number()
			new_spr = SPR(
					project = project,
					spr_number = spr_number,
					authored_date = date,
					edited_date = date,
					valid_through = valid_through,
					application = application, 
					product_to_be_sold = product_to_be_sold,
					notes = notes,
					account_type = account_type,
					proposed_quantity = proposed_quantity,
					fob = fob,
					terms = terms,
					author = Contact.objects.get(user = user),
					editor = Contact.objects.get(user = user),
					customer_company = customer_company,
					customer_attention = customer_attention,
					customer_address_line1 = customer_address_line1,
					customer_address_line2 = customer_address_line2,
					customer_city = customer_city,
					customer_state = customer_state,
					customer_post_code = customer_post_code,
					customer_phone = customer_phone,
					)
			new_spr.save()

			for i in range(rows):
				battery_description = request.POST.get('battery_description'+str(i+1))
				if request.POST.get('type_number'+str(i+1)): 
					type_number = request.POST.get('type_number'+str(i+1))
					battery = Battery.objects.get(type_number = type_number)
				else:
					battery = None
				if request.POST.get('vkb_number'+str(i+1)):
					vkb_number = request.POST.get('vkb_number'+str(i+1))
					battery_pack = Pack.objects.get(vkb_number = vkb_number)
					battery = battery_pack.battery
				else:
					battery_pack = None
				if not request.POST.get('type_number'+str(i+1)) and not request.POST.get('vkb_number'+str(i+1)):
					battery = None
				margin = request.POST.get('margin'+str(i+1))
				if not margin:
					margin = None
				quantity = request.POST.get('quantity'+str(i+1))
				price = request.POST.get('price'+str(i+1))
				new_spr_row = SPRRow(
					spr = new_spr,
					margin = margin,
					quantity = quantity,
					price = price,
					battery_description = battery_description,
					battery = battery,
					battery_pack = battery_pack,
					)
				new_spr_row.save()
			rows = new_spr.sprrow_set.all().reverse()

			c = Context({'spr':new_spr, 'rows':rows})
			t = loader.get_template('xml/spr-base.xml')
			render_xml = t.render(c)
			response = HttpResponse(render_xml, mimetype='application/ms-word')
			response['Content-Disposition'] = 'attachment; filename='+customer_company+'-'+battery_description+'-'+str(date)+'-spr.doc'
			return response
	return render_to_response('spr_new.html',{'tab':tab, 'form':form, 'user':user,'customer_form':customer_form, 'row_form':row_form})

@login_required
def spr_edit_or_view(request, id):
	tab = 'spr'
	user = request.user
	spr = SPR.objects.get(id = id)
	rows = spr.sprrow_set.all().reverse()
	row_count = rows.count()
	if user.groups.all()[0] == spr.author.user.groups.all()[0]:
		customer_form = RequiredAddressForm(initial = {
			'required_company' : spr.customer_company,
			'required_attention' : spr.customer_attention,
			'required_address_line1' : spr.customer_address_line1,
			'required_address_line2' : spr.customer_address_line2,
			'required_city' : spr.customer_city,
			'required_state' : spr.customer_state,
			'required_post_code' : spr.customer_post_code,
			'required_phone' : spr.customer_phone,
			'required_id' : spr.customer_attention,
			})
		form = SprEditForm(initial = {
			'date' : spr.edited_date,
			'valid_through' : spr.valid_through,
			'terms' : spr.terms,
			'fob' : spr.fob,
			'account_type' : spr.account_type,
			'application' : spr.application,
			'proposed_quantity' : spr.proposed_quantity,
			'product_to_be_sold' : spr.product_to_be_sold,
			'rows' : str(row_count),
			})

		if request.method == 'POST':
			form = SprEditForm(request.POST)
			customer_form = RequiredAddressForm(request.POST)
			if form.is_valid() and customer_form.is_valid():
				date = form.cleaned_data['date'] 
				valid_through = form.cleaned_data['valid_through'] 
				application = form.cleaned_data['application'] 
				product_to_be_sold = form.cleaned_data['product_to_be_sold'] 
				notes = form.cleaned_data['notes'] 
				account_type = form.cleaned_data['account_type'] 
				proposed_quantity = form.cleaned_data['proposed_quantity'] 
				fob = form.cleaned_data['fob']
				terms = form.cleaned_data['terms']
				rows = form.cleaned_data['rows']
				customer_company = customer_form.cleaned_data['required_company'] 
				customer_attention = customer_form.cleaned_data['required_attention'] 
				customer_address_line1 = customer_form.cleaned_data['required_address_line1'] 
				customer_address_line2 = customer_form.cleaned_data['required_address_line2'] 
				customer_city = customer_form.cleaned_data['required_city'] 
				customer_state = customer_form.cleaned_data['required_state'] 
				customer_post_code = customer_form.cleaned_data['required_post_code'] 
				customer_phone = customer_form.cleaned_data['required_phone'] 
				edited_spr = SPR(
					id = spr.id,
					spr_number = spr.spr_number,
					project = spr.project,
					authored_date = date,
					edited_date = date,
					valid_through = valid_through,
					application = application, 
					product_to_be_sold = product_to_be_sold,
					notes = notes,
					account_type = account_type,
					proposed_quantity = proposed_quantity,
					fob = fob,
					terms = terms,
					author = Contact.objects.get(user = user),
					editor = Contact.objects.get(user = user),
					customer_company = customer_company,
					customer_attention = customer_attention,
					customer_address_line1 = customer_address_line1,
					customer_address_line2 = customer_address_line2,
					customer_city = customer_city,
					customer_state = customer_state,
					customer_post_code = customer_post_code,
					customer_phone = customer_phone,
					)
				edited_spr.save()
				for i in range(row_count-1):
					battery_description = request.POST.get('battery_description'+str(i+1))
					if request.POST.get('type_number'+str(i+1)): 
						type_number = request.POST.get('type_number'+str(i+1))
						battery = Battery.objects.get(type_number = type_number)
					else:
						battery = None
					if request.POST.get('vkb_number'+str(i+1)):
						vkb_number = request.POST.get('vkb_number'+str(i+1))
						battery_pack = Pack.objects.get(vkb_number = vkb_number)
						battery = battery_pack.battery
					else:
						battery_pack = None
					if not request.POST.get('type_number'+str(i+1)) and not request.POST.get('vkb_number'+str(i+1)):
						battery = None
					margin = request.POST.get('margin'+str(i+1))
					if margin == "None":
						margin = 0
					quantity = request.POST.get('quantity'+str(i+1))
					price = request.POST.get('price'+str(i+1))
					id = request.POST.get('row_id'+str(i+1))
					edited_spr_row = SPRRow(
						id = id,
						spr = spr,
						margin = margin,
						quantity = quantity,
						price = price,
						battery_description = battery_description,
						battery = battery,
						battery_pack = battery_pack,
						)
					edited_spr_row.save()

				rows = edited_spr.sprrow_set.all().reverse()
				c = Context({'spr':edited_spr, 'rows':rows})
				t = loader.get_template('xml/spr-base.xml')
				render_xml = t.render(c)
				response = HttpResponse(render_xml, mimetype='application/ms-word')
				response['Content-Disposition'] = 'attachment; filename='+customer_company+'-'+product_to_be_sold+'-'+str(date)+'-spr.doc'
				return response
		else:
			return render_to_response('spr_edit.html',{'tab':tab, 'form':form, 'user':user, 'rows' :rows, 'customer_form':customer_form})
	else:
		return render_to_response('spr_view.html',{'tab':tab, 'user':user, 'spr':spr, 'rows':rows})

@login_required
def spr_word_doc(request, spr_number):
	tab = 'spr'
	user = request.user
	new_spr = Sample.objects.get(spr_number = spr_number)
	c = Context({'spr':new_spr})
	t = loader.get_template('xml/spr-base.xml')
	render_xml = t.render(c)
	response = HttpResponse(render_xml, mimetype='application/ms-word')
	response['Content-Disposition'] = 'attachment; filename='+new_spr.ship_to_attention+'-spr.doc'
	return response

#UPLOAD VIEWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def upload_new(request):
	tab = 'upload'
	user = request.user
	form = UploadEditForm()
	if request.method == 'POST':
		form = UploadEditForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			file_title = form.cleaned_data['file_title']
			new_upload = Upload(
				file_title = file_title,
				)
			new_upload.save()
			new_upload.file.save(file.name, file)

			return HttpResponseRedirect(reverse('upload_list'))
		else:
			return render_to_response('upload_new.html', {'tab':tab,'form': form, 'user':user})
	else:
		return render_to_response('upload_new.html', {'tab':tab,'form': form, 'user':user})

@login_required
def upload_edit(request,id):
	tab = 'upload'
	user = request.user
	form = UploadEditForm()
	upload = Upload.objects.get(id = id)
	initial = {
		'file_title':upload.file_title
		}
	if request.method == 'POST':
		form = UploadEditForm(request.POST, request.FILES)
		if form.is_valid():
			if request.FILES:
				file = request.FILES['file']
				edited_upload.file.save(file.name, file)
			else:
				file = upload.file
			file_title = form.cleaned_data['file_title']
			edited_upload = Upload(
				id = id,
				file_title = file_title,
				file = file,
				)
			edited_upload.save()

			return HttpResponseRedirect(reverse('upload_list'))
		else:
			return render_to_response('upload_new.html', {'tab':tab,'form': form, 'user':user})
	else:
		form = UploadEditForm(initial = initial)
		return render_to_response('upload_new.html', {'tab':tab,'form': form, 'user':user})

@login_required
def upload_new_popup(request):
	tab = 'upload'
	user = request.user
	form = UploadEditForm()
	if request.method == 'POST':
		form = UploadEditForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			file_title = form.cleaned_data['file_title']
			new_upload = Upload(
				file_title = file_title,
				)
			new_upload.save()
			new_upload.file.save(file.name, file)

			return HttpResponse('''
				<script type="text/javascript">
					window.close();
				</script>''')
		else:
			return render_to_response('upload_new.html', {'tab':tab,'form': form, 'user':user})
	else:
		return render_to_response('upload_new.html', {'tab':tab,'form': form, 'user':user})


@login_required
def upload_list(request):
	tab = 'upload'
	user = request.user
	form = SearchForm()
	list = Upload.objects.all()
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			search = request.POST.get('search') 
			if search:
				list = list.filter(Q(file__icontains = search)|Q(file_title__icontains = search))
		return render_to_response('upload_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user})
	else:
		return render_to_response('upload_list.html',{'tab':tab, 'list':list, 'form':form, 'user':user})

@login_required
def upload_view(request, file_name):
	tab = 'upload'
	user = request.user
	#datasheets and drawings are saved as pdf's but have 5 or 11 digit file_names w/o file extensions
	if re.match('uploads/',file_name):
		file_name = re.split('uploads/', file_name)[1]
	if re.match(r'^\d{5}$',file_name) or re.match(r'^\d{11}$',file_name) or re.match(r'^\d{10}$',file_name):
		file_name = file_name+'.pdf'
	if re.match(r'^\d{4}$',file_name):
		file_name = '0'+file_name+'.pdf'
	file = open(UPLOAD_DIR+'/'+file_name, 'rb').read()
	if re.search('.pdf', file_name):
		return HttpResponse(file, mimetype="application/pdf")
	else:
		response = HttpResponse(file)
		response['Content-Disposition'] = 'attachment; filename='+file_name
		return response
		

@login_required
def link_a_file(request, link_type, id):
	form = SearchForm()
	tab = 'upload'
	user = request.user
	if request.method == 'GET':
		list = []
		form = SearchForm(request.GET)
		if form.is_valid():
			search = request.GET.get('search') 
			if search:
				list = Upload.objects.filter(Q(file__icontains = search)|Q(file_title__icontains = search))  
		return render_to_response('link_a_file.html',{'tab':tab, 'list':list, 'form':form, 'user':user, 'link_type':link_type, 'id':id})
	else:
		return render_to_response('link_a_file.html',{'tab':tab, 'form':form, 'user':user, 'link_type':link_type, 'id':id})

@login_required
def link_a_file_confirm(request, link_type, id, upload_id):
	upload = Upload.objects.get(id = upload_id)
	if link_type == 'project':
		if request.method == 'GET':
			project = Project.objects.get(id = id)
			new_link, created = Link2Project.objects.get_or_create(key = project, upload = upload)
			if created:
				new_link.save()
			return HttpResponse('''
				<script type="text/javascript">
					window.close();
				</script>''')
		else:
			return render_to_response('link_a_file_confirm.html', {'project':project, 'upload':upload})
	if link_type == 'battery':
		if request.method == 'GET':
			battery = Battery.objects.get(id = id)
			new_link, created = Link2Battery.objects.get_or_create(key = battery, upload = upload)
			if created:
				new_link.save()
			return HttpResponse('''
				<script type="text/javascript">
					window.close();
				</script>''')
		else:
			return render_to_response('link_a_file_confirm.html', {'project':project, 'upload':upload})
	else:
		return render_to_response('link_a_file_confirm.html', {'project':project, 'upload':upload})

@login_required
def handle_uploaded_file(file):
	user = request.user
	destination = open(settings.MEDIA_ROOT+'uploads/file.txt', 'wb+')
	for chunk in file.chunks():
		destination.write(chunk)
	destination.close()

#SEARCH FUNCTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def ProjectSearch(list, status, division, region, market_segment, customer, battery_search, sales_potential):
	if battery_search:
		list = Project.objects.none()
		if re.match(r'^\d*$', battery_search):
			battery, pack = [], []
			pack = Pack.objects.filter(Q(vkb_number__icontains = battery_search)|Q(drawing_number__icontains = battery_search))
			battery = Battery.objects.filter(type_number__icontains = battery_search)
			if battery:
				for i in battery:
					list = list|Project.objects.filter(battery = i)
			if pack:
				for i in pack:
					list = list|Project.objects.filter(battery_pack = i)
		else:
			list = list|Project.objects.filter(battery_description__icontains = battery_search)
			battery = Battery.objects.filter(type_description__icontains = battery_search)
			if battery:
				for i in battery:
					list = list|Project.objects.filter(battery = i)
	if status != 'None':
		list = list.filter(status = status)
	if division != 'None':
		list = list.filter(division = division)
	if region != 'None':
		list = list.filter(region = region)
	if market_segment != 'None':
		list = list.filter(market_segment = market_segment)
	if customer:
		list = list.filter(customer__icontains = customer)
	if sales_potential:
		list = list.filter(sales_potential__gte = int(sales_potential))
	return list

def BatterySearch(search):
	if re.match(r'^\d*$', search):
		list = Battery.objects.filter(type_number__icontains = search)
	else:
		list = Battery.objects.filter(type_description__icontains = search)

def SampleSearch(search):
	list = Sample.objects.all()
	if search:
		if re.match(r'^\d*$', search):
			battery, pack = [], []
			pack = Pack.objects.filter(Q(vkb_number__icontains = search)|Q(drawing_number__icontains = search))
			battery = Battery.objects.filter(type_number__icontains = search)
			if battery:
				for i in battery:
					if list.filter(battery = i):
						list = list.filter(battery = i)
			if pack:
				for i in pack:
					if list.filter(battery_pack = i):
						list = list.filter(battery_pack = i)
			if not battery and not pack:
				list = []
		else:
			battery = Battery.objects.filter(type_description__icontains = search)
			if battery:
				for i in battery:
					list = list.filter(battery = i)
			else:
				list = list.filter(
					Q(battery_description__icontains = search)|
					Q(engineer__icontains = search)|
					Q(inside_sales__icontains = search)|
					Q(ship_to_company__icontains = search)|
					Q(ship_to_attention__icontains = search)|
					Q(ship_to_address_line1__icontains = search)|
					Q(ship_to_address_line2__icontains = search)|
					Q(ship_to_city__icontains = search)|
					Q(ship_to_state__icontains = search)|
					Q(end_user_company__icontains = search)|
					Q(end_user_attention__icontains = search)|
					Q(end_user_address_line1__icontains = search)|
					Q(end_user_address_line2__icontains = search)|
					Q(end_user_city__icontains = search)|
					Q(end_user_state__icontains = search)
					)
	return list

def ContactSearch(search):
	list = []
	if search:
		list = Contact.objects.filter(Q(firstname__icontains = search)|Q(lastname__icontains = search)|Q(company__icontains = search))
	return list

def QuoteSearch(search):
	if search:
		if re.match(r'^\d*$', search):
			battery, pack = [], []
			pack = Pack.objects.filter(Q(vkb_number__icontains = search)|Q(drawing_number__icontains = search))
			battery = Battery.objects.filter(type_number__icontains = search)
			if battery:
				for i in battery:
					if list.filter(battery = i):
						list = list.filter(battery = i)
			if pack:
				for i in pack:
					if list.filter(battery_pack = i):
						list = list.filter(battery_pack = i)
			if not battery and not pack:
				list = []
		else:
			battery = Battery.objects.filter(type_description__icontains = search)
			if battery:
				for i in battery:
					list = list.filter(battery = i)
			else:
				list = QuoteRow.objects.none()
				list = QuoteRow.objects.filter(
					battery_description__icontains = search
					)
				quote_list = Quote.objects.filter(
					Q(fob__icontains = search)| 
					Q(terms__icontains = search)| 
					Q(signature1_name__icontains = search)| 
					Q(signature1_title__icontains = search)| 
					Q(signature2_name__icontains = search)| 
					Q(signature2_title__icontains = search)| 
					Q(signature3_name__icontains = search)| 
					Q(signature3_title__icontains = search)| 
					Q(customer_company__icontains = search)| 
					Q(customer_attention__icontains = search)| 
					Q(customer_address_line1__icontains = search)| 
					Q(customer_address_line2__icontains = search)| 
					Q(customer_city__icontains = search)| 
					Q(customer_state__icontains = search)| 
					Q(customer_post_code__icontains = search)| 
					Q(customer_email = search)
					)
				if quote_list:
					for i in quote_list:
						list = list|i.quoterow_set.all()
				list = list.order_by('quote')
	else:
		list = QuoteRow.objects.none()
	return list
#FORM HANDLERS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def ProjectEditFormHandler(form):
	if form.is_valid():
		status = form.cleaned_data['status']
		division = form.cleaned_data['division'] 
		region = form.cleaned_data['region'] 
		market_segment = form.cleaned_data['market_segment'] 
		customer = form.cleaned_data['customer'] 
		battery_description = form.cleaned_data['battery_description'] 
		prototype_verification = form.cleaned_data['prototype_verification']
		design_verification = form.cleaned_data['design_verification']
		manufacturing_verification = form.cleaned_data['manufacturing_verification']
		production_verification = form.cleaned_data['production_verification']
		end_of_life = form.cleaned_data['end_of_life']
		battery_description = form.cleaned_data['battery_description'] 
		if form.cleaned_data['vkb_number']:
			battery_pack = form.cleaned_data['vkb_number']
			battery = battery_pack.battery
		else:
			battery_pack = None
		if form.cleaned_data['type_number']: 
			battery = form.cleaned_data['type_number'] 
		if not form.cleaned_data['type_number'] and not form.cleaned_data['vkb_number']:
			battery = None
		if form.cleaned_data['sales_potential']:
			sales_potential = form.cleaned_data['sales_potential']
		else:
			sales_potential = None
		if form.cleaned_data['primary_contact_id']:
			primary_contact = Contact.objects.get(id = form.cleaned_data['primary_contact_id'])
		else:
			primary_contact = None
		if form.cleaned_data['sales_rep_id']:
			sales_rep = Contact.objects.get(id = form.cleaned_data['sales_rep_id'])
		else:
			sales_rep = None
		if form.cleaned_data['project_manager_id']:
			project_manager = Contact.objects.get(id = form.cleaned_data['project_manager_id'])
		else:
			project_manager = None
		notes = form.cleaned_data['notes']
		project = Project(
				status = status,
				division = division, 
				region = region, 
				market_segment = market_segment, 
				customer = customer, 
				battery_description = battery_description, 
				battery_pack = battery_pack, 
				battery = battery, 
				sales_potential = sales_potential, 
				primary_contact =primary_contact , 
				sales_rep =sales_rep , 
				project_manager =project_manager , 
				prototype_verification =prototype_verification ,
				design_verification =design_verification , 
				manufacturing_verification =manufacturing_verification , 
				production_verification =production_verification , 
				end_of_life =end_of_life, 
				notes = notes)
		return project
	else:
		return None

def SampleFormHandler(sample, form, ship_to_form, end_user_form):
	if sample: sample = sample
	else: sample = Sample()
	date = form.cleaned_data['date'] 
	battery_description = form.cleaned_data['battery_description'] 
	engineer = form.cleaned_data['engineer']
	inside_sales = form.cleaned_data['inside_sales']
	ship_to_company = ship_to_form.cleaned_data['required_company'] 
	ship_to_attention = ship_to_form.cleaned_data['required_attention'] 
	ship_to_address_line1 = ship_to_form.cleaned_data['required_address_line1'] 
	ship_to_address_line2 = ship_to_form.cleaned_data['required_address_line2'] 
	ship_to_city = ship_to_form.cleaned_data['required_city'] 
	ship_to_state = ship_to_form.cleaned_data['required_state'] 
	ship_to_post_code = ship_to_form.cleaned_data['required_post_code'] 
	ship_to_phone = ship_to_form.cleaned_data['required_phone'] 
	end_user_company = end_user_form.cleaned_data['non_required_company'] 
	end_user_attention = end_user_form.cleaned_data['non_required_attention'] 
	end_user_address_line1 = end_user_form.cleaned_data['non_required_address_line1'] 
	end_user_address_line2 = end_user_form.cleaned_data['non_required_address_line2'] 
	end_user_city = end_user_form.cleaned_data['non_required_city'] 
	end_user_state = end_user_form.cleaned_data['non_required_state'] 
	end_user_post_code = end_user_form.cleaned_data['non_required_post_code'] 
	end_user_phone = end_user_form.cleaned_data['non_required_phone'] 
	sample.date = date
	sample.battery_description = battery_description
	sample.engineer = engineer
	sample.inside_sales = inside_sales
	sample.ship_to_company = ship_to_company
	sample.ship_to_attention = ship_to_attention
	sample.ship_to_address_line1 = ship_to_address_line1
	sample.ship_to_address_line2 = ship_to_address_line2
	sample.ship_to_city = ship_to_city
	sample.ship_to_state = ship_to_state
	sample.ship_to_post_code = ship_to_post_code
	sample.ship_to_phone = ship_to_phone
	sample.end_user_company = end_user_company
	sample.end_user_attention = end_user_attention
	sample.end_user_address_line1 = end_user_address_line1
	sample.end_user_address_line2 = end_user_address_line2
	sample.end_user_city = end_user_city
	sample.end_user_state = end_user_state
	sample.end_user_post_code = end_user_post_code
	sample.end_user_phone = end_user_phone
	return sample

def ContactEditFormHandler(form):
	firstname = form.cleaned_data['firstname']
	lastname = form.cleaned_data['lastname']
	company = form.cleaned_data['company']
	title = form.cleaned_data['title']
	cell = form.cleaned_data['cell']
	landline = form.cleaned_data['landline']
	fax = form.cleaned_data['fax']
	email = form.cleaned_data['email']
	primary_address_line1 = form.cleaned_data['primary_address_line1']
	primary_address_line2 = form.cleaned_data['primary_address_line2']
	primary_state = form.cleaned_data['primary_state']
	primary_city = form.cleaned_data['primary_city']
	primary_post_code = form.cleaned_data['primary_post_code']
	secondary_address_line1 = form.cleaned_data['secondary_address_line1']
	secondary_address_line2 = form.cleaned_data['secondary_address_line2']
	secondary_state = form.cleaned_data['secondary_state']
	secondary_city = form.cleaned_data['secondary_city']
	secondary_post_code = form.cleaned_data['secondary_post_code']
	cell = form.cleaned_data['cell']
	landline = form.cleaned_data['landline']
	fax = form.cleaned_data['fax']
	contact = Contact(
		firstname = firstname,
		lastname = lastname,
		company = company,
		title = title,
		cell = cell,
		landline = landline ,
		fax = fax ,
		email = email ,
		primary_address_line1 = primary_address_line1 ,
		primary_address_line2 = primary_address_line2 ,
		primary_state = primary_state ,
		primary_city = primary_city ,
		primary_post_code = primary_post_code ,
		secondary_address_line1 = secondary_address_line1 ,
		secondary_address_line2 = secondary_address_line2 ,
		secondary_state = secondary_state ,
		secondary_city = secondary_city ,
		secondary_post_code = secondary_post_code 
			)
	return contact

def BatteryEditFormHandler(form, battery, datasheet):
	if battery: id = battery.id
	else: id = None
	type_number = form.cleaned_data['type_number']
	type_description = form.cleaned_data['type_description']
	chemistry = form.cleaned_data['chemistry']
	type = form.cleaned_data['type']
	capacity = form.cleaned_data['capacity']
	voltage = form.cleaned_data['voltage']
	max_cont = form.cleaned_data['max_cont']
	max_pulse = form.cleaned_data['max_pulse']
	min_storage_temp = form.cleaned_data['min_storage_temp']
	max_storage_temp = form.cleaned_data['max_storage_temp']
	min_discharge_temp = form.cleaned_data['min_discharge_temp']
	max_discharge_temp = form.cleaned_data['max_discharge_temp']
	min_charge_temp = form.cleaned_data['min_charge_temp']
	max_charge_temp = form.cleaned_data['max_charge_temp']
	discontinued = form.cleaned_data['discontinued']
	battery = Battery(
		id = id,
		type_number = type_number,
		type_description = type_description,
		chemistry = chemistry,
		type = type,
		capacity = capacity,
		voltage = voltage,
		max_cont = max_cont,
		max_pulse = max_pulse,
		min_storage_temp = min_storage_temp,
		max_storage_temp = max_storage_temp,
		min_discharge_temp = min_discharge_temp,
		max_discharge_temp = max_discharge_temp,
		min_charge_temp = min_charge_temp,
		max_charge_temp = max_charge_temp,
		discontinued = discontinued,
		datasheet = datasheet
		)
	return battery

def PackEditFormHandler(pack, form, vkb_form, drawing):
	if not pack: pack = Pack() 
	drawing_number = form.cleaned_data['drawing_number']
	vkb_number,battery = vkb_form.cleaned_data['vkb_number']
	chemistry = form.cleaned_data['chemistry']
	type = form.cleaned_data['type']
	configuration = form.cleaned_data['configuration']
	connection = form.cleaned_data['connection']
	series_cells = form.cleaned_data['series_cells']
	parallel_cells = form.cleaned_data['parallel_cells']
	capacity = form.cleaned_data['capacity']
	voltage = form.cleaned_data['voltage']
	max_cont = form.cleaned_data['max_cont']
	max_pulse = form.cleaned_data['max_pulse']
	pack.battery = battery
	pack.vkb_number = vkb_number
	pack.drawing_number = drawing_number
	pack.chemistry = chemistry
	pack.type = type
	pack.configuration = configuration
	pack.connection = connection
	pack.series_cells = series_cells
	pack.parallel_cells = parallel_cells
	pack.capacity = capacity
	pack.voltage = voltage
	pack.max_cont = max_cont
	pack.max_pulse = max_pulse
	return pack

def QuoteEditFormHandler(form, customer_form):
	date = form.cleaned_data['date'] 
	inquiry_date = form.cleaned_data['inquiry_date'] 
	rows = form.cleaned_data['rows']
	fob = form.cleaned_data['fob']
	terms = form.cleaned_data['terms']
	customer_company = customer_form.cleaned_data['required_company'] 
	customer_attention = customer_form.cleaned_data['required_attention'] 
	customer_address_line1 = customer_form.cleaned_data['required_address_line1'] 
	customer_address_line2 = customer_form.cleaned_data['required_address_line2'] 
	customer_city = customer_form.cleaned_data['required_city'] 
	customer_state = customer_form.cleaned_data['required_state'] 
	customer_post_code = customer_form.cleaned_data['required_post_code'] 
	customer_phone = customer_form.cleaned_data['required_phone'] 
	customer_fax = customer_form.cleaned_data['required_fax'] 
	customer_email = customer_form.cleaned_data['required_email'] 
	signature1 = form.cleaned_data['signature1']
	signature1_title = form.cleaned_data['signature1_title']
	signature2 = form.cleaned_data['signature2']
	signature2_title = form.cleaned_data['signature2_title']
	signature3 = form.cleaned_data['signature3']
	signature3_title = form.cleaned_data['signature3_title']
	quote_number = Quote.get_quote_number()
	quote = Quote(
		project = project,
		quote_number = quote_number,
		date = date,
		author = Contact.objects.get(user = user),
		editor = Contact.objects.get(user = user),
		authored_date = date,
		edited_date = date,
		fob = fob,
		terms = terms,
		inquiry_date = inquiry_date,
		signature1_name = signature1,
		signature1_title = signature1_title,
		signature2_name = signature2,
		signature2_title = signature2_title,
		signature3_name = signature3,
		signature3_title = signature3_title,
		customer_company = customer_company,
		customer_attention = customer_attention,
		customer_address_line1 = customer_address_line1,
		customer_address_line2 = customer_address_line2,
		customer_city = customer_city,
		customer_state = customer_state,
		customer_post_code = customer_post_code,
		customer_phone = customer_phone,
		customer_fax = customer_fax,
		customer_email = customer_email,
		)
	return quote
#FORM INITIALIZERS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def InitializeProjectEditForm(project):
	initial = {
		'status':project.status,
		'division':project.division,
		'region':project.region,
		'market_segment':project.market_segment,
		'customer':project.customer,
		'battery_description':project.battery_description,
		'sales_potential':project.sales_potential,
		'prototype_verification':project.prototype_verification,
		'design_verification':project.design_verification,
		'manufacturing_verification':project.manufacturing_verification,
		'production_verification':project.production_verification,
		'end_of_life':project.end_of_life,
		'notes':project.notes
		}
	if project.battery:
		initial['type_number'] = project.battery.type_number
	if project.battery_pack:
		initial['vkb_number'] = project.battery_pack.vkb_number
	if project.primary_contact:
		initial['primary_contact_name']= project.primary_contact.firstname+' '+project.primary_contact.lastname
		initial['primary_contact_id']=project.primary_contact.id
	if project.sales_rep:
		initial['sales_rep_name']=project.sales_rep.firstname+' '+project.sales_rep.lastname
		initial['sales_rep_id']=project.sales_rep.id
	if project.project_manager:
		initial['project_manager_name']=project.project_manager.firstname+' '+project.project_manager.lastname
		initial['project_manager_id']=project.project_manager.id
	return initial

def InitializeContactEditForm(contact):
	initial = {
		'firstname':contact.firstname, 
		'lastname':contact.lastname, 
		'company':contact.company, 
		'title':contact.title, 
		'cell':contact.cell, 
		'landline':contact.landline, 
		'fax':contact.fax, 
		'email':contact.email, 
		'primary_address_line1':contact.primary_address_line1, 
		'primary_address_line2':contact.primary_address_line2, 
		'primary_state':contact.primary_state, 
		'primary_city':contact.primary_city, 
		'primary_post_code':contact.primary_post_code, 
		'secondary_address_line1':contact.secondary_address_line1, 
		'secondary_address_line2':contact.secondary_address_line2, 
		'secondary_state':contact.secondary_state, 
		'secondary_city':contact.secondary_city, 
		'secondary_post_code':contact.secondary_post_code
		}
	return initial

def InitializeBatteryEditForm(battery):
	initial = {
		'datasheet':battery.datasheet, 
		'type_number':battery.type_number, 
		'type_description':battery.type_description, 
		'chemistry':battery.chemistry, 
		'type':battery.type, 
		'capacity':battery.capacity, 
		'voltage':battery.voltage, 
		'max_cont':battery.max_cont, 
		'max_pulse':battery.max_pulse, 
		'min_storage_temp':battery.min_storage_temp, 
		'max_storage_temp':battery.max_storage_temp, 
		'min_discharge_temp':battery.min_discharge_temp, 
		'max_discharge_temp':battery.max_discharge_temp, 
		'min_charge_temp':battery.min_charge_temp, 
		'max_charge_temp':battery.max_charge_temp, 
		'discontinued':battery.discontinued 
		}
	return initial

def InitializeSampleEditForm(o):
	if type(o).__name__ == 'Project':
		project = o
		form = SampleEditForm(initial = {
			'date' : today,
			'battery' : project.battery_description
			})
		if project.sales_rep and project.primary_contact:
			end_user_form = NonRequiredAddressForm(initial = {
					'non_required_company' : project.primary_contact.company,
					'non_required_attention' : project.primary_contact.firstname+" "+project.primary_contact.lastname,
					'non_required_address_line1' : project.primary_contact.primary_address_line1,
					'non_required_address_line2' : project.primary_contact.primary_address_line2,
					'non_required_city' : project.primary_contact.primary_city,
					'non_required_state' : project.primary_contact.primary_state,
					'non_required_post_code' : project.primary_contact.primary_post_code,
					'non_required_phone' : project.primary_contact.landline,
					'non_required_id' : project.primary_contact.id
					})
			ship_to_form = RequiredAddressForm(initial = {
					'required_company' : project.sales_rep.company,
					'required_attention' : project.sales_rep.firstname+" "+project.sales_rep.lastname,
					'required_address_line1' : project.sales_rep.primary_address_line1,
					'required_address_line2' : project.sales_rep.primary_address_line2,
					'required_city' : project.sales_rep.primary_city,
					'required_state' : project.sales_rep.primary_state,
					'required_post_code' : project.sales_rep.primary_post_code,
					'required_phone' : project.sales_rep.landline,
					'required_id' : project.sales_rep.id
					})
		elif project.primary_contact:
			ship_to_form = RequiredAddressForm(initial = {
					'required_company' : project.primary_contact.company,
					'required_attention' : project.primary_contact.firstname+" "+project.primary_contact.lastname,
					'required_address_line1' : project.primary_contact.primary_address_line1,
					'required_address_line2' : project.primary_contact.primary_address_line2,
					'required_city' : project.primary_contact.primary_city,
					'required_state' : project.primary_contact.primary_state,
					'required_post_code' : project.primary_contact.primary_post_code,
					'required_phone' : project.primary_contact.landline,
					'required_id' : project.primary_contact.id
					})
			end_user_form = NonRequiredAddressForm()
		else:
			ship_to_form = RequiredAddressForm()
			end_user_form = NonRequiredAddressForm()
		return form, ship_to_form, end_user_form
	elif type(o).__name__ == 'Sample':
		sample = o
		form = SampleEditForm(initial = {
				'date' : sample.date,
				'engineer' : sample.engineer,
				'inside_sales' : sample.inside_sales,
				'battery_description' : sample.battery_description,
				})
		end_user_form = NonRequiredAddressForm(initial = {
				'non_required_company' : sample.end_user_company,
				'non_required_attention' : sample.end_user_attention,
				'non_required_address_line1' : sample.end_user_address_line1,
				'non_required_address_line2' : sample.end_user_address_line2 ,
				'non_required_city' : sample.end_user_city,
				'non_required_state' : sample.end_user_state,
				'non_required_post_code' : sample.end_user_post_code,
				'non_required_phone' : sample.end_user_phone,
				'non_required_id' : sample.end_user_contact_id,
				})
		ship_to_form = RequiredAddressForm(initial = {
				'required_company' : sample.ship_to_company,
				'required_attention' : sample.ship_to_attention,
				'required_address_line1' : sample.ship_to_address_line1,
				'required_address_line2' : sample.ship_to_address_line2,
				'required_city' : sample.ship_to_city,
				'required_state' : sample.ship_to_state,
				'required_post_code' : sample.ship_to_post_code,
				'required_phone' : sample.ship_to_phone,
				'required_id' : sample.ship_to_contact_id,
				})
		return form, ship_to_form, end_user_form
	else:
		form, ship_to_form, end_user_form = None,  None,  None  
		return form, ship_to_form, end_user_form

def InitializePackEditForm(pack):
	form = PackEditForm(initial = {
			'drawing_number':pack.drawing_number,
			'chemistry':pack.chemistry, 
			'type':pack.type, 
			'configuration':pack.configuration, 
			'series_cells':pack.series_cells, 
			'parallel_cells':pack.parallel_cells, 
			'connection':pack.connection, 
			'capacity':pack.capacity, 
			'voltage':pack.voltage, 
			'max_cont':pack.max_cont, 
			'max_pulse':pack.max_pulse 
		})
	vkb_form = VKBForm(initial = {
			'vkb_number':pack.vkb_number, 
		})
	return form, vkb_form

def InitializeProjectForm(project):
	if project.primary_contact:
		initial = {
		'required_company' : project.primary_contact.company,
		'required_attention' : project.primary_contact.firstname+" "+project.primary_contact.lastname,
		'required_address_line1' : project.primary_contact.primary_address_line1,
		'required_address_line2' : project.primary_contact.primary_address_line2,
		'required_city' : project.primary_contact.primary_city,
		'required_state' : project.primary_contact.primary_state,
		'required_post_code' : project.primary_contact.primary_post_code,
		'required_phone' : project.primary_contact.landline,
		'required_fax' : project.primary_contact.fax,
		'required_email' : project.primary_contact.email,
		'required_id' : project.primary_contact.id,
		}
	else:
		initial = {}
	customer_form = RequiredAddressForm(initial = initial)
	today = datetime.date.today()
	form = QuoteEditForm(initial = {
		'date' : today,
		'inquiry_date' : today,
		'terms' : 'Net 30',
		'fob' : 'Harrisburg, PA'
		})
	return form, customer_form
#WORD DOC FUNCTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def SampleWordDoc(sample):
	c = Context({'sample':sample})
	t = loader.get_template('xml/sample-base.xml')
	render_xml = t.render(c)
	response = HttpResponse(render_xml, mimetype='application/ms-word')
	response['Content-Disposition'] = 'attachment; filename='+sample.ship_to_attention+'-sample.doc'
	return response
