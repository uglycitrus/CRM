from myproject.opmlist.models import Contact
from myproject.opmlist.models import Battery
from myproject.opmlist.models import Pack
from myproject.opmlist.models import Sample
from myproject.opmlist.models import Quote
from myproject.opmlist.models import QuoteRow
from myproject.opmlist.models import SPR
from myproject.opmlist.models import SPRRow
from myproject.opmlist.models import Project
from myproject.opmlist.models import Link
from django.contrib import admin

admin.site.register(Contact)
admin.site.register(Battery)
admin.site.register(Pack)
admin.site.register(Sample)
admin.site.register(Quote)
admin.site.register(QuoteRow)
admin.site.register(SPR)
admin.site.register(SPRRow)
admin.site.register(Project)
admin.site.register(Link)
