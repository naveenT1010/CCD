# TODO: Replace forms.Form with ModelForm wherever possible
# TODO: Add CSS classes to form inputs (Naveen)
# (http://stackoverflow.com/questions/401025/define-css-class-in-django-forms)


from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from functools import partial
from django.utils import timezone
# Project imports
from models import Programme, Department, Year
from constants import *
# Crispy Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
# Captcha
from captcha.fields import CaptchaField

# Date Widget
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class StudentLoginForm(forms.Form):
    username = forms.CharField(required=True, label='Webmail', max_length=25)
    password = forms.CharField(required=True, widget=forms.PasswordInput, label="Password")
    # captcha = CaptchaField()


class EditStudProfileForm(forms.Form):
    roll_no = forms.DecimalField(label="Roll No", required=True,
                                 error_messages={'required': 'Please enter your roll number',
                                                 'invalid_choice': 'Please enter a valid roll number'},
                                 widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    iitg_webmail = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    first_name = forms.CharField(max_length=20, label='First Name', required=True,
                                 widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    middle_name = forms.CharField(max_length=20, label='Middle Name', required=False,
                                  widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    last_name = forms.CharField(max_length=20, label='Last Name', required=True,
                                widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    dept = forms.ModelChoiceField(queryset=Department.objects.all(),
                                  widget=forms.Select(attrs={'disabled': 'disabled'}))
    prog = forms.ModelChoiceField(queryset=Programme.objects.all(),
                                  widget=forms.Select(attrs={'disabled': 'disabled'}))
    minor_programme = forms.ModelChoiceField(queryset=Department.objects.all(),
                                             widget=forms.Select(attrs={'disabled': 'disabled'}))
    dob = forms.DateField(required=False)
    sex = forms.ChoiceField(choices=SEX, initial="Male", required=True)
    category = forms.ChoiceField(choices=CATEGORY, initial="Foreign", required=True)
    nationality = forms.CharField(max_length=25, required=False)
    jee_air_rank = forms.DecimalField(max_digits=6, decimal_places=0, initial=5555)
    hostel = forms.ChoiceField(choices=HOSTELS, required=False, initial="Manas")
    room_no = forms.CharField(max_length=6, required=False)
    alternative_email = forms.EmailField(max_length=50, required=False)
    mobile_campus = forms.CharField(label='Mobile(Campus)', required=True, max_length=16)
    mobile_campus_alternative = forms.CharField(label='Mobile Alternative(Campus)', required=False, max_length=16)
    mobile_home = forms.CharField(label='Mobile(Home)', required=True, max_length=16)
    address_line1 = forms.CharField(max_length=50, initial="", label="Permanent Address (Line 1)")
    address_line2 = forms.CharField(max_length=50, initial="", label="Permanent Address (Line 2)")
    address_line3 = forms.CharField(max_length=50, initial="", label="Permanent Address (Line 3)")
    pin_code = forms.DecimalField(max_digits=10, decimal_places=0, initial="781039")
    percentage_x = forms.DecimalField(label='X Percentage', required=True, max_digits=5, decimal_places=2)
    percentage_xii = forms.DecimalField(label='XII Percentage', required=True, max_digits=5, decimal_places=2)
    board_x = forms.CharField(max_length=30, required=False, initial="CBSE")
    board_xii = forms.CharField(max_length=30, required=False, initial="CBSE")
    medium_x = forms.CharField(max_length=30, required=False, initial="English")
    medium_xii = forms.CharField(max_length=30, required=False, initial="English")
    passing_year_x = forms.DecimalField(max_digits=4, decimal_places=0, initial=2001)
    passing_year_xii = forms.DecimalField(max_digits=4, decimal_places=0, initial=2001)
    gap_in_study = forms.BooleanField(label="Gap in study", initial=False)
    gap_reason = forms.CharField(widget=forms.Textarea)
    linkedin_link = forms.EmailField(max_length=254, required=False, label='LinkedIn')
    cpi = forms.DecimalField(max_digits=4, decimal_places=2, initial=6.00)
    spi_1_sem = forms.DecimalField(max_digits=4, decimal_places=2, initial=8.00)
    spi_2_sem = forms.DecimalField(max_digits=4, decimal_places=2, initial=8.00)
    spi_3_sem = forms.DecimalField(max_digits=4, decimal_places=2, initial=8.00)
    spi_4_sem = forms.DecimalField(max_digits=4, decimal_places=2, initial=8.00)
    spi_5_sem = forms.DecimalField(max_digits=4, decimal_places=2, initial=8.00)
    spi_6_sem = forms.DecimalField(max_digits=4, decimal_places=2, initial=8.00)

    def __init__(self, *args, **kwargs):
        super(EditStudProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Personal Information',
                    'roll_no',
                    AppendedText('iitg_webmail', '@iitg.ernet.in'),
                    'first_name',
                    'middle_name',
                    'last_name',
                    'dob',
                    'sex',
                    'category',
                    'nationality',
                    'dept',
                    'prog',
                    'minor_programme',
                    'jee_air_rank',
                    'hostel',
                    'room_no'
                ),
                Tab(
                    'Contact Information',
                    'alternative_email',
                    'mobile_campus',
                    'mobile_campus_alternative',
                    'mobile_home'
                ),
                Tab(
                    'Home Address',
                    'address_line1',
                    'address_line2',
                    'address_line3',
                    'pin_code'
                ),
                Tab(
                    'Board Exams',
                    'percentage_x',
                    'percentage_xii',
                    'board_x',
                    'board_xii',
                    'medium_x',
                    'medium_xii',
                    'passing_year_x',
                    'passing_year_xii',
                    'gap_in_study',
                    'gap_reason',
                ),
                Tab(
                    'CPI',
                    'cpi',
                    'spi_1_sem',
                    'spi_2_sem',
                    'spi_3_sem',
                    'spi_4_sem',
                    'spi_5_sem',
                    'spi_6_sem',
                )
            )
        )


class AlumLoginForm(forms.Form):
    username = forms.CharField(required=True, label='Webmail', max_length=25)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    # captcha = CaptchaField()


class EditAlumProfileForm(forms.Form):
    iitg_webmail = forms.CharField(label="Webmail", max_length=50, required=True)
    alternate_email = forms.EmailField(label="Alternate Email", required=True)
    # programme = forms.ChoiceField(label="Programme", required=True,
    #                               choices=PROGRAMMES,
    #                               error_messages=dict(required='Please choose one programme from list.',
    #                                                   invalied_choice='Please select  a valid choice.'))
    # department = forms.ChoiceField(label="Department",
    #                                required=True, choices=DEPARTMENTS,
    #                                error_messages=dict(required='Please choose one department from list.',
    #                                                    invalied_choice='Please select  a valid choice.'))
    # roll_no = forms.DecimalField(label="Roll No",
    #                              required=True,
    #                              error_messages=dict(required='Please enter your roll number',
    #                                                  invalied_choice='Please enter a valid roll number'))
    # Foreign Keys
    dept = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    prog = forms.ModelChoiceField(queryset=Programme.objects.all(), required=True)

    linkedin_link = forms.EmailField(max_length=254, required=False, label='LinkedIn')


class JobEditForm(forms.Form):
    description = forms.CharField(label="Description", widget=forms.Textarea, required=True)
    designation = forms.CharField(label="Job Designation", max_length=30, required=True)
    # Is Job open for Alum
    open_for_alum = forms.BooleanField(initial=True, required=True, label="Open for Alumni")
    # Are there any CPI requirements
    cpi_shortlist = forms.BooleanField(initial=False, required=False)
    minimum_cpi = forms.DecimalField(decimal_places=2, max_digits=4, initial=06.00, required=True)
    percentage_x = forms.DecimalField(decimal_places=2, max_digits=5, initial=70.00, required=True)
    percentage_xii = forms.DecimalField(decimal_places=2, max_digits=5, initial=70.00, required=True)
    num_openings = forms.DecimalField(label="Openings", required=True)
    other_requirements = forms.CharField(label="Other requirements", widget=forms.Textarea, max_length=140,
                                         required=False)
    # salary information
    currency = forms.CharField(max_length=15, initial="INR")
    ctc_btech = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    ctc_mtech = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    ctc_msc = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    ctc_ma = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    ctc_phd = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    gross_btech = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    gross_mtech = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    gross_msc = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    gross_ma = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    gross_phd = forms.DecimalField(max_digits=12, decimal_places=2, initial=10000)
    take_home_during_training = forms.DecimalField(max_digits=12, decimal_places=2, required=False, initial=10000)
    take_home_after_training = forms.DecimalField(max_digits=12, decimal_places=2, required=False, initial=10000)
    bonus = forms.DecimalField(max_digits=12, decimal_places=2, label="Bonus/Perks/Incentives", required=False)
    bond = forms.BooleanField(required=True, initial=False)
    bond_details = forms.CharField(widget=forms.Textarea, required=False, max_length=200)
    profile_name = forms.CharField(max_length=25, required=True)
    prog = forms.ModelMultipleChoiceField(queryset=Programme.objects.all(), widget=forms.CheckboxSelectMultiple,
                                          required=True, label='Programmes')
    dept = forms.ModelMultipleChoiceField(queryset=Department.objects.all(), widget=forms.CheckboxSelectMultiple,
                                          required=True, label='Departments')

    # current year is not required for Job
    # current_year = forms.ModelMultipleChoiceField(queryset=Year.objects.all(), widget=forms.CheckboxSelectMultiple,
    #                                               required=True, label='Audience')

    def __init__(self, *args, **kwargs):
        """
        Init function.
        Form layout is defined here.
        :param args: args
        :param kwargs:kwargs
        :return:void
        """
        super(JobEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Basic Information',
                    'description',
                    'designation',
                    'profile_name',
                    'open_for_alum',
                    'num_openings'
                ),
                Tab(
                    'Requirements',
                    'cpi_shortlist',
                    'minimum_cpi',
                    'percentage_x',
                    'percentage_xii',
                    'other_requirements'
                ),
                Tab(
                    'Salary/Incentives',
                    'currency',
                    'ctc_btech',
                    'ctc_mtech',
                    'ctc_phd',
                    'ctc_msc',
                    'ctc_ma',
                    'gross_btech',
                    'gross_mtech',
                    'gross_phd',
                    'gross_msc',
                    'gross_ma',
                    'take_home_during_training',
                    'take_home_after_training',
                    'bonus'
                ),
                Tab(
                    'Bond',
                    'bond',
                    'bond_details'
                ),
                Tab(
                    'Open For',
                    'prog',
                    'dept',
                    'current_year'
                )
            )
        )


