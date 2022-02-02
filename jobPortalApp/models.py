from django.db import models
from django.conf import settings

# Create your models here.


# maverick
class SEEKER(models.Model):
    username = models.TextField()
    email = models.TextField()
    fullname = models.CharField(max_length=255, null=True)
    experience = models.TextField(null=True)
    about = models.TextField( null=True)
    resume = models.FileField(upload_to=settings.MEDIA_ROOT, null=True) 

    def __str__(self):
        return self.username
# maverick
class COMPANY(models.Model):
    username = models.TextField()
    email = models.TextField()
    name = models.CharField(max_length=255, null=True)
    description = models.TextField( null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username