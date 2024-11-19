from django.db import models
from django.contrib.auth.models import User


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bets")
    outcome = models.CharField(max_length=20, choices=[('win', 'Win'), ('loss', 'Loss'), ('draw', 'Draw')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.outcome} - {self.amount}"