class AdminJobEditForm(JobEditForm):
    opening_date = forms.DateField(label="Opening Date", required=True, widget=DateInput())
    application_deadline = forms.DateField(label="Application Deadline", required=True, widget=DateInput())

    def __init__(self, *args, **kwargs):
        super(AdminJobEditForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Basic Information',
                    'description',
                    'designation',
                    'profile_name',
                    'open_for_alum',
                    'num_openings'
                ),
                Tab(
                    'Requirements',
                    'cpi_shortlist',
                    'minimum_cpi',
                    'percentage_x',
                    'percentage_xii',
                    'other_requirements'
                ),
                Tab(
                    'Salary/Incentives',
                    'currency',
                    'ctc_btech',
                    'ctc_mtech',
                    'ctc_phd',
                    'ctc_msc',
                    'ctc_ma',
                    'gross_btech',
                    'gross_mtech',
                    'gross_phd',
                    'gross_msc',
                    'gross_ma',
                    'take_home_during_training',
                    'take_home_after_training',
                    'bonus'
                ),
                Tab(
                    'Bond',
                    'bond',
                    'bond_details'
                ),
                Tab(
                    'Open For',
                    'prog',
                    'dept',
                    'current_year'
                ),
                Tab(
                    'Date Settings',
                    'opening_date',
                    'application_deadline'
                )
            )
        )


