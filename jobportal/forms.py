# TODO: Replace forms.Form with ModelForm wherever possible
# TODO: Add CSS classes to form inputs (Naveen)
# (http://stackoverflow.com/questions/401025/define-css-class-in-django-forms)

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory
from functools import partial
# Project imports
from models import *
from constants import *
# Crispy Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
# Captcha
from captcha.fields import CaptchaField

# Date Widget
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

JobProgFormSet = inlineformset_factory(Job, ProgrammeJobRelation, fields=('year', 'dept', 'prog'), extra=2)


class StudentLoginForm(forms.Form):
    username = forms.CharField(required=True, label='Webmail', max_length=25)
    password = forms.CharField(required=True, widget=forms.PasswordInput, label="Password")
    # captcha = CaptchaField()


class EditStudProfileForm(ModelForm):

    class Meta:
        model = Student
        exclude = ['user', 'avatar', 'signature', 'cv1', 'cv2', 'placed', 'inter2', 'intern3', 'ppo']

    def __init__(self, *args, **kwargs):
        super(EditStudProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Student Information',
                    'roll_no',
                    AppendedText('iitg_webmail', '@iitg.ernet.in'),
                    'first_name',
                    'middle_name',
                    'last_name',
                    'dob',
                    'sex',
                    'category',
                    'nationality',
                    'year',
                    'dept',
                    'prog',
                    'minor_programme',
                    'hostel',
                    'room_no'
                ),
                Tab(
                    'Contact Information',
                    'linkedin_link',
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
                    'Academic',
                    'jee_air_rank',
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
    dept = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    prog = forms.ModelChoiceField(queryset=Programme.objects.all(), required=True)

    linkedin_link = forms.EmailField(max_length=254, required=False, label='LinkedIn')


class JobEditForm(ModelForm):
    class Meta:
        model = Job
        exclude = ['alum_owner', 'company_owner', 'posted_by_alumnus', 'posted_by_company',
                   'posted_on', 'approved', 'approved_on', 'sent_back', 'last_updated', 'opening_date',
                   'application_deadline']

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
                )
            )
        )


class AdminJobEditForm(ModelForm):
    class Meta:
        model = Job
        exclude = ['alum_owner', 'company_owner', 'posted_by_alumnus', 'posted_by_company',
                   'posted_on', 'approved_on', 'last_updated']

    def __init__(self, *args, **kwargs):
        super(AdminJobEditForm, self).__init__(*args, **kwargs)
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


class CompanySignupForm(ModelForm):

    # Captcha Field
    # captcha = CaptchaField()

    class Meta:
        model = CompanyReg
        exclude = []

    def __init__(self, *args, **kwargs):
        super(CompanySignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'General Details',
                    'company_name_reg',
                    'description_reg',
                    'postal_address_reg',
                    'website_reg',
                    'organization_type_reg',
                    'industry_sector_reg',
                    'captcha'
                ),
                Tab(
                    'HR Details',
                    'head_hr_name_reg',
                    'head_hr_email_reg',
                    'head_hr_designation_reg',
                    'head_hr_mobile_reg',
                    'head_hr_fax_reg',
                    'first_hr_name_reg',
                    'first_hr_email_reg',
                    'first_hr_designation_reg',
                    'first_hr_mobile_reg',
                    'first_hr_fax_reg'
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


class CompanyProfileEdit(ModelForm):
    company_name = forms.CharField(max_length=30,
                                   label="Company Name",
                                   widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Company
        exclude = ['user', 'password_copy', 'approved', 'sent_back']

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
                    'first_hr_fax'
                )
            )
        )


# Search forms
class StudentSearchForm(forms.Form):
    programme = forms.ChoiceField(label="Programme", required=True, choices=PROGRAMMES)
    year = forms.DecimalField(required=True)
    department = forms.ChoiceField(label="Department", required=True, choices=DEPARTMENTS)


# Admin User Management forms
class AddStudent(ModelForm):
    # Login Credentials
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = Student
        exclude = ['user', 'avatar', 'signature', 'placed', 'cv1', 'cv2', 'intern2', 'intern3', 'ppo']


class AddCompany(ModelForm):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=30)

    class Meta:
        model = Company
        fields = '__all__'

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
                    'first_hr_fax'
                )
            )
        )


class EditCompany(ModelForm):

    class Meta:
        model = Company
        exclude = ['username', 'password']

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
                    'first_hr_fax'
                ),
                Tab(
                    'Settings',
                    'approved',
                    'sent_back'
                )
            )
        )


class EditStudentAdmin(ModelForm):

    class Meta:
        model = Student
        exclude = ['username', 'password', 'avatar', 'signature']


class AddEditDepartment(ModelForm):
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


class AvatarSignForm(ModelForm):
    class Meta:
        model = Student
        fields = ['avatar', 'signature']


