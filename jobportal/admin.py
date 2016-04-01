from django.contrib import admin
# Register your models here.
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'login_type']
    list_display = ['user', 'login_type']
    list_filter = ['login_type']


admin.site.register(UserProfile, UserProfileAdmin)


class StudentAdmin(admin.ModelAdmin):
    fields = ['user', 'iitg_webmail', 'roll_no', 'dept', 'year', 'cv1', 'cv2']
    list_display = ['user', 'iitg_webmail', 'first_name', 'middle_name', 'last_name', 'roll_no', 'dept', 'year', 'cpi',
                    'placed']
    list_filter = ['dept', 'prog']


admin.site.register(Student, StudentAdmin)


class AlumniAdmin(admin.ModelAdmin):
    fields = ['user', 'iitg_webmail', 'alternate_email', 'dept', 'prog', ]
    list_display = ['user', 'iitg_webmail', 'alternate_email', 'dept', 'prog']
    list_filter = ['dept', 'prog']


admin.site.register(Alumni, AlumniAdmin)


class JobAdmin(admin.ModelAdmin):
    fields = ['alum_owner', 'company_owner', 'posted_by_alumnus', 'posted_by_company', 'description', 'designation',
              'num_openings', 'profile_name', 'dept', 'current_year', 'posted_on', 'last_updated',
              'application_deadline', 'approved']
    list_display = ['alum_owner', 'company_owner', 'num_openings', 'posted_on', 'last_updated', 'opening_date',
                    'application_deadline', 'approved']
    list_filter = ['posted_by_alumnus', 'posted_by_company', 'posted_on', 'last_updated']


admin.site.register(Job, JobAdmin)





admin.site.register(Year)

admin.site.register(Department)

admin.site.register(Programme)

class EventAdmin(admin.ModelAdmin):
    fields = ['alum_owner', 'company_owner', 'title', 'date1', 'date2', 'date3', 'final_date', 'finalised']
    list_display = ['alum_owner', 'company_owner', 'title', 'date1', 'date2', 'date3', 'final_date', 'finalised']


admin.site.register(Event, EventAdmin)

admin.site.register(Company)

admin.site.register(StudentJobRelation)


class AdminAdmin(admin.ModelAdmin):
    fields = ['user', 'admin_username', 'position']
    list_display = ['user', 'admin_username', 'position']


admin.site.register(Admin, AdminAdmin)


class CompanyRegAdmin(admin.ModelAdmin):
    fields = ['company_name_reg', 'first_hr_email_reg']
    list_display = ['company_name_reg', 'first_hr_email_reg']

admin.site.register(CompanyReg, CompanyRegAdmin)