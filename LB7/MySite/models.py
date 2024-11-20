from django.db import models
from django.contrib.auth.models import User


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bets")
    outcome = models.CharField(max_length=20, choices=[('win', 'Win'), ('loss', 'Loss'), ('draw', 'Draw')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class SportsCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    category = models.ForeignKey(SportsCategory, on_delete=models.CASCADE, related_name="votes")
    team = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} voted for {self.team} in {self.category.name}"


class Match(models.Model):
    category = models.ForeignKey(SportsCategory, on_delete=models.CASCADE, related_name="matches")
    team_a = models.CharField(max_length=100)
    team_b = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.team_a} vs {self.team_b} ({self.category.name})"