class RequestEventForm(forms.Form):
    title = forms.CharField(max_length=30, required=True, label='Event Title')
    date1 = forms.DateField(label='Date priority 1', required=True, widget=DateInput())
    date2 = forms.DateField(label='Date priority 2', required=True, widget=DateInput())
    date3 = forms.DateField(label='Date priority 3', required=True, widget=DateInput())


class CompanySignupForm(forms.Form):
    company_name = forms.CharField(max_length=30, label="Company Name")
    description = forms.CharField(label="Brief Writeup on organization", widget=forms.Textarea)
    postal_address = forms.CharField(label="Postal Address", widget=forms.Textarea)
    website = forms.CharField(initial="www.example.com", max_length=100)
    organization_type = forms.ChoiceField(choices=ORGANIZATION_TYPE, initial='PSU')
    industry_sector = forms.ChoiceField(choices=INDUSTRY_SECTOR, initial='IT')
    # HR Contact
    head_hr_name = forms.CharField(max_length=20, required=False)
    head_hr_email = forms.CharField(max_length=60, required=False)
    head_hr_designation = forms.CharField(max_length=30, required=False)
    head_hr_mobile = forms.CharField(max_length=12, required=False)
    head_hr_fax = forms.CharField(max_length=15, required=False)

    first_hr_name = forms.CharField(max_length=20, required=True)
    first_hr_email = forms.CharField(max_length=60, required=True)
    first_hr_designation = forms.CharField(max_length=30, required=True)
    first_hr_mobile = forms.CharField(max_length=12, required=True)
    first_hr_fax = forms.CharField(max_length=15, required=True)

    second_hr_name = forms.CharField(max_length=20, required=False)
    second_hr_email = forms.CharField(max_length=60, required=False)
    second_hr_designation = forms.CharField(max_length=30, required=False)
    second_hr_mobile = forms.CharField(max_length=12, required=False)
    second_hr_fax = forms.CharField(max_length=15, required=False)

    # Captcha Field
    # captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CompanySignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'General Details',
                    'company_name',
                    'description',
                    'postal_address',
                    'website',
                    'organization_type',
                    'industry_sector',
                    'captcha'
                ),
                Tab(
                    'HR Details',
                    'head_hr_name',
                    'head_hr_email',
                    'head_hr_designation',
                    'head_hr_mobile',
                    'head_hr_fax',
                    'first_hr_name',
                    'first_hr_email',
                    'first_hr_designation',
                    'first_hr_mobile',
                    'first_hr_fax',
                    'second_hr_name',
                    'second_hr_email',
                    'second_hr_designation',
                    'second_hr_mobile',
                    'second_hr_fax'
                )
            )
        )


