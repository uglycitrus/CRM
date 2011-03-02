from django import forms
from myproject.opmlist.models import Pack
from myproject.opmlist.models import Battery
import re

class VKBField(forms.Field):
	def clean(self, value):
		"""
		check that a VKB# is 10 or 11 digits, and there's a Pack with the entered VKB#
		"""
		if value:
			if not re.match(r'^\d{10}$',value) and not re.match(r'^\d{11}$',value):
				raise forms.ValidationError('VKB# must be 10 or 11 digits')
			if re.match(r'^\d{10}$',value) or re.match(r'^\d{11}$',value):
				match = Pack.objects.filter(vkb_number = value)
				if match:
					value = match[0]
				else:
					raise forms.ValidationError('VKB# does not exist')
		return value

class New_VKBField(forms.Field):
	def clean(self, value):
		"""
		check that a VKB# is 10 or 11 digits, and there's a Battery with a type_number matching the beginning of the VKB#
		"""
		if not re.match(r'^\d{10}$',value) and not re.match(r'^\d{11}$',value):
			raise forms.ValidationError('VKB# must be 10 or 11 digits')
		if re.match(r'^\d{10}$',value):
			type_number = int(str(value)[0:4])
		if re.match(r'^\d{11}$',value):
			type_number = int(str(value)[0:5])
		battery = Battery.objects.filter(type_number = type_number)[0]
		if not battery:
			raise forms.ValidationError('cannot match first digits of vkb# to a battery')
		return value, battery

class TypeField(forms.Field):
	def clean(self, value):
		"""
		check that a type# is 4 or 5 digits and finds existing battery
		"""
		if value:
			if not re.match(r'^\d{4}$',value) and not re.match(r'^\d{5}$',value):
				raise forms.ValidationError('Type# must be 4 or 5 digits')
			if re.match(r'^\d{4}$',value) or re.match(r'^\d{5}$',value):
				match = Battery.objects.filter(type_number = value)
				if match:
					value = match[0]
				else:
					raise forms.ValidationError('Type# does not exist')
		return value

class New_TypeField(forms.Field):
	def clean(self, value):
		"""
		check that a Type# is 4 or 5 digits
		"""
		if value:
			if not re.match(r'^\d{4}$',value) and not re.match(r'^\d{5}$',value):
				raise forms.ValidationError('Type# must be 4 or 5 digits')
		return value

class DrawingField(forms.Field):
	def clean(self, value):
		"""
		check that a Drawing# is 5 or 6 digits
		"""
		if value:
			if not re.match(r'^\d{6}$',value) and not re.match(r'^\d{5}', value):
				raise forms.ValidationError('Type# must be 5 or 6 digits')
		return value
