import email
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from base.models import District, Reasons, Sector, Student
from .forms import studentForm, userForm
from django.contrib import messages
from .decorators import admin_only, allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required


# Create your views here.


def displayDistrict(request):
    return render(request, 'dashboard/district.html')

def displaySectors(request):
    return render(request, 'dashboard/sector.html')

def displayStudent(request):
    return render(request, 'dashboard/student.html')

def profilePage(request):
    return render(request, 'dashboard/profile.html')


def registerpage(request):
    form = userForm()
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid:
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'account created for the user: ' + user)
            return redirect('login')
    context = {'form': form}
    return render(request, 'base/register.html', context)


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'user or passowrd are incorect! ')

    context = {}
    return render(request, 'user/login.html', context)


def logoutpage(request):
    logout(request)
    return redirect('login')


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['user'])
def home(request):
    districts = District.objects.all()
    reasons =Reasons.objects.all()
    
    context={'districts': districts, 'reasons': reasons}
    return render(request, 'base/index.html', context)


@admin_only
def homepage(request):

    return render(request, 'base/index.html')

def registerstudent(request):
    form = studentForm()
    if request.method == 'POST':
        form = studentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_student')
    return render(request, 'base/index.html', {'form': form})

def indexpage(request):
    districts = District.objects.all()
    context = {'districts': districts}
    return render(request, 'base/home.html', context)


def load_sectors(request):
    district_id = request.GET.get('district')
    sectors = Sector.objects.filter(district_id=district_id).order_by('s_name')
    return render(request, 'base/sectors_list.html', {'sectors': sectors})

def reasons(request):
   reasons =Reasons.objects.all()
   dictionary= {'reasons': reasons}
   return render(request, 'base/index.html', dictionary)