class CompanyLoginForm(forms.Form):
    username = forms.CharField(required=True, label='Webmail', max_length=25)
    password = forms.CharField(required=True, widget=forms.PasswordInput, label="Password")
    # captcha = CaptchaField()


class AdminLoginForm(forms.Form):
    username = forms.CharField(required=True, label="Username", max_length=25)
    password = forms.CharField(required=True, widget=forms.PasswordInput, label="Password")
    # captcha = CaptchaField()


class CompanyProfileEdit(CompanySignupForm):
    company_name = forms.CharField(max_length=30,
                                   label="Company Name",
                                   widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super(CompanyProfileEdit, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'General Details',
                    'company_name',
                    'description',
                    'postal_address',
                    'website',
                    'organization_type',
                    'industry_sector'
                ),
                Tab(
                    'HR Details',
                    'head_hr_name',
                    'head_hr_email',
                    'head_hr_designation',
                    'head_hr_mobile',
                    'head_hr_fax',
                    'first_hr_name',
                    'first_hr_email',
                    'first_hr_designation',
                    'first_hr_mobile',
                    'first_hr_fax',
                    'second_hr_name',
                    'second_hr_email',
                    'second_hr_designation',
                    'second_hr_mobile',
                    'second_hr_fax',
                )
            )
        )


