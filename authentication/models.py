from typing import Iterable, Optional
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone  # Import timezone from django.utils
from django.core.serializers.base import Serializer

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
    def medium_points(self):
        # punctaj mediu
        # expected a medium of points per solved grids of a chapter
        # ex: Boliile Hepatice: 3.0,
        #     Cardiologie:      1.0,
        return None
    
    @property
    def progress(self):
        # only from learning
        # last uncompleted learning session
        # return chapter_name, 'nr_solved_questions/total_nr_questions' (as string)
        return None
    
    @property
    def kumar_solved_precentage(self):
        # only from test
        return 0
    
    @property
    def chirurgie_solved_precentage(self):
        # only from test
        return 0
    
    @property
    def sinopsis_solved_precentage(self):
        # only from test
        return 0
    
    @property
    def total_grids_solved(self):
        # both from learn and test categories
        return 0
    
    @property
    def total_kumar_grids_solved(self):
        # both from learn and test categories
        return 0
    
    @property
    def total_chirurgie_grids_solved(self):
        # both from learn and test categories
        return 0
    
    @property
    def total_sinopsis_grids_solved(self):
        # both from learn and test categories
        return 0
    
    @property
    def global_points(self):
        # both from learn and test categories
        return 0
    
    @property
    def last_unfinished_challenge_progress(self):
        # only from test
        return None
    
    @property
    def todo_tasks(self):
        # order by last completed 
        # (the last completed should be the first showed in the list)
        return self.todotask_set.order_by('-is_completed', '-is_completed_date', 'deadline')

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


class TodoTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    is_completed_date = models.DateTimeField(null=True, blank=True)

    @property
    def formatted_deadline(self):
        if self.deadline:
            return self.deadline.strftime('%b. %d, %Y')
        return ""
    
    def save(self, *args, **kwargs):
        # Check if the object is already in the database (has a primary key)
        if self.pk:
            original_task = TodoTask.objects.get(pk=self.pk)
            if not original_task.is_completed and self.is_completed:
                self.is_completed_date = timezone.now()
        super(TodoTask, self).save(*args, **kwargs)


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
