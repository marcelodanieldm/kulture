from django.contrib import admin

from .models import Event
from .models_ticket import Ticket
from .models_expense import Expense

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Expense)
