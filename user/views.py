from datetime import datetime, timedelta
import imp
from itertools import count
from multiprocessing import context
import pstats
import datetime
from django.db.models import Sum
import re
from urllib import response
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa
from os import name
from base.decorators import admin_only, allowed_users, unauthenticated_user
from pydoc import render_doc
from django.shortcuts import redirect, render
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from base.forms import studentForm
from .forms import *
from base .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.db import connection

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.contrib import messages


# Create your views here.

#  home page view

@login_required(login_url='login-user')
def index(request):
    std = Student()
    # reasons=Reasons.objects.all()
    student = Student.objects.all()
    sectors = Sector.objects.all()
    s_count = student.count()
    mess = Messages.objects.all()
    c_message= mess.count()
    stude = Student.objects.raw(
        'SELECT 1 id, count(id) as total_reason, reason FROM student GROUP BY reason')
    student = Student.objects.raw(
        'SELECT 1 id, count(id) as total, gender FROM student GROUP BY gender')
    stud = Student.objects.raw(
        'SELECT 1 id, count(id) as total_dropout, sector_id FROM student GROUP BY sector_id')
   # duplicateReason=Student.objects.values('reason').annotate(std_count= count('reason'))

    context = {'student': student, 's_count': s_count,
               'sectors': sectors, 'student': student, 'stud': stud, 'stude': stude, 'c_message': c_message}
    return render(request, 'dashboard/maindashboard.html', context)

#  function to register new users in the system


@allowed_users(allowed_roles=['admin'])
def register(request):
    if request.method == 'POST':
        form = createrUser(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login-user')
    else:
        form = createrUser()
    context = {'form': form}

    return render(request, 'user/register.html', context)

#function to search in table

def search(request):
    if 'q' in request.GET:
        q=request.GET['q']
        q= Student.objects.filter(Full_name__icontains=q)
    else:
        student= Student.objects.all()
    return render(request, 'dashboard/maindashboard.html', {'student': student})

# funtion to record new student dropped out
@login_required
def registerStudent(request):
    studentform = registerStudentForm()
    districts = District.objects.all()
    sec = Sector.objects.all()
    if request.method == 'POST':
        studentform = registerStudentForm(request.POST)
        if studentform.is_valid():
            studentform.save()
            return redirect('student-list')
    else:
        studentform = registerStudentForm()

    context = {'studentform': studentform, 'districts': districts, 'sec': sec}
    return render(request, 'user/student_form.html', context)

# function to record a sectors


@allowed_users(allowed_roles=['admin'])
def record_sectors(request):
    sectorform = sectorForm()
    if request.method == 'POST':
        sectorform = sectorForm(request.POST)
        if sectorform.is_valid():
            sectorform.save()
            return redirect('sector-list')
    else:
        sectorform = sectorForm()
    context = {'sectorform': sectorform}

    return render(request, 'dashboard/record-sectors.html', context)


#  function to count student in a given sector

def countStudentInsector(request):
    student = Student.objects.annotate(
        studentcount=Count('sector'))
    context = {'student': student}
    return render(request, 'dashboard/female.html', context)


# dashboard new

def maindashboard(request):
    return render(request, 'dashboard/maindashboard.html')


# function to display all recorded sector

def displaySectors(request):
    sectors = Sector.objects.all()
    context = {'sectors': sectors}
    return render(request, 'dashboard/sector.html', context)

# function to display all student student dropped out


def studentList(request):
    students = Student.objects.all()
    student_count = students.count()
    context = {'students': students, 'student_count': student_count}
    return render(request, 'dashboard/student.html', context)


def displayReason(request):
    reasons = Reasons.objects.all()
    context = {'reasons': reasons}
    return render(request, 'dashboard/reason-list.html', context)

#  function to send a notification


@allowed_users(allowed_roles=['admin'])
def sendmessage(request):
    messageform = messageForm()
    if request.method == 'POST':
        messageform = messageForm(request.POST)
        if messageform.is_valid():
            messageform.save()
            return redirect('sendmessage')
    else:
        messageform = messageForm()
        context = {'messageform': messageform}
    return render(request, 'dashboard/direct-message.html', context)


#  function to display a message
@allowed_users(allowed_roles=['user'])
def notifications(request):
    notification = Messages.objects.all()
    sector= Sector.objects.all()
    context = {'notification': notification, 'sector': sector}
    return render(request, 'dashboard/messageboard.html', context)



def sectors(request):
    result = request.GET['sectors']
    student = Student()
    if result:
        student = Student.objects.all()
    context = {'result': result, 'student': student}
    return render(request, 'dashboard/sectors.html', context)

#  function to delete a student


@login_required
def deleteStudent(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student-list')
    return render(request, 'dashboard/delete_student.html')

# user profile function


@login_required
def userProfile(request):
    return render(request, 'user/profile.html')

#  function to update student


@login_required
def editStudent(request, pk):
    stud = Student.objects.get(id=pk)
    if request.method == 'POST':
        studentform = registerStudentForm(request.POST, instance=stud)
        if studentform.is_valid():
            studentform.save()
            return redirect('student-list')
    else:
        studentform = registerStudentForm(instance=stud)

    context = {
        'studentform': studentform

    }
    return render(request, 'dashboard/edit-sudent.html', context)


def countBygender(request):
    student = Student.objects.raw(
        'SELECT 1 id, count(id) as total, gender FROM student GROUP BY gender')
    context = {'student': student}
    return render(request, 'dashboard/gender.html', context)


def countBysector(request):
    stud = Student.objects.raw(
        'SELECT 1 id, count(id) as total_reason, reason FROM student GROUP BY reason')
    context = {'stud': stud}
    return render(request, 'dashboard/sector.html', context)


# report generated
@login_required
def createReport(request):
    student = Student.objects.all()
    user= User.objects.all()
    template_path = 'dashboard/generate-report.html'
    context = {'student': student, 'user': user}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dropout-report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    # pisa_status = pisa.CreatePDF(
    #     html, dest=response)
    # if error then show some funy view
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

def generatereport2(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment'; 'filename= dropout' + \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding']= 'binary'

    totalstudent= Student.objects.all()

    # all= Student.objects.aggregate(Sum('gender'))
    html_string= render_to_string('dashboard/report2.html',{'totalstudent': totalstudent, 'name': None})
    html=HTML(string= html_string)
    result= html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response