from turtle import end_fill
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class Contract(models.Model):
    title = models.CharField(max_length=30)
    aim = models.CharField(max_length=300)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='refCont')
    referee2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='ref2Cont') #incline default

    sub_freq = models.IntegerField()
    sub_tolerance = models.FloatField(default=0.1)

    f_recipient = models.CharField(max_length=50)

    end_date = models.DateField()
    vote_deadline = models.DateField()
    wager = models.IntegerField()
    def __str__(self):
        return self.title
    #In actual contract: User & Referee 2 & 3 (with password hashes), vote_deadline, f_recipient
    #to lose 20kg by 12/10/2022


class ContractInfManager(models.Manager):
    def create_progress(self, contract, description, notes, date, file):
        ContractProgress = self.create(contract=contract, description=description, notes=notes, date=date, file=file)
        return ContractProgress

class ContractProgress(models.Model):

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)
    notes = models.CharField(max_length=300, blank=False)
    date = models.DateField()
    file = models.FileField(null=True)

    objects = ContractInfManager()

    def __str__(self):
        return self.description