from django.db import models

# Create your models here.
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    sub_date = models.DateField(auto_now_add=True, db_index=True)
    message = models.TextField(max_length=1000)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.sub_date}"

    class Meta:
        ordering = ['-sub_date']