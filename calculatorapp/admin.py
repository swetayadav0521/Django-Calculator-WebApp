from django.contrib import admin
from calculatorapp.models import History

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'result', 'creation_date_time',)

admin.site.register(History, HistoryAdmin)
