from django.db import models
from events.models import Event

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    buyer_name = models.CharField(max_length=100)
    buyer_email = models.EmailField()
    seats_reserved = models.PositiveIntegerField(default=1)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer_name} - {self.event.name} - ${self.amount_paid}"
