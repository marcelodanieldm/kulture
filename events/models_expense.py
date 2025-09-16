from django.db import models
from events.models import Event

class Expense(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='expenses')
    concept = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.concept} - ${self.amount} ({self.event.name})"
