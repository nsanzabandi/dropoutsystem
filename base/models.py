from os import name
from pyexpat import model
from time import timezone
from tkinter import CASCADE
from django.db import models


class District(models.Model):
    d_name = models.CharField(max_length=30)

    def __str__(self):
        return self.d_name
    class Meta:
        db_table='district'


class Sector(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    s_name = models.CharField(max_length=20)

    def __str__(self):
        return self.s_name
    class Meta:
        db_table='sector'


Gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)


YearDropped = (
    ('2010', '2010'),
    ('2011', '2011'),
    ('2012', '2012'),
    ('2013', '2013'),
    ('2014', '2014'),
    ('2015', '2015'),
    ('2016', '2016'),
    ('2017', '2017'),
    ('2018', '2018'),
    ('2019', '2019'),
    ('2020', '2020'),
    ('2021', '2021'),
)


levelOfeducation = (
    ('P3', 'P3'),
    ('P4', 'P4'),
    ('P5', 'P5'),
    ('P6', 'P6'),
    ('S1', 'S1'),
    ('S2', 'S2'),
    ('S3', 'S3'),
    ('S4', 'S4'),
    ('S5', 'S5'),
    ('S6', 'S6'),
)

reason=(
    ('Academic Failure', 'Academic Failure'),
    ('Pregnancy', 'Pregnancy'),
    ('Financial Difficulties', 'Financial Difficulties'),
    ('Mental Illness', 'Mental Illness'),
    ('Drug Use/Addiction', 'Drug Use/Addiction'),
    ('Disabilities', 'Disabilities'),
    ('Retention', 'Retention'),
    ('Disengagement', 'Disengagement'),
    ('Transition', 'Transition'),

)


class Student(models.Model):
    Full_name = models.CharField(max_length=80)
    gender = models.CharField(
        max_length=6, choices=Gender, default='Male', null=False)
    DoB = models.DateField()
    phone_number = models.CharField(max_length=15, unique=True)
    levelofEducation = models.CharField(
        max_length=4, choices=levelOfeducation, null=False)
    yearDropped = models.CharField(
        max_length=6, choices=YearDropped, null=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=False)
    sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, null=False)

    reason = models.CharField(max_length=200, choices=reason, null=False)

    def __str__(self):
        return self.Full_name
    class Meta:
        db_table='student'
    
    
class Reasons(models.Model):
    reasonName = models.CharField(max_length=100)

    def __str__(self):
        return self.reasonName
    class Meta:
        db_table='reason'


class Messages(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    messageBody = models.TextField(max_length=300)

    def __str__(self):
        return self.messageBody
    class Meta:
        db_table='message'