# Search forms
class StudentSearchForm(forms.Form):
    programme = forms.ChoiceField(label="Programme", required=True, choices=PROGRAMMES)
    year = forms.DecimalField(required=True)
    department = forms.ChoiceField(label="Department", required=True, choices=DEPARTMENTS)


# Admin User Management forms
class AddStudent(forms.Form):
    # Login Credentials
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    roll_no = forms.DecimalField(label="Roll No", required=True,
                                 error_messages={'required': 'Please enter your roll number',
                                                 'invalied_choice': 'Please enter a valid roll number'})
    first_name = forms.CharField(required=True, max_length=20, label="First Name")
    middle_name = forms.CharField(required=True, max_length=20, label="Middle Name")
    last_name = forms.CharField(max_length=20, label='Last Name', required=True)
    dob = forms.DateField(initial=timezone.now())
    sex = forms.ChoiceField(choices=SEX)
    category = forms.ChoiceField(choices=CATEGORY)
    nationality = forms.CharField(max_length=20, initial="INDIAN")
    jee_air_rank = forms.DecimalField(max_digits=6, decimal_places=0)
    dept = forms.ModelChoiceField(queryset=Department.objects.all())
    year = forms.ModelChoiceField(queryset=Year.objects.all())
    prog = forms.ModelChoiceField(queryset=Programme.objects.all())
    minor_programme = forms.ModelChoiceField(queryset=Department.objects.all())
    hostel = forms.ChoiceField(choices=HOSTELS)
    room_no = forms.CharField(max_length=6, required=True, label="Room No")
    iitg_webmail = forms.CharField(max_length=20, label = "IITG_webmail")
    alternative_email = forms.CharField(max_length=50)
    mobile_campus = forms.CharField(label='Mobile Number(IITG)', max_length=16)
    mobile_campus_alternative = forms.CharField(label='Alternative Mobile Number(IITG)')
    mobile_home = forms.CharField(label='Mobile Number(Home)', max_length=16)
    address_line1 = forms.CharField(max_length=50, initial="", label="Permanent Address (Line 1)")
    address_line2 = forms.CharField(max_length=50, initial="", label="Permanent Address (Line 2)")
    address_line3 = forms.CharField(max_length=50, initial="", label="Permanent Address (Line 3)")
    pin_code = forms.DecimalField(max_digits=10, decimal_places=0, initial="781039")
    percentage_x = forms.DecimalField(label='X Percentage', required=True, max_digits=5, decimal_places=2)
    percentage_xii = forms.DecimalField(label='XII Percentage', required=True, max_digits=5, decimal_places=2)
    gap_in_study = forms.BooleanField(label="Gap in study", initial=False)
    gap_reason = forms.CharField(widget=forms.Textarea)
    linkedin_link = forms.EmailField(max_length=254, required=False, label='LinkedIn')
    placed = forms.BooleanField(initial=False)
    intern2 = forms.BooleanField(initial=False)
    intern3 = forms.BooleanField(initial=False)
    ppo = forms.BooleanField(initial=False)
    cpi = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_1_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_2_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_3_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_4_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_5_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_6_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)


