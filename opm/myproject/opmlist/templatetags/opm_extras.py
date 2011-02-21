from django import template
from django.db.models import get_model
from django.template import Node, NodeList, Template, Context, Variable
from django.template import TemplateSyntaxError, VariableDoesNotExist

from myproject.opmlist.models import Sample
from myproject.opmlist.models import Project
from myproject.opmlist.models import Battery
from myproject.opmlist.models import Quote
from myproject.opmlist.models import SPR
from myproject.opmlist.models import Link2Project
from myproject.opmlist.models import Link2Battery

register = template.Library()

def extend_samples(parser, token):
	bits = token.split_contents()
	if len(bits) != 2 and len(bits) != 3:
		raise template.TemplateSyntaxError("'extend_samples' tag takes two or three arguments")
	project_id = bits[1]
	if len(bits) == 3:
		limit = bits[2]
	else:
		limit = None
	return ExtendSamplesNode(project_id, limit)

class ExtendSamplesNode(template.Node):
	def __init__(self, project_id, limit):
		self.project_id = Variable(project_id)
		self.limit = limit

	def render(self, context):
		try:
			project_id = self.project_id.resolve(context)
		except VariableDoesNotExist:
			project_id = None
		project = Project.objects.get(id = project_id)
		if self.limit != None:
			context['samples'] = project.sample_set.all()[0:int(self.limit)]
		else:
			context['samples'] = project.sample_set.all()
		context['count'] = project.sample_set.count()
		return '' 

def extend_quotes(parser, token):
	bits = token.split_contents()
	if len(bits) != 2 and len(bits) != 3:
		raise template.TemplateSyntaxError("'extend_quotes' tag takes two or three arguments")
	project_id = bits[1]
	if len(bits) == 3:
		limit = bits[2]
	else:
		limit = None
	return ExtendQuotesNode(project_id, limit)

class ExtendQuotesNode(template.Node):
	def __init__(self, project_id, limit):
		self.project_id = Variable(project_id)
		self.limit = limit

	def render(self, context):
		try:
			project_id = self.project_id.resolve(context)
		except VariableDoesNotExist:
			project_id = None
		project = Project.objects.get(id = project_id)
		if self.limit != None:
			context['quotes'] = project.quote_set.all()[0:int(self.limit)]
		else:
			context['quotes'] = project.quote_set.all()
		context['count'] = project.quote_set.count()
		return '' 

def extend_quote_rows(parser, token):
	bits = token.split_contents()
	if len(bits) != 2:
		raise template.TemplateSyntaxError("'extend_quote_rows' tag takes exactly two arguments")
	quote_number = bits[1]
	return ExtendQuoteRowsNode(quote_number)

class ExtendQuoteRowsNode(template.Node):
	def __init__(self, quote_number):
		self.quote_number = Variable(quote_number)

	def render(self, context):
		try:
			quote_number = self.quote_number.resolve(context)
		except VariableDoesNotExist:
			quote_number = None
		quote = Quote.objects.get(quote_number = quote_number)
		context['quote_rows'] = quote.quoterow_set.all()
		return '' 

#SPR EXTENSIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def extend_spr(parser, token):
	bits = token.split_contents()
	if len(bits) != 2 and len(bits) != 3:
		raise template.TemplateSyntaxError("'extend_samples' tag takes two or three arguments")
	project_id = bits[1]
	if len(bits) == 3:
		limit = bits[2]
	else:
		limit = None
	return ExtendSprsNode(project_id, limit)

class ExtendSprsNode(template.Node):
	def __init__(self, project_id, limit):
		self.project_id = Variable(project_id)
		self.limit = limit

	def render(self, context):
		try:
			project_id = self.project_id.resolve(context)
		except VariableDoesNotExist:
			project_id = None
		project = Project.objects.get(id = project_id)
		if self.limit != None:
			context['spr_list'] = project.spr_set.all()[0:int(self.limit)]
		else:
			context['spr_list'] = project.spr_set.all()
		context['count'] = project.spr_set.count()
		return '' 

def extend_spr_rows(parser, token):
	bits = token.split_contents()
	if len(bits) != 2:
		raise template.TemplateSyntaxError("'extend_spr_rows' tag takes exactly two arguments")
	spr_number = bits[1]
	return ExtendSprRowsNode(spr_number)

class ExtendSprRowsNode(template.Node):
	def __init__(self, spr_number):
		self.spr_number = Variable(spr_number)

	def render(self, context):
		try:
			spr_number = self.spr_number.resolve(context)
		except VariableDoesNotExist:
			spr_number = None
		spr = SPR.objects.get(spr_number = spr_number)
		context['spr_rows'] = spr.sprrow_set.all()
		return '' 

def extend_files(parser, token):
	bits = token.split_contents()
	if len(bits) != 3 and len(bits) != 4:
		raise template.TemplateSyntaxError("'extend_files' tag takes three or four arguments")
	type = bits[1]
	id = bits[2]
	if len(bits) == 4:
		limit = bits[3]
	else:
		limit = None
	return ExtendFilesNode(type, id, limit)

class ExtendFilesNode(template.Node):
	def __init__(self, type, id, limit):
		self.type = Variable(type)
		self.id = Variable(id)
		self.limit = limit

	def render(self, context):
		try:
			id = self.id.resolve(context)
			type = self.type.resolve(context)
		except VariableDoesNotExist:
			id = None
		if type == 'Project':
			project = Project.objects.get(id = int(id))
			if self.limit != None:
				context['files'] = project.link2project_set.all()[0:int(self.limit)]
			else:
				context['files'] = project.link2project_set.all()
				context['count'] = project.link2project_set.count()
		if type == 'Battery':
			battery = Battery.objects.get(id = int(id))
			if self.limit != None:
				context['files'] = battery.link2battery_set.all()[0:int(self.limit)]
			else:
				context['files'] = battery.link2battery_set.all()
				context['count'] = battery.link2battery_set.count()
		return '' 

register.tag('extend_files',extend_files)
register.tag('extend_samples',extend_samples)
register.tag('extend_quotes',extend_quotes)
register.tag('extend_quote_rows', extend_quote_rows)
register.tag('extend_spr',extend_spr)
register.tag('extend_spr_rows', extend_spr_rows)
