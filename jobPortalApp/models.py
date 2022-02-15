from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
# Create your models here.

# maverick


class SEEKER(models.Model):
    user_id = models.IntegerField(null=True)
    username = models.TextField(null=True)
    fullname = models.CharField(max_length=255, null=True)
    experience = models.TextField(null=True)
    about = models.TextField(null=True)
    status = models.TextField(null=True)

    def __str__(self):
        return self.username

# maverick


class COMPANY(models.Model):
    user_id = models.IntegerField(null=True)
    username = models.TextField(null=True)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    status = models.TextField(null=True)

    def __str__(self):
        return self.username


class SKILL(models.Model):
    skillname = models.TextField(unique=True)

    def __str__(self):
        return self.skillname


class SEEKERSKILL(models.Model):
    skill_id = models.IntegerField()
    user_id = models.IntegerField()


class JOBSKILL(models.Model):
    skill_id = models.IntegerField()
    job_id = models.IntegerField()


class RESUME(models.Model):
    user_id = models.IntegerField(null=True)
    resume = models.FileField(upload_to=settings.MEDIA_ROOT, null=True,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])


class JOB(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.IntegerField()
    type = models.CharField(max_length=255)
    company_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.TextField(null=True)

    def __str__(self):
        return self.name


class APPLICATION(models.Model):
    user_id = models.IntegerField(null=True)
    job_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class PROFILE(models.Model):
    user_id = models.IntegerField(null=True)
    profile = models.FileField(upload_to=settings.MEDIA_ROOT, null=True)

class ACTIVITY(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    user_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)