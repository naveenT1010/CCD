from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from datetime import datetime
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from .models import UserProfile, Student, Company, Job, Year, Programme, \
    Department, Admin, CompanyReg, StudentJobRelation, AlumJobRelation, Alumni
from .forms import AdminLoginForm, StudentSearchForm, AddStudent, \
    AddCompany, EditCompany, EditStudentAdmin
from .forms import AddEditDeartment, AddEditProgramme, AddEditYear, AdminJobEditForm

ADMIN_LOGIN_URL = reverse_lazy('jobportal/admin_login')


def admin_login(request):
    """
    Admin login.
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    if request.method == "POST":
        admin_login_form_data = AdminLoginForm(request.POST)
        if admin_login_form_data.is_valid():
            username = admin_login_form_data.cleaned_data['username']
            password = admin_login_form_data.cleaned_data['password']
            # check authentication
            user = auth.authenticate(username=username, password=password)
            # if User exists
            if user is not None:
                # get User instance
                current_user = User.objects.get(username=username)
                # get UserProfile instance
                user_profile = UserProfile.objects.get(user=current_user)
                # if UserProfile instance is Admin
                if user_profile.login_type == 'Admin':
                    # login User
                    auth.login(request, user)
                    # get Admin instance
                    admin_instance = Admin.objects.get(user=user_profile)
                    # set session variables
                    request.session['admin_instance_id'] = admin_instance.id
                    request.session['user_type'] = 'Admin'
                    return redirect('admin_home')
                # User exists but is not Admin
                # TODO : Add redirect to correct login page
                else:
                    args = dict(login_form=admin_login_form_data)
                    return render(request, 'jobportal/Admin/admin_login.html', args)
            # either username-password mismatch or User doesn't exist
            else:
                args = dict(login_form=admin_login_form_data)
                return render(request, 'jobportal/Admin/admin_login.html', args)
        # invalid form submission
        else:
            args = dict(login_form=admin_login_form_data)
            return render(request, 'jobportal/Admin/admin_login.html', args)
    else:
        args = dict(login_form=AdminLoginForm())
        return render(request, 'jobportal/Admin/admin_login.html', args)


# Admin home
@login_required(login_url=ADMIN_LOGIN_URL)
def admin_home(request):
    admin_instance = get_object_or_404(Admin, id=request.session['admin_instance_id'])
    requestscount = CompanyReg.objects.all().count()
    companiescount = Company.objects.all().count()
    jobscount = Job.objects.all().count()
    args = {'admin': admin_instance,
            'requestscount': requestscount,
            'companiescount': companiescount,
            'jobscount': jobscount
            }

    return render(request, 'jobportal/Admin/admin_home.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def admin_logout(request):
    """
    Logout Admin.
    :param request: HttpResquest object
    :return: HttpResponse object
    """
    auth.logout(request)
    return render(request, "jobportal/logout.html")


@login_required(login_url=ADMIN_LOGIN_URL)
def departments(request):
    """
    Fetch all Department instances
    :param request: HttpRequest instance
    :return: HttpResponse instance
    """
    args = dict(departments=Department.objects.all())
    return render(request, 'jobportal/Admin/departments.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def add_department(request):
    """
    Add new Department instance.
    :param request: HttpRequest instance
    :return: HttpResponse instance
    """
    if request.method == 'POST':
        # parse form data
        department_form = AddEditDeartment(request.POST)
        # if form is valid
        if department_form.is_valid():
            # save instance
            department_form.save()
            # redirect to jobportal/departments
            return redirect("departments")
        else:
            args = dict(department_add_form=department_form, add=True)
            return render(request, 'jobportal/Admin/add_edit_department.html', args)
    else:
        args = dict(department_add_form=AddEditDeartment(), add=True)
        return render(request, 'jobportal/Admin/add_edit_department.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def edit_department(request, deptid):
    """
    Edit existing Department instance
    :param request: HttpRequest instance
    :param deptid: id of Department instance
    :return: HttpResponse instance
    """
    if request.method == "POST":
        department_instance = Department.objects.get(id=deptid)
        department_form = AddEditDeartment(request.POST, instance=department_instance)
        if department_form.is_valid():
            department_form.save()
            # redirect to jobportal/departments
            return redirect('departments')
        else:
            args = dict(department_edit_form=department_form, edit=True, deptid=deptid)
            return render(request, 'jobportal/Admin/add_edit_department.html', args)
    else:
        department_instance = get_object_or_404(Department, id=deptid)
        args = dict(department_edit_form=AddEditDeartment(instance=department_instance), edit=True, deptid=deptid)
        return render(request, 'jobportal/Admin/add_edit_department.html', args)


# Delte an existing department
@login_required(login_url=ADMIN_LOGIN_URL)
def delete_department(request, deptid):
    dept_instance = get_object_or_404(Department, id=deptid)
    dept_instance.delete()
    return redirect("departments")


# All programmes
@login_required(login_url=ADMIN_LOGIN_URL)
def programmes(request):
    args = {'programmes': Programme.objects.all()}
    return render(request, 'jobportal/Admin/programmes.html', args)


# Add a programme
@login_required(login_url=ADMIN_LOGIN_URL)
def add_programme(request):
    if request.method == "POST":
        programme_form = AddEditProgramme(request.POST)
        if programme_form.is_valid():
            programme_form.save()
            return redirect('programmes')
        else:
            args = {'add_programme_form': programme_form, 'add': True}
            return render(request, 'jobportal/Admin/add_edit_programmes.html', args)
    else:
        args = {'add_programme_form': AddEditProgramme(), 'add': True}
        return render(request, 'jobportal/Admin/add_edit_programmes.html', args)


# Edit a programme
@login_required(login_url=ADMIN_LOGIN_URL)
def edit_programme(request, progid):
    if request.method == "POST":
        prog_instance = Programme.objects.get(id=progid)
        programe_form = AddEditProgramme(request.POST, prog_instance)
        if programe_form.is_valid():
            programe_form.save()
            return redirect('programmes')
        else:
            args = {'edit_programme_form': programe_form, 'edit': True, 'progid': progid}
            return render(request, 'jobportal/Admin/add_edit_programmes.html', args)
    else:
        prog_instance = Programme.objects.get(id=progid)
        args = {'edit_programme_form': AddEditProgramme(instance=prog_instance), 'edit': True, 'progid': progid}
        return render(request, 'jobportal/Admin/add_edit_programmes.html', args)


# Delete Programme
@login_required(login_url=ADMIN_LOGIN_URL)
def delete_programme(request, progid):
    prog_instance = get_object_or_404(Programme, id=progid)
    prog_instance.delete()
    return redirect("programmes")


# All years
@login_required(login_url=ADMIN_LOGIN_URL)
def years(request):
    args = {'years': Year.objects.all()}
    return render(request, 'jobportal/Admin/years.html', args)


# Add year
@login_required(login_url=ADMIN_LOGIN_URL)
def add_year(request):
    if request.method == "POST":
        add_year_form = AddEditYear(request.POST)
        if add_year_form.is_valid():
            add_year_form.save()
            return redirect('years')
        else:
            args = {'add_year_form': add_year_form, 'add': True}
            return render(request, 'jobportal/Admin/add_edit_years.html', args)
    else:
        args = {'add_year_form': AddEditYear(), 'add': True}
        return render(request, 'jobportal/Admin/add_edit_years.html', args)


# Edit year
@login_required(login_url=ADMIN_LOGIN_URL)
def edit_year(request, yearid):
    return HttpResponse("edit year")


# Delete year
@login_required(login_url=ADMIN_LOGIN_URL)
def delete_year(request, yearid):
    year_instacne = get_object_or_404(Year, id=yearid)
    year_instacne.delete()
    return redirect("years")


# All jobs
@login_required(login_url=ADMIN_LOGIN_URL)
def jobs(request):
    alljobs = Job.objects.all()
    args = {'jobs': alljobs}
    return render(request, "jobportal/Admin/jobs.html", args)


# Review a job
@login_required(login_url=ADMIN_LOGIN_URL)
def review_job(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    args = {'job_instance': job_instance}
    return render(request, 'jobportal/Admin/review_job.html', args)


# Edit job
@login_required(login_url=ADMIN_LOGIN_URL)
def edit_job(request, jobid):
    job = get_object_or_404(Job, id=jobid)
    if request.method == "POST":
        job_add_form = AdminJobEditForm(request.POST)
        if job_add_form.is_valid():
            job.description = job_add_form.cleaned_data['description']
            job.designation = job_add_form.cleaned_data['designation']
            job.cpi_shortlist = job_add_form.cleaned_data['cpi_shortlist']
            job.minimum_cpi = job_add_form.cleaned_data['minimum_cpi']
            job.percentage_x = job_add_form.cleaned_data['percentage_x']
            job.percentage_xii = job_add_form.cleaned_data['percentage_xii']
            job.other_requirements = job_add_form.cleaned_data['other_requirements']
            job.num_openings = job_add_form.cleaned_data['num_openings']
            job.currency = job_add_form.cleaned_data['currency']
            job.ctc_btech = job_add_form.cleaned_data['ctc_btech']
            job.ctc_mtech = job_add_form.cleaned_data['ctc_mtech']
            job.ctc_ma = job_add_form.cleaned_data['ctc_ma']
            job.ctc_msc = job_add_form.cleaned_data['ctc_msc']
            job.ctc_phd = job_add_form.cleaned_data['ctc_phd']
            job.gross_btech = job_add_form.cleaned_data['gross_btech']
            job.gross_mtech = job_add_form.cleaned_data['gross_mtech']
            job.gross_ma = job_add_form.cleaned_data['gross_ma']
            job.gross_msc = job_add_form.cleaned_data['gross_msc']
            job.gross_phd = job_add_form.cleaned_data['gross_phd']
            job.take_home_during_training = job_add_form.cleaned_data['take_home_during_training']
            job.take_home_after_training = job_add_form.cleaned_data['take_home_after_training']
            job.bonus = job_add_form.cleaned_data['bonus']
            job.bond = job_add_form.cleaned_data['bond']
            job.bond_details = job_add_form.cleaned_data['bond_details']
            job.profile_name = job_add_form.cleaned_data['profile_name']
            job.last_updated = datetime.now()
            # Dates
            job.opening_date = job_add_form.cleaned_data['opening_date']
            job.application_deadline = job_add_form.cleaned_data['application_deadline']
            # Save
            job.save()

            # dept_list = job_add_form.cleaned_data['dept']
            # current_year_list = job_add_form.cleaned_data['current_year']
            # prog_list = job_add_form.cleaned_data['prog']
            #
            # job.dept.clear()
            # job.current_year.clear()
            # job.prog.clear()
            #
            # for adept in dept_list:
            #     job.dept.add(adept)
            # for acurrent_year in current_year_list:
            #     job.current_year.add(acurrent_year)
            # for aprog in prog_list:
            #     job.prog.add(aprog)

            job.save()
            return redirect('review_job', jobid=jobid)
        else:
            print "Not saved"
            args = {'edit_job_form': job_add_form, 'job': job}
            return render(request, 'jobportal/Admin/edit_job.html', args)
    else:
        args = {'edit_job_form': AdminJobEditForm(initial={
            'description': job.description,
            'designation': job.designation,
            'cpi_shortlist': job.cpi_shortlist,
            'minimum_cpi': job.minimum_cpi,
            'percentage_x': job.percentage_x,
            'percentage_xii': job.percentage_xii,
            'num_openings': job.num_openings,
            'other_requirements': job.other_requirements,
            'currency': job.currency,
            'ctc_btech': job.ctc_btech,
            'ctc_mtech': job.ctc_mtech,
            'ctc_ma': job.ctc_msc,
            'ctc_msc': job.ctc_ma,
            'ctc_phd': job.ctc_phd,
            'gross_btech': job.gross_btech,
            'gross_mtech': job.gross_mtech,
            'gross_ma': job.gross_ma,
            'gross_msc': job.gross_msc,
            'gross_phd': job.gross_phd,
            'take_home_during_training': job.take_home_during_training,
            'take_home_after_training': job.take_home_after_training,
            'bonus': job.bonus,
            'bond': job.bond,
            'bond_details': job.bond_details,
            'profile_name': job.profile_name,
            'prog': job.prog.all(),
            'dept': job.dept.all(),
            'current_year': job.current_year.all(),
            'opening_date': job.opening_date,
            'application_deadline': job.application_deadline
        }), 'job': job}
        return render(request, 'jobportal/Admin/edit_job.html', args)


# Delete job
@login_required(login_url=ADMIN_LOGIN_URL)
def delete_job(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    job_instance.delete()
    return redirect("jobs")


# Approve job
@login_required(login_url=ADMIN_LOGIN_URL)
def approve_job(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    job_instance.approved = True
    job_instance.approved_on = datetime.now()
    job_instance.save()
    return redirect("review_job", jobid=job_instance.id)


# Send back a job for edits
@login_required(login_url=ADMIN_LOGIN_URL)
def sent_back_job(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    job_instance.sent_back = True
    job_instance.save()
    return redirect("review_job", jobid=job_instance.id)


# ADMIN USER MANAGEMENT
@login_required(login_url=ADMIN_LOGIN_URL)
def admin_manage(request):
    return render(request, "jobportal/Admin/admin_manage.html")


# Add student manually
@login_required(login_url=ADMIN_LOGIN_URL)
def add_student(request):
    if request.method == "POST":
        print "added start"
        add_student_form_data = AddStudent(request.POST)
        if add_student_form_data.is_valid():
            username = add_student_form_data.cleaned_data['username']
            password = add_student_form_data.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user_profile_instance = UserProfile.objects.create(user=user, login_type="Current Student")
            Student.objects.create(
                user=user_profile_instance,
                iitg_webmail=username,
                roll_no=add_student_form_data.cleaned_data['roll_no'],
                first_name=add_student_form_data.cleaned_data['first_name'],
                middle_name=add_student_form_data.cleaned_data['middle_name'],
                last_name=add_student_form_data.cleaned_data['last_name'],
                dob=add_student_form_data.cleaned_data['dob'],
                sex=add_student_form_data.cleaned_data['sex'],
                category=add_student_form_data.cleaned_data['category'],
                nationality=add_student_form_data.cleaned_data['nationality'],
                minor_programme=add_student_form_data.cleaned_data['minor_programme'],
                jee_air_rank=add_student_form_data.cleaned_data['jee_air_rank'],
                dept=add_student_form_data.cleaned_data['dept'],
                year=add_student_form_data.cleaned_data['year'],
                prog=add_student_form_data.cleaned_data['prog'],
                room_no=add_student_form_data.cleaned_data['room_no'],
                hostel=add_student_form_data.cleaned_data['hostel'],
                alternative_email=add_student_form_data.cleaned_data['alternative_email'],
                mobile_campus_alternative=add_student_form_data.cleaned_data['mobile_campus_alternative'],
                mobile_campus=add_student_form_data.cleaned_data['mobile_campus'],
                mobile_home=add_student_form_data.cleaned_data['mobile_home'],
                address_line1=add_student_form_data.cleaned_data['address_line1'],
                address_line2=add_student_form_data.cleaned_data['address_line2'],
                address_line3=add_student_form_data.cleaned_data['address_line3'],
                pin_code=add_student_form_data.cleaned_data['pin_code'],
                percentage_x=add_student_form_data.cleaned_data['percentage_x'],
                percentage_xii=add_student_form_data.cleaned_data['percentage_xii'],
                gap_in_study=add_student_form_data.cleaned_data['gap_in_study'],
                gap_reason=add_student_form_data.cleaned_data['gap_reason'],
                linkedin_link=add_student_form_data.cleaned_data['linkedin_link'],
                ppo=add_student_form_data.cleaned_data['ppo'],
                intern2=add_student_form_data.cleaned_data['intern2'],
                intern3=add_student_form_data.cleaned_data['intern3'],
                cpi=add_student_form_data.cleaned_data['cpi'],
                spi_1_sem=add_student_form_data.cleaned_data['spi_1_sem'],
                spi_2_sem=add_student_form_data.cleaned_data['spi_2_sem'],
                spi_3_sem=add_student_form_data.cleaned_data['spi_3_sem'],
                spi_4_sem=add_student_form_data.cleaned_data['spi_4_sem'],
                spi_5_sem=add_student_form_data.cleaned_data['spi_5_sem'],
                spi_6_sem=add_student_form_data.cleaned_data['spi_6_sem']
            )
            args = {'created': 'Student', 'webmail': username}
            return render(request, 'jobportal/Admin/admin_manage.html', args)
        else:
            print "invalid"
            add_student_form = add_student_form_data
            args = {'add_student_form': add_student_form}
            return render(request, 'jobportal/Admin/add_student.html', args)
    else:
        add_student_form = AddStudent()
        args = {'add_student_form': add_student_form}
        return render(request, 'jobportal/Admin/add_student.html', args)


# Search Student by Department, Year and Programme
@login_required(login_url=ADMIN_LOGIN_URL)
def search_students(request):
    if request.method == "POST":
        studentsearch_form_data = StudentSearchForm(request.POST)
        if studentsearch_form_data.is_valid():
            student_programme = studentsearch_form_data.cleaned_data['programme']
            student_year = studentsearch_form_data.cleaned_data['year']
            student_departent = studentsearch_form_data.cleaned_data['department']
            students_list = Student.objects.all().filter(
                prog__name=student_programme).filter(
                dept__dept_code=student_departent).filter(
                year__current_year=student_year)

            args = {'students_list': students_list, 'student_search_form': studentsearch_form_data}
            return render(request, 'jobportal/Admin/all_users.html', args)
        else:
            args = {'student_search_form': studentsearch_form_data}
            return render(request, 'jobportal/Admin/all_users.html', args)
    else:
        args = {'student_search_form': StudentSearchForm()}
        return render(request, 'jobportal/Admin/all_users.html', args)


# Review student profile
@login_required(login_url=ADMIN_LOGIN_URL)
def review_stud_profile(request, studid):
    try:
        student_instance = Student.objects.get(id=studid)
        args = {'edited': 'Student', 'student_instance': student_instance}
        return render(request, 'jobportal/Admin/review_profile.html', args)
    except:
        raise Http404("Error 404")


# Edit student profile
@login_required(login_url=ADMIN_LOGIN_URL)
def edit_student(request, studid):
    if request.method == "POST":
        edit_student_form_data = EditStudentAdmin(request.POST)
        if edit_student_form_data.is_valid():
            student_instance = get_object_or_404(Student, id=studid)
            student_instance.roll_no = edit_student_form_data.cleaned_data['roll_no']
            student_instance.first_name = edit_student_form_data.cleaned_data['first_name']
            student_instance.middle_name = edit_student_form_data.cleaned_data['middle_name']
            student_instance.last_name = edit_student_form_data.cleaned_data['last_name']
            student_instance.dob = edit_student_form_data.cleaned_data['dob']
            student_instance.sex = edit_student_form_data.cleaned_data['sex']
            student_instance.category = edit_student_form_data.cleaned_data['category']
            student_instance.nationality = edit_student_form_data.cleaned_data['nationality']
            student_instance.minor_programme = edit_student_form_data.cleaned_data['minor_programme']
            student_instance.jee_air_rank = edit_student_form_data.cleaned_data['jee_air_rank']
            student_instance.hostel = edit_student_form_data.cleaned_data['hostel']
            student_instance.room_no = edit_student_form_data.cleaned_data['room_no']
            student_instance.alternative_email = edit_student_form_data.cleaned_data['alternative_email']
            student_instance.mobile_campus = edit_student_form_data.cleaned_data['mobile_campus']
            student_instance.mobile_campus_alternative = edit_student_form_data.cleaned_data[
                'mobile_campus_alternative']
            student_instance.mobile_home = edit_student_form_data.cleaned_data['mobile_home']
            student_instance.dept = edit_student_form_data.cleaned_data['dept']
            student_instance.year = edit_student_form_data.cleaned_data['year']
            student_instance.prog = edit_student_form_data.cleaned_data['prog']
            student_instance.address_line1 = edit_student_form_data.cleaned_data['address_line1']
            student_instance.address_line2 = edit_student_form_data.cleaned_data['address_line2']
            student_instance.address_line3 = edit_student_form_data.cleaned_data['address_line3']
            student_instance.pin_code = edit_student_form_data.cleaned_data['pin_code']
            student_instance.percentage_xii = edit_student_form_data.cleaned_data['percentage_xii']
            student_instance.percentage_x = edit_student_form_data.cleaned_data['percentage_x']
            student_instance.gap_reason = edit_student_form_data.cleaned_data['gap_reason']
            student_instance.gap_in_study = edit_student_form_data.cleaned_data['gap_in_study']
            student_instance.ppo = edit_student_form_data.cleaned_data['ppo']
            student_instance.intern2 = edit_student_form_data.cleaned_data['intern2']
            student_instance.intern3 = edit_student_form_data.cleaned_data['intern3']
            student_instance.cpi = edit_student_form_data.cleaned_data['cpi']
            student_instance.spi_1_sem = edit_student_form_data.cleaned_data['spi_1_sem']
            student_instance.spi_2_sem = edit_student_form_data.cleaned_data['spi_2_sem']
            student_instance.spi_3_sem = edit_student_form_data.cleaned_data['spi_3_sem']
            student_instance.spi_4_sem = edit_student_form_data.cleaned_data['spi_4_sem']
            student_instance.spi_5_sem = edit_student_form_data.cleaned_data['spi_5_sem']
            student_instance.spi_6_sem = edit_student_form_data.cleaned_data['spi_6_sem']
            student_instance.save()
            return redirect('review_stud_profile', studid=studid)
        else:
            args = {'student_profile_edit_form': edit_student_form_data, 'studid': studid}
            return render(request, 'jobportal/Admin/edit_student_profile.html', args)
    else:
        args = {}
        args.update(csrf(request))
        student_instance = Student.objects.get(id=studid)
        args['student_profile_edit_form'] = EditStudentAdmin(initial={
            'roll_no': student_instance.roll_no,
            'first_name': student_instance.first_name,
            'middle_name': student_instance.middle_name,
            'last_name': student_instance.last_name,
            'dob': student_instance.dob,
            'sex': student_instance.sex,
            'category': student_instance.category,
            'nationality': student_instance.nationality,
            'minor_programme': student_instance.minor_programme,
            'jee_air_rank': student_instance.jee_air_rank,
            'dept': student_instance.dept,
            'year': student_instance.year,
            'prog': student_instance.prog,
            'hostel': student_instance.hostel,
            'room_no': student_instance.room_no,
            'alternative_email': student_instance.alternative_email,
            'mobile_campus': student_instance.mobile_campus,
            'mobile_campus_alternative': student_instance.mobile_campus_alternative,
            'mobile_home': student_instance.mobile_home,
            'address_line1': student_instance.address_line1,
            'address_line2': student_instance.address_line2,
            'address_line3': student_instance.address_line3,
            'pin_code': student_instance.pin_code,
            'percentage_x': student_instance.percentage_x,
            'percentage_xii': student_instance.percentage_xii,
            'gap_in_study': student_instance.gap_in_study,
            'gap_reason': student_instance.gap_reason,
            'ppo': student_instance.ppo,
            'intern2': student_instance.intern2,
            'intern3': student_instance.intern3,
            'cpi': student_instance.cpi,
            'spi_1_sem': student_instance.spi_1_sem,
            'spi_2_sem': student_instance.spi_2_sem,
            'spi_3_sem': student_instance.spi_3_sem,
            'spi_4_sem': student_instance.spi_4_sem,
            'spi_5_sem': student_instance.spi_5_sem,
            'spi_6_sem': student_instance.spi_6_sem
        })
        args['studid'] = studid
        return render(request, 'jobportal/Admin/edit_student_profile.html', args)


# All companies
@login_required(login_url=ADMIN_LOGIN_URL)
def companies(request):
    comapnies = Company.objects.all()
    args = {'companies': comapnies}
    return render(request, "jobportal/Admin/companies.html", args)


# Add company manually
@login_required(login_url=ADMIN_LOGIN_URL)
def add_company(request):
    if request.method == "POST":
        add_company_form_data = AddCompany(request.POST)
        if add_company_form_data.is_valid():
            username = add_company_form_data.cleaned_data['username']
            password = add_company_form_data.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user_profile_instance = UserProfile.objects.create(user=user, login_type="Company")
            Company.objects.create(
                user=user_profile_instance,
                company_name=add_company_form_data.cleaned_data['company_name'],
                description=add_company_form_data.cleaned_data['description'],
                website=add_company_form_data.cleaned_data['website'],
                organization_type=add_company_form_data.cleaned_data['organization_type'],
                industry_sector=add_company_form_data.cleaned_data['industry_sector'],
                head_hr_designation=add_company_form_data.cleaned_data['head_hr_designation'],
                head_hr_email=add_company_form_data.cleaned_data['head_hr_email'],
                head_hr_mobile=add_company_form_data.cleaned_data['head_hr_mobile'],
                head_hr_fax=add_company_form_data.cleaned_data['head_hr_fax'],
                first_hr_name=add_company_form_data.cleaned_data['first_hr_name'],
                first_hr_designation=add_company_form_data.cleaned_data['first_hr_designation'],
                first_hr_email=add_company_form_data.cleaned_data['first_hr_email'],
                first_hr_mobile=add_company_form_data.cleaned_data['first_hr_mobile'],
                first_hr_fax=add_company_form_data.cleaned_data['first_hr_fax'],
                second_hr_name=add_company_form_data.cleaned_data['second_hr_name'],
                second_hr_email=add_company_form_data.cleaned_data['second_hr_email'],
                second_hr_designation=add_company_form_data.cleaned_data['second_hr_designation'],
                second_hr_mobile=add_company_form_data.cleaned_data['second_hr_mobile'],
                second_hr_fax=add_company_form_data.cleaned_data['second_hr_fax'],
                approved=add_company_form_data.cleaned_data['approved'],
                sent_back=add_company_form_data.cleaned_data['sent_back']
            )
            messages.add_message(request, messages.SUCCESS, "Company " + add_company_form_data.cleaned_data[
                'company_name'] + " has been successfully added.")
            return redirect("companies")
        else:
            add_company_form = add_company_form_data
            args = {'add_company_form': add_company_form, 'request': False}
            return render(request, 'jobportal/Admin/add_company.html', args)
    else:
        add_company_form = AddCompany()
        args = {'add_company_form': add_company_form, 'request': False}
        return render(request, 'jobportal/Admin/add_company.html', args)


# Review company profile
@login_required(login_url=ADMIN_LOGIN_URL)
def review_company_profile(request, companyid):
    company_instance = get_object_or_404(Company, id=companyid)
    args = {'edited': 'Company', 'company_instance': company_instance}
    return render(request, 'jobportal/Admin/review_profile.html', args)


# Delete an existing company profile
@login_required(login_url=ADMIN_LOGIN_URL)
def delete_company(request, companyid):
    company_instance = get_object_or_404(Company, id=companyid)
    user_instance = User.objects.get(username=company_instance.user.user.username)
    user_instance.delete()
    return redirect('companies')


@login_required(login_url=ADMIN_LOGIN_URL)
def edit_company(request, companyid):
    """
    Edit an existing Company instance.
    :param request: HttpRequest object
    :param companyid: id of Company instance
    :return: HttpResponse
    """
    if request.method == "POST":
        # parse submitted form data
        edit_company_data = EditCompany(request.POST)
        # if form is valid
        if edit_company_data.is_valid():
            # TODO : Convert this to model form
            # TODO : Use create_instance method instead of line by line adding
            company_instance = get_object_or_404(Company, id=companyid)
            company_instance.company_name = edit_company_data.cleaned_data['company_name']
            company_instance.description = edit_company_data.cleaned_data['description']
            company_instance.website = edit_company_data.cleaned_data['website']
            company_instance.organization_type = edit_company_data.cleaned_data['organization_type']
            company_instance.industry_sector = edit_company_data.cleaned_data['industry_sector']
            company_instance.head_hr_designation = edit_company_data.cleaned_data['head_hr_designation']
            company_instance.head_hr_email = edit_company_data.cleaned_data['head_hr_email']
            company_instance.head_hr_mobile = edit_company_data.cleaned_data['head_hr_mobile']
            company_instance.head_hr_fax = edit_company_data.cleaned_data['head_hr_fax']
            company_instance.first_hr_name = edit_company_data.cleaned_data['first_hr_name']
            company_instance.first_hr_designation = edit_company_data.cleaned_data['first_hr_designation']
            company_instance.first_hr_email = edit_company_data.cleaned_data['first_hr_email']
            company_instance.first_hr_mobile = edit_company_data.cleaned_data['first_hr_mobile']
            company_instance.first_hr_fax = edit_company_data.cleaned_data['first_hr_fax']
            company_instance.second_hr_name = edit_company_data.cleaned_data['second_hr_name']
            company_instance.second_hr_email = edit_company_data.cleaned_data['second_hr_email']
            company_instance.second_hr_designation = edit_company_data.cleaned_data['second_hr_designation']
            company_instance.second_hr_mobile = edit_company_data.cleaned_data['second_hr_mobile']
            company_instance.second_hr_fax = edit_company_data.cleaned_data['second_hr_fax']
            company_instance.approved = edit_company_data.cleaned_data['approved']
            company_instance.sent_back = edit_company_data.cleaned_data['sent_back']
            company_instance.save()
            return redirect('review_company_profile', companyid=companyid)
        else:
            args = dict(company_profile_edit_form=edit_company_data, companyid=companyid)
            return render(request, 'jobportal/Admin/edit_company_profile.html', args)
    else:
        args = {}
        args.update(csrf(request))
        company_instance = get_object_or_404(Company, id=companyid)
        args['company_profile_edit_form'] = EditCompany(initial={
            # 'username': company_instance.user.user.username,
            'company_name': company_instance.company_name,
            'description': company_instance.description,
            'website': company_instance.website,
            'organization_type': company_instance.organization_type,
            'industry_sector': company_instance.industry_sector,
            'head_hr_designation': company_instance.head_hr_designation,
            'head_hr_email': company_instance.head_hr_email,
            'head_hr_mobile': company_instance.head_hr_mobile,
            'head_hr_fax': company_instance.head_hr_fax,
            'first_hr_name': company_instance.first_hr_name,
            'first_hr_designation': company_instance.first_hr_designation,
            'first_hr_email': company_instance.first_hr_email,
            'first_hr_mobile': company_instance.first_hr_mobile,
            'first_hr_fax': company_instance.first_hr_fax,
            'second_hr_name': company_instance.second_hr_name,
            'second_hr_email': company_instance.second_hr_email,
            'second_hr_designation': company_instance.second_hr_designation,
            'second_hr_mobile': company_instance.second_hr_mobile,
            'second_hr_fax': company_instance.second_hr_fax,
            'approved': company_instance.approved,
            'sent_back': company_instance.sent_back
        })
        args['companyid'] = companyid
        return render(request, 'jobportal/Admin/edit_company_profile.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def signup_requests(request):
    """
    View Company signup requests.
    :param request: HttpResquest object
    :return: HttpResponse object
    """
    args = dict(requests=CompanyReg.objects.all())
    return render(request, 'jobportal/Admin/signup_requests.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def del_signup_request(request, companyregid):
    """
    Delete Company signup requests.
    :param request: HttpRequest object
    :param companyregid: id of CompanyReg instance
    :return: HttpResponse object
    """
    companyreg_instance = get_object_or_404(CompanyReg, id=companyregid)
    companyreg_instance.delete()
    return redirect("signup_requests")


@login_required(login_url=ADMIN_LOGIN_URL)
def review_request_profile(request, companyregid):
    companyreg_instance = CompanyReg.objects.get(id=companyregid)
    args = {'edited': 'Request', 'request': companyreg_instance}
    return render(request, 'jobportal/Admin/review_profile.html', args)


# Approve company signup request
@login_required(login_url=ADMIN_LOGIN_URL)
def add_company_by_signup_request(request, companyregid):
    if request.method == "POST":
        add_company_form_data = AddCompany(request.POST)
        if add_company_form_data.is_valid():
            username = add_company_form_data.cleaned_data['username']
            password = add_company_form_data.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user_profile_instance = UserProfile.objects.create(user=user, login_type="Company")
            company_instance = Company.objects.create(
                user=user_profile_instance,
                company_name=add_company_form_data.cleaned_data['company_name'],
                description=add_company_form_data.cleaned_data['description'],
                website=add_company_form_data.cleaned_data['website'],
                organization_type=add_company_form_data.cleaned_data['organization_type'],
                industry_sector=add_company_form_data.cleaned_data['industry_sector'],
                head_hr_designation=add_company_form_data.cleaned_data['head_hr_designation'],
                head_hr_email=add_company_form_data.cleaned_data['head_hr_email'],
                head_hr_mobile=add_company_form_data.cleaned_data['head_hr_mobile'],
                head_hr_fax=add_company_form_data.cleaned_data['head_hr_fax'],
                first_hr_name=add_company_form_data.cleaned_data['first_hr_name'],
                first_hr_designation=add_company_form_data.cleaned_data['first_hr_designation'],
                first_hr_email=add_company_form_data.cleaned_data['first_hr_email'],
                first_hr_mobile=add_company_form_data.cleaned_data['first_hr_mobile'],
                first_hr_fax=add_company_form_data.cleaned_data['first_hr_fax'],
                second_hr_name=add_company_form_data.cleaned_data['second_hr_name'],
                second_hr_email=add_company_form_data.cleaned_data['second_hr_email'],
                second_hr_designation=add_company_form_data.cleaned_data['second_hr_designation'],
                second_hr_mobile=add_company_form_data.cleaned_data['second_hr_mobile'],
                second_hr_fax=add_company_form_data.cleaned_data['second_hr_fax'],
                approved=add_company_form_data.cleaned_data['approved'],
                sent_back=add_company_form_data.cleaned_data['sent_back']
            )
            print "Test Starts"
            print company_instance.company_name
            companyreg_instance = CompanyReg.objects.get(company_name_reg=company_instance.company_name)
            print companyreg_instance.company_name_reg
            companyreg_instance.delete()
            print "Test Ends"
            messages.add_message(request, messages.SUCCESS, "Company " + add_company_form_data.cleaned_data[
                'company_name'] + " has been successfully added.")
            return redirect("companies")
        else:
            add_company_form = add_company_form_data
            args = {'add_company_form': add_company_form, 'request': True, 'companyregid': companyregid}
            return render(request, 'jobportal/Admin/add_company.html', args)
    else:
        companyreg_instance = CompanyReg.objects.get(id=companyregid)
        add_company_form = AddCompany(initial={
            'company_name': companyreg_instance.company_name_reg,
            'description': companyreg_instance.description_reg,
            'website': companyreg_instance.website_reg,
            'organization_type': companyreg_instance.organization_type_reg,
            'industry_sector': companyreg_instance.industry_sector_reg,
            'head_hr_designation': companyreg_instance.head_hr_designation_reg,
            'head_hr_email': companyreg_instance.head_hr_email_reg,
            'head_hr_mobile': companyreg_instance.head_hr_mobile_reg,
            'head_hr_fax': companyreg_instance.head_hr_fax_reg,
            'first_hr_name': companyreg_instance.first_hr_name_reg,
            'first_hr_designation': companyreg_instance.first_hr_designation_reg,
            'first_hr_email': companyreg_instance.first_hr_email_reg,
            'first_hr_mobile': companyreg_instance.first_hr_mobile_reg,
            'first_hr_fax': companyreg_instance.first_hr_fax_reg,
            'second_hr_name': companyreg_instance.second_hr_name_reg,
            'second_hr_email': companyreg_instance.second_hr_email_reg,
            'second_hr_designation': companyreg_instance.second_hr_designation_reg,
            'second_hr_mobile': companyreg_instance.second_hr_mobile_reg,
            'second_hr_fax': companyreg_instance.second_hr_fax_reg
        })
        args = {'add_company_form': add_company_form, 'request': True, 'companyregid': companyregid}
        return render(request, 'jobportal/Admin/add_company.html', args)


# Student job relation
@login_required(login_url=ADMIN_LOGIN_URL)
def stud_relation(request, jobid, studid):
    stud_instance = get_object_or_404(Student, id=studid)
    job_instance = get_object_or_404(Job, id=jobid)
    relation_instance = get_object_or_404(StudentJobRelation, stud=stud_instance, job=job_instance)
    args = {'relation_instance': relation_instance, 'stud_instance': stud_instance, 'job_instance': job_instance}
    return render(request, "jobportal/Admin/review_job_relation.html", args)


# Alumni job relation
@login_required(login_url=ADMIN_LOGIN_URL)
def alum_relation(request, jobid, alumid):
    alum_instance = get_object_or_404(Alumni, id=alumid)
    job_instance = get_object_or_404(Job, id=jobid)
    relation_instance = get_object_or_404(AlumJobRelation, alum=alum_instance, job=job_instance)
    args = {'relation_instance': relation_instance, 'alum_instance': alum_instance, 'job_instance': job_instance}
    return render(request, "jobportal/Admin/review_job_relation.html", args)


@login_required(login_url=ADMIN_LOGIN_URL)
def approve_stud_relation(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    if relation_instance.placed_init is True:
        if relation_instance.placed_approved is not True:
            relation_instance.placed_approved = True
            relation_instance.save()
    if relation_instance.ppo_init is True and relation_instance.ppo_accepted is True:
        if relation_instance.ppo_approved is not True:
            relation_instance.ppo_approved = True
            relation_instance.save()
    return redirect("approve_action", applicant_type="stud", relationid=relationid)


@login_required(login_url=ADMIN_LOGIN_URL)
def approve_alum_relation(request, relationid):
    relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    if relation_instance.placed_init is True:
        if relation_instance.placed_approved is not True:
            relation_instance.placed_approved = True
            relation_instance.save()
    return redirect("approve_action", applicant_type="alum", relationid=relationid)


@login_required(login_url=ADMIN_LOGIN_URL)
def job_candidates(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    relation_list_stud = StudentJobRelation.objects.all().filter(job=job_instance)
    relation_list_alum = AlumJobRelation.objects.all().filter(job=job_instance)
    args = {
        'relation_list_alum': relation_list_alum,
        'relation_list_stud': relation_list_stud,
        'job_instance': job_instance
    }
    return render(request, 'jobportal/Admin/job_candidates.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def approve_action(request, applicant_type, relationid):
    if applicant_type == "stud":
        relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    if applicant_type == "alum":
        relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    args = {'relation_instance': relation_instance, 'applicant_type': applicant_type}
    return render(request, 'jobportal/Admin/approve_actions.html', args)


# New approval views
@login_required(login_url=ADMIN_LOGIN_URL)
def admin_approvals(request, object_type):
    if str(object_type) == "job":
        job_list = Job.objects.all().filter(approved__isnull=True)
        return render(request, 'jobportal/Admin/unapprv_job.html', {'job_list': job_list})
    elif str(object_type) == "ppo":
        ppo_list = StudentJobRelation.objects.all().filter(ppo_init=True, ppo_approved__isnull=True)
        return render(request, 'jobportal/Admin/unapprv_ppo.html', {'ppo_list': ppo_list})
    elif str(object_type) == "place":
        student_list = StudentJobRelation.objects.all().filter(placed_init=True).filter(placed_approved__isnull=True)
        alum_list = AlumJobRelation.objects.all().filter(placed_init=True).filter(placed_approved__isnull=True)
        print len(student_list)
        print len(alum_list)
        args = {'student_list': student_list, 'alum_list': alum_list}
        return render(request, 'jobportal/Admin/unapprv_place.html', args)
    else:
        return redirect("admin_home")