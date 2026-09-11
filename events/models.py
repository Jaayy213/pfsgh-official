from django.db import models


class RSVP(models.Model):
    ATTENDANCE_CHOICES = [
        ('yes', 'Yes, I will attend in-person'),
        ('no', 'Regretfully, I cannot attend'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    attendance = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    dietary_requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'RSVP'
        verbose_name_plural = 'RSVPs'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company}"