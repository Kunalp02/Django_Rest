from django.contrib import admin
from api.models import ChoiceList, People, PeopleChoice

admin.site.register(ChoiceList)
admin.site.register(People)
admin.site.register(PeopleChoice)