from django.db import models

# Create your models here.
# tickets/models.py

from django.db import models
from events.models import Event
from users.models import CustomUser

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    seat_numbers = models.JSONField(default=list)  # ["A1", "A2", ...]

    def __str__(self):
        return f"{self.buyer.username} - {self.event.name}"

class PaymentSummary(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    @property
    def profit(self):
        return self.total_revenue - self.total_expenses

    def __str__(self):
        return f"Balance: {self.event.name}"