class AddCompany(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=30)
    company_name = forms.CharField(max_length=30, label="Company Name")
    description = forms.CharField(label="Brief Writeup on organization", widget=forms.Textarea)
    website = forms.CharField(initial="www.example.com", max_length=100)
    organization_type = forms.ChoiceField(choices=ORGANIZATION_TYPE, initial='PSU')
    industry_sector = forms.ChoiceField(choices=INDUSTRY_SECTOR, initial='IT')
    # HR Contact
    head_hr_name = forms.CharField(max_length=20, required=False)
    head_hr_email = forms.CharField(max_length=60, required=False)
    head_hr_designation = forms.CharField(max_length=30, required=False)
    head_hr_mobile = forms.CharField(max_length=12, required=False)
    head_hr_fax = forms.CharField(max_length=15, required=False)
    first_hr_name = forms.CharField(max_length=20, required=True, initial="First Hr name")
    first_hr_email = forms.CharField(max_length=60, required=True, initial="FHR email")
    first_hr_designation = forms.CharField(max_length=30, required=True, initial="desg")
    first_hr_mobile = forms.CharField(max_length=12, required=True, initial="781039")
    first_hr_fax = forms.CharField(max_length=15, required=True, initial="781039")
    second_hr_name = forms.CharField(max_length=20, required=False)
    second_hr_email = forms.CharField(max_length=60, required=False)
    second_hr_designation = forms.CharField(max_length=30, required=False)
    second_hr_mobile = forms.CharField(max_length=12, required=False)
    second_hr_fax = forms.CharField(max_length=15, required=False)
    approved = forms.BooleanField(initial=False, required=False)
    sent_back = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(AddCompany, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Login Credentials',
                    'username',
                    'password'
                ),
                Tab(
                    'General Details',
                    'company_name',
                    'description',
                    'postal_address',
                    'website',
                    'organization_type',
                    'industry_sector'
                ),
                Tab(
                    'HR Details',
                    'head_hr_name',
                    'head_hr_email',
                    'head_hr_designation',
                    'head_hr_mobile',
                    'head_hr_fax',
                    'first_hr_name',
                    'first_hr_email',
                    'first_hr_designation',
                    'first_hr_mobile',
                    'first_hr_fax',
                    'second_hr_name',
                    'second_hr_email',
                    'second_hr_designation',
                    'second_hr_mobile',
                    'second_hr_fax',
                )
            )
        )


class EditCompany(forms.Form):
    # username = forms.CharField(max_length=20, required=True,
    #                            help_text="Username cannot be changed")
    # password = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'readonly' : 'readonly'}))
    company_name = forms.CharField(max_length=30, label="Company Name")
    description = forms.CharField(label="Brief Writeup on organization", widget=forms.Textarea)
    website = forms.CharField(initial="www.example.com", max_length=100)
    organization_type = forms.ChoiceField(choices=ORGANIZATION_TYPE, initial='PSU')
    industry_sector = forms.ChoiceField(choices=INDUSTRY_SECTOR, initial='IT')
    # HR Contact
    head_hr_name = forms.CharField(max_length=20, required=False)
    head_hr_email = forms.CharField(max_length=60, required=False)
    head_hr_designation = forms.CharField(max_length=30, required=False)
    head_hr_mobile = forms.CharField(max_length=12, required=False)
    head_hr_fax = forms.CharField(max_length=15, required=False)
    first_hr_name = forms.CharField(max_length=20, required=True)
    first_hr_email = forms.CharField(max_length=60, required=True)
    first_hr_designation = forms.CharField(max_length=30, required=True)
    first_hr_mobile = forms.CharField(max_length=12, required=True)
    first_hr_fax = forms.CharField(max_length=15, required=True)
    second_hr_name = forms.CharField(max_length=20, required=False)
    second_hr_email = forms.CharField(max_length=60, required=False)
    second_hr_designation = forms.CharField(max_length=30, required=False)
    second_hr_mobile = forms.CharField(max_length=12, required=False)
    second_hr_fax = forms.CharField(max_length=15, required=False)
    approved = forms.BooleanField(initial=False, required=False)
    sent_back = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(EditCompany, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'General Details',
                    'company_name',
                    'description',
                    'postal_address',
                    'website',
                    'organization_type',
                    'industry_sector'
                ),
                Tab(
                    'HR Details',
                    'head_hr_name',
                    'head_hr_email',
                    'head_hr_designation',
                    'head_hr_mobile',
                    'head_hr_fax',
                    'first_hr_name',
                    'first_hr_email',
                    'first_hr_designation',
                    'first_hr_mobile',
                    'first_hr_fax',
                    'second_hr_name',
                    'second_hr_email',
                    'second_hr_designation',
                    'second_hr_mobile',
                    'second_hr_fax',
                ),
                Tab(
                    'Settings',
                    'username',
                    'approved',
                    'sent_back'
                )
            )
        )


