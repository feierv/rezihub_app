from typing import Iterable, Optional
from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta


class User(AbstractUser):
    '''This is the custom User class, here we add new user fields'''
    STEP_ONE = '1'
    STEP_TWO = '2'
    STEP_THREE = '3'
    STEP_FOUR = '4'

    email = models.CharField(max_length=100, unique=True)

    university = models.ForeignKey('University', on_delete=models.SET_NULL, null=True, blank=True)
    specialitate = models.ForeignKey('Speciality', on_delete=models.SET_NULL, null=True, blank=True)
    oras = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def personal_data(self):
        if hasattr(self, 'userdata'):
            user_data = getattr(self, 'userdata')
            return dict(
                nume=user_data.nume,
                prenume=user_data.prenume,
                phone=user_data.phone,
                localitate=user_data.localitate,
                judet=user_data.judet,
                strada=user_data.strada,
                numar=user_data.numar,
            )
        return None

    @property
    def last_uncompleted_step(self):
        def get_last_uncompleted_step():
            if not self.personal_data:
                return self.STEP_ONE
            if not self.university:
                return self.STEP_TWO
            if not self.specialitate:
                return self.STEP_THREE
            if not self.oras:
                return self.STEP_FOUR
            # no uncompleted steps
            return None
        return get_last_uncompleted_step()
            

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nume = models.CharField(max_length=100)
    prenume = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    localitate = models.CharField(max_length=100)
    judet = models.CharField(max_length=100)
    strada = models.CharField(max_length=100)
    numar = models.CharField(max_length=100)


class Speciality(models.Model):
    category = models.CharField(max_length=100)
    nume = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nume

class City(models.Model):
    nume = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nume

class University(models.Model):
    nume = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nume
