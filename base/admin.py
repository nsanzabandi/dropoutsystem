from django.contrib import admin
from .models import Student, District, Sector, Reasons

# Register your models here.
admin.site.site_header ='Dropout'

admin.site.register(Student)
admin.site.register(District)
# admin.site.register(Messages)
admin.site.register(Sector)
admin.site.register(Reasons)

