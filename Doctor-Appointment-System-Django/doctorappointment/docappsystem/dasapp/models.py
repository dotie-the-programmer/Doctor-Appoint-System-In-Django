from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER = {
        (1, 'admin'),
        (2, 'doc'),
    }
    user_type = models.CharField(choices=USER, max_length=4, default=1)
    profile_pic = models.ImageField(upload_to='profile_pic/')

class Specialization(models.Model):
    sname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sname

class DoctorReg(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    mobilenumber = models.CharField(max_length=11)
    specialization_id = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}" if self.admin else f"User not associated - {self.mobilenumber}"

class Appointment(models.Model):
    appointmentnumber = models.IntegerField(default=0)
    fullname = models.CharField(max_length=250)
    mobilenumber = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    date_of_appointment = models.DateField()
    time_of_appointment = models.TimeField()
    doctor_id = models.ForeignKey(DoctorReg, on_delete=models.CASCADE)
    additional_msg = models.TextField(blank=True)
    remark = models.CharField(max_length=250, default='')
    status = models.CharField(max_length=200, default='')
    prescription = models.TextField(blank=True, default='')
    recommendedtest = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment #{self.appointmentnumber} - {self.fullname}"

class Page(models.Model):
    pagetitle = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    aboutus = models.TextField()
    email = models.EmailField(max_length=200)
    mobilenumber = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pagetitle
