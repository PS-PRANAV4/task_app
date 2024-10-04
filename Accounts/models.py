from django.db import models


class EmailOtp(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=10)
    verify_signature = models.CharField(max_length=12,null=True,blank=True)


class OtpLogin(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=10)