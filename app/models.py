from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Suggestion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),  # Admin hasn't reviewed it yet
        ('approved', 'Approved'),  # Admin has approved it
        ('rejected', 'Rejected'),  # Admin has rejected it
    ]

    suggestion = models.CharField(max_length=1000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"{self.suggestion} ({self.get_status_display()})"

#13.09.2024 Schema for participant - suggestion - rating.
class Rating(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)  # Regular user as a participant
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('participant', 'suggestion')

    def __str__(self):
        return f"{self.participant.username} rated {self.suggestion.suggestion} as {self.rating}"