class EditStudentAdmin(forms.Form):
    roll_no = forms.DecimalField(label="Roll No", required=True,
                                 error_messages={'required': 'Please enter your roll number',
                                                 'invalied_choice': 'Please enter a valid roll number'})
    first_name = forms.CharField(required=True, max_length=20, label="First Name")
    middle_name = forms.CharField(required=True, max_length=20, label="Middle Name")
    last_name = forms.CharField(max_length=20, label='Last Name', required=True)
    dob = forms.DateField(initial=timezone.now)
    sex = forms.ChoiceField(choices=SEX)
    category = forms.ChoiceField(choices=CATEGORY)
    nationality = forms.CharField(max_length=20, initial="INDIAN")
    minor_programme = forms.ModelChoiceField(queryset=Department.objects.all())
    jee_air_rank = forms.DecimalField(max_digits=6, decimal_places=0)
    dept = forms.ModelChoiceField(queryset=Department.objects.all())
    year = forms.ModelChoiceField(queryset=Year.objects.all())
    prog = forms.ModelChoiceField(queryset=Programme.objects.all())
    hostel = forms.ChoiceField(choices=HOSTELS)
    room_no = forms.CharField(max_length=6, required=True, label="Room No")
    alternative_email = forms.CharField(max_length=50)
    mobile_campus = forms.CharField(label='Mobile Number(IITG)', max_length=16)
    mobile_campus_alternative = forms.CharField(label='Alternative Mobile Number(IITG)', initial="781039")
    mobile_home = forms.CharField(label='Mobile Number(Home)', max_length=16, initial="781039")
    address_line1 = forms.CharField(max_length=50, label="Permanent Address (Line 1)", initial="line1")
    address_line2 = forms.CharField(max_length=50, label="Permanent Address (Line 2)", initial="line2")
    address_line3 = forms.CharField(max_length=50, label="Permanent Address (Line 3)", initial="line3")
    pin_code = forms.DecimalField(max_digits=10, decimal_places=0, initial="781039")
    percentage_x = forms.DecimalField(label='X Percentage', required=True, max_digits=5, decimal_places=2, initial=100)
    percentage_xii = forms.DecimalField(label='XII Percentage', required=True, max_digits=5, decimal_places=2,
                                        initial=100)
    gap_in_study = forms.BooleanField(label="Gap in study", initial=False)
    gap_reason = forms.CharField(widget=forms.Textarea)
    linkedin_link = forms.EmailField(max_length=254, required=False, label='LinkedIn')
    intern2 = forms.BooleanField(initial=False, required=False)
    intern3 = forms.BooleanField(initial=False, required=False)
    ppo = forms.BooleanField(initial=False, required=False)
    cpi = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_1_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_2_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_3_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_4_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_5_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)
    spi_6_sem = forms.DecimalField(initial=0.00, decimal_places=2, max_digits=4, required=True)


class AddEditDeartment(ModelForm):
    class Meta:
        model = Department
        fields = "__all__"


class AddEditProgramme(ModelForm):
    class Meta:
        model = Programme
        fields = "__all__"


class AddEditYear(ModelForm):
    class Meta:
        model = Year
        fields = "__all__"


class SelectCVForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop("extra")
        super(SelectCVForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            self.fields['custom_%s' % i] = forms.BooleanField(label=question, initial=True, required=False)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)

    def clean(self):
        all_false = True
        for (question, answer) in self.extra_answers():
            if answer is True:
                all_false = False
        if all_false:
            raise ValidationError("At least one CV must be selected.")


class StudCVForm(forms.Form):
    cv1 = forms.FileField(label='CV1', required=False, max_length=100)
    cv2 = forms.FileField(label='CV2', required=False, max_length=100)

    def __init__(self, *args, **kwargs):
        super(StudCVForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout()

    def clean(self):
        form_data = self.cleaned_data
        if not bool(form_data['cv1']) and not bool(form_data['cv2']):
            raise ValidationError("Provide at least one file.")
