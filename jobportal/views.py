# Author:
# Name: Narendra Choudhary
# Email : n.choudhary@iitg.ernet.in

# Warning:
# DO NOT try to optimize the code before reading the complete documentation
# at least 2 times.
# DO NOT make any assumption about anything. Double check the documentation.


from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from .models import UserProfile, Student, Alumni, Company, \
    Job, Event, StudentJobRelation
from .forms import StudentLoginForm, EditStudProfileForm, StudCVForm, \
    RequestEventForm, SelectCVForm
from datetime import datetime
from reportlab.pdfgen import canvas
from io import BytesIO

STUD_LOGIN_URL = reverse_lazy('jobportal/stud_login')
ALUM_LOGIN_URL = reverse_lazy('jobportal/alum_login')
COMPANY_LOGIN_URL = reverse_lazy('jobportal/companylogin')


def get_questions(studid):
    """
    Returns list of student's CV to be selected before application
    :param studid: id of Student instance
    :return: list of CVs uploaded
    """
    stud_instance = get_object_or_404(Student, id=studid)
    questions = []
    if bool(stud_instance.cv1):
        questions.append("cv1")
    if bool(stud_instance.cv2):
        questions.append("cv2")
    return questions


def index(request):
    """
    Serves the landing page.
    :param request: HTTP Request object
    :return: HTTP Response object
    """
    args = {}
    args.update(csrf(request))
    return render(request, 'jobportal/index.html', args)


def stud_login(request):
    """
    Handles student login functionality.
    :param request: HTTP Request object
    :return: HTTP Response object
    """
    if request.method == "POST":
        student_login_form_data = StudentLoginForm(request.POST)
        if student_login_form_data.is_valid():
            # get username
            username = student_login_form_data.cleaned_data['username']
            password = student_login_form_data.cleaned_data['password']
            # authenticate
            user = auth.authenticate(username=username, password=password)
            # if authenticated
            if user is not None:
                # get username from User instance
                current_user = User.objects.get(username=username)
                # get corresponding UserProfile instance
                user_profile = UserProfile.objects.get(user=current_user)
                # if UserProfile instance is Student
                if user_profile.login_type == "Current Student":
                    # login User
                    auth.login(request, user)
                    student_instance = Student.objects.get(iitg_webmail=username)
                    request.session['student_instance_id'] = student_instance.id
                    request.session['user_type'] = 'Student'
                    return redirect('stud_home')
                # User exists but is not Student
                # TODO : Add redirect to correct login page
                else:
                    args = dict(login_form=student_login_form_data)
                    return render(request, 'jobportal/Student/stud_login.html', args)
            # either username-password mismatch or User doesn't exist
            else:
                args = dict(login_form=student_login_form_data)
                return render(request, 'jobportal/Student/stud_login.html', args)
        # invalid form submission
        else:
            args = dict(login_form=student_login_form_data)
            return render(request, 'jobportal/Student/stud_login.html', args)
    else:
        args = dict(login_form=StudentLoginForm())
        return render(request, 'jobportal/Student/stud_login.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def stud_logout(request):
    """
    Logout Student.
    :param request: HTTP Request object
    :return: HTTP Response object
    """
    auth.logout(request)
    return render(request, 'jobportal/logout.html')


@login_required(login_url=STUD_LOGIN_URL)
def stud_home(request):
    """
    Render Student home.
    :param request: HTTP Request object
    :return: HTTP Response object
    """
    try:
        student_instance = Student.objects.get(id=request.session['student_instance_id'])
    except:
        raise Http404("Error 404")
    args = dict(stud=student_instance)
    return render(request, 'jobportal/Student/stud_home.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def edit_stud_profile(request):
    try:
        student_instance = Student.objects.get(id=request.session['student_instance_id'])
    except:
        raise Http404("Error 404")
    if request.method == "POST":
        edit_stud_form_data = EditStudProfileForm(request.POST)
        if edit_stud_form_data.is_valid():
            student_instance.dob = edit_stud_form_data.cleaned_data['dob']
            student_instance.sex = edit_stud_form_data.cleaned_data['sex']
            student_instance.category = edit_stud_form_data.cleaned_data['category']
            student_instance.nationality = edit_stud_form_data.cleaned_data['nationality']
            student_instance.minor_programme = edit_stud_form_data.cleaned_data['minor_programme']
            student_instance.jee_air_rank = edit_stud_form_data.cleaned_data['jee_air_rank']
            student_instance.room_no = edit_stud_form_data.cleaned_data['room_no']
            student_instance.hostel = edit_stud_form_data.cleaned_data['hostel']
            student_instance.alternative_email = edit_stud_form_data.cleaned_data['alternative_email']
            student_instance.mobile_campus_alternative = edit_stud_form_data.cleaned_data['mobile_campus_alternative']
            student_instance.mobile_campus = edit_stud_form_data.cleaned_data['mobile_campus']
            student_instance.mobile_home = edit_stud_form_data.cleaned_data['mobile_home']
            student_instance.address_line1 = edit_stud_form_data.cleaned_data['address_line1']
            student_instance.address_line2 = edit_stud_form_data.cleaned_data['address_line2']
            student_instance.address_line3 = edit_stud_form_data.cleaned_data['address_line3']
            student_instance.pin_code = edit_stud_form_data.cleaned_data['pin_code']
            student_instance.dept = edit_stud_form_data.cleaned_data['dept']
            student_instance.prog = edit_stud_form_data.cleaned_data['prog']
            student_instance.percentage_x = edit_stud_form_data.cleaned_data['percentage_x']
            student_instance.percentage_xii = edit_stud_form_data.cleaned_data['percentage_xii']
            student_instance.board_x = edit_stud_form_data.cleaned_data['board_x']
            student_instance.board_xii = edit_stud_form_data.cleaned_data['board_xii']
            student_instance.medium_x = edit_stud_form_data.cleaned_data['medium_x']
            student_instance.medium_xii = edit_stud_form_data.cleaned_data['medium_xii']
            student_instance.passing_year_x = edit_stud_form_data.cleaned_data['passing_year_x']
            student_instance.passing_year_xii = edit_stud_form_data.cleaned_data['passing_year_xii']
            student_instance.gap_in_study = edit_stud_form_data.cleaned_data['gap_in_study']
            student_instance.gap_reason = edit_stud_form_data.cleaned_data['gap_reason']
            student_instance.linkedin_link = edit_stud_form_data.cleaned_data['linkedin_link']
            student_instance.cpi = edit_stud_form_data.cleaned_data['cpi']
            student_instance.spi_1_sem = edit_stud_form_data.cleaned_data['spi_1_sem']
            student_instance.spi_2_sem = edit_stud_form_data.cleaned_data['spi_2_sem']
            student_instance.spi_3_sem = edit_stud_form_data.cleaned_data['spi_3_sem']
            student_instance.spi_4_sem = edit_stud_form_data.cleaned_data['spi_4_sem']
            student_instance.spi_5_sem = edit_stud_form_data.cleaned_data['spi_5_sem']
            student_instance.spi_6_sem = edit_stud_form_data.cleaned_data['spi_6_sem']
            student_instance.save()
            return redirect('stud_home')
        else:
            args = dict(edit_stud_profile_form=edit_stud_form_data)
            return render(request, 'jobportal/Student/editstudprofile.html', args)
    else:
        args = {}
        args.update(csrf(request))
        args['edit_stud_profile_form'] = EditStudProfileForm(initial={
            'iitg_webmail': student_instance.iitg_webmail,
            'roll_no': student_instance.roll_no,
            'first_name': student_instance.first_name,
            'middle_name': student_instance.middle_name,
            'last_name': student_instance.last_name,
            'dept': student_instance.dept,
            'prog': student_instance.prog,
            'dob': student_instance.dob,
            'sex': student_instance.sex,
            'category': student_instance.category,
            'nationality': student_instance.nationality,
            'minor_programme': student_instance.minor_programme,
            'jee_air_rank': student_instance.jee_air_rank,
            'room_no': student_instance.room_no,
            'hostel': student_instance.hostel,
            'alternative_email': student_instance.alternative_email,
            'mobile_campus': student_instance.mobile_campus,
            'mobile_campus_alternative': student_instance.mobile_campus_alternative,
            'mobile_home': student_instance.mobile_home,
            'address_line1': student_instance.address_line1,
            'address_line2': student_instance.address_line2,
            'address_line3': student_instance.address_line3,
            'percentage_x': student_instance.percentage_x,
            'percentage_xii': student_instance.percentage_xii,
            'board_x': student_instance.board_x,
            'board_xii': student_instance.board_xii,
            'medium_x': student_instance.medium_x,
            'medium_xii': student_instance.medium_xii,
            'passing_year_x': student_instance.passing_year_x,
            'passing_year_xii': student_instance.passing_year_xii,
            'gap_in_study': student_instance.gap_in_study,
            'gap_reason': student_instance.gap_reason,
            'linkedin_link': student_instance.linkedin_link,
            'cpi': student_instance.cpi,
            'spi_1_sem': student_instance.spi_1_sem,
            'spi_2_sem': student_instance.spi_2_sem,
            'spi_3_sem': student_instance.spi_3_sem,
            'spi_4_sem': student_instance.spi_4_sem,
            'spi_5_sem': student_instance.spi_5_sem,
            'spi_6_sem': student_instance.spi_6_sem
        })
        return render(request, 'jobportal/Student/editstudprofile.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def stud_viewjobs(request):
    """
    Fetch jobs open for application.
    :param request: HTTP Request object
    :return: HTTP Response object
    """
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    job_list = Job.objects.all()
    for job in job_list:
        if job.cpi_shortlist:
            if job.minimum_cpi > student_instance.cpi:
                job_list.remove(job)
    args = {'job_list': job_list}
    return render(request, 'jobportal/Student/studjobs.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def stud_applyjob(request, jobid):
    """
    Apply for an open job
    :param request: HttpRequest object
    :param jobid: Id of Job instance
    :return: HttpResponse object
    """
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    job_instance = get_object_or_404(Job, id=jobid)
    form = SelectCVForm(request.POST or None, extra=get_questions(student_instance.id))
    if request.method == "POST":
        if form.is_valid():
            relation_instance = StudentJobRelation(
                stud=student_instance,
                job=job_instance,
                placed_init=False,
                shortlist_status=False
            )
            relation_instance.save()
            for (question, answer) in form.extra_answers():
                setattr(relation_instance, question, answer)
            relation_instance.save()
            return redirect('jobdetails', jobid=jobid)
        else:
            args = {'form': form, 'jobid': jobid}
            return render(request, 'jobportal/Student/apply.html', args)
    else:
        args = {'form': form, 'jobid': jobid}
        return render(request, 'jobportal/Student/apply.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def stud_deapplyjob(request, jobid):
    """
    Remove application from a job.
    :param request: HttpRequest object
    :param jobid: id of Job instance
    :return: HttpResponse object
    """
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    job_instance = Job.objects.get(id=jobid)
    relation_instance = get_object_or_404(StudentJobRelation, stud=student_instance, job=job_instance)
    relation_instance.delete()
    return redirect('jobdetails', jobid=jobid)


@login_required(login_url=STUD_LOGIN_URL)
def stud_jobsappliedfor(request):
    """
    Fetch all Jobs to which Student has applied,
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    job_list = student_instance.job_set.all()
    args = {'job_list': job_list}
    return render(request, 'jobportal/Student/appliedfor.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def stud_jobdetails(request, jobid):
    """
    Details of a job instance
    :param request: HttpRequest instance
    :param jobid: id of Job instance
    :return: HttpResponse object
    """
    job_instance = get_object_or_404(Job, id=jobid)
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    deadline_gone = True if job_instance.application_deadline < datetime.now().date() else False
    nocv = True if not bool(student_instance.cv1) and not bool(student_instance.cv2) else False
    args = {'job_instance': job_instance, 'deadline_gone': deadline_gone, 'nocv': nocv}
    try:
        relation_instance = StudentJobRelation.objects.get(stud=student_instance, job=job_instance)
    except StudentJobRelation.DoesNotExist:
        relation_instance = None
    args['relation_instance'] = relation_instance
    return render(request, "jobportal/Student/jobdetail.html", args)


@login_required(login_url=STUD_LOGIN_URL)
def view_cvs(request):
    student_instance = Student.objects.get(id=request.session['student_instance_id'])
    args = {'student_instance': student_instance}
    return render(request, 'jobportal/Student/viewcvs.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def cv_upload(request):
    stud_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    if request.method == "POST":
        cv_data = StudCVForm(request.POST, request.FILES or None)
        if cv_data.is_valid():
            stud_instance.cv1 = cv_data.cleaned_data['cv1']
            stud_instance.cv2 = cv_data.cleaned_data['cv2']
            stud_instance.save()
            return redirect("viewcvs")
        else:
            args = {'cv_upload_form': cv_data}
            return render(request, 'jobportal/Student/cvupload.html', args)
    else:
        args = {'cv_upload_form': StudCVForm(initial={
            'cv1': stud_instance.cv1,
            'cv2': stud_instance.cv2
        })}
        return render(request, 'jobportal/Student/cvupload.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def del_cv(request, cvno):
    stud_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    if str(cvno) == "1":
        stud_instance.cv1.delete()
        stud_instance.save()
    if str(cvno) == "2":
        stud_instance.cv2.delete()
        stud_instance.save()
    return redirect("viewcvs")


# Loads event form via template and saves the vent data
def requestevent(request):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    if request.method == 'POST':
        event_form_data = RequestEventForm(request.POST)
        if event_form_data.is_valid():
            event_instance = Event(
                alum_owner=alum_instance,
                title=event_form_data.cleaned_data['title'],
                date1=event_form_data.cleaned_data['date1'],
                date2=event_form_data.cleaned_data['date2'],
                date3=event_form_data.cleaned_data['date3']
            )
            event_instance.save()
            return redirect('alum_home')
        else:
            args = {'event_form': event_form_data}
            return render(request, 'jobportal/Alumni/requestevent.html', args)
    else:
        args = {}
        args.update(csrf(request))
        args['event_form'] = RequestEventForm()

        return render(request, 'jobportal/Alumni/requestevent.html', args)


def eventsandstatus(request):
    alum_instance = Alumni.objects.get(id=request.session['alum_instance_id'])
    args = {'event_list': Event.objects.filter(alum_owner=alum_instance)}
    return render(request, 'jobportal/Alumni/eventsandstatus.html', args)


# ---------------------
# Experiments
# ---------------------

@login_required
def stud_pdf(request):
    response = HttpResponse(content_type="application/pdf")

    response['Content-Disposition'] = 'filename = "student_jobs.pdf"'

    byte_buffer = BytesIO()

    p = canvas.Canvas(byte_buffer)

    p.drawString(50, 50, 'Hello World')

    p.showPage()
    p.save()

    pdf = byte_buffer.getvalue()
    byte_buffer.close()
    response.write(pdf)

    return response


"""

Company view

"""


@login_required(login_url=COMPANY_LOGIN_URL)
def company_requestevent(request):
    try:
        company_instance = Company.objects.get(id=request.session['company_instance_id'])
    except:
        raise Http404("404 Error.")
    if request.method == 'POST':
        event_form_data = RequestEventForm(request.POST)

        if event_form_data.is_valid():
            event_instance = Event(
                company_owner=company_instance,
                title=event_form_data.cleaned_data['title'],
                date1=event_form_data.cleaned_data['date1'],
                date2=event_form_data.cleaned_data['date2'],
                date3=event_form_data.cleaned_data['date3']
            )
            event_instance.save()
            return redirect('companyhome')
        else:
            args = {'event_form': event_form_data}
            return render(request, 'jobportal/Company/requestevent.html', args)
    else:
        args = {}
        args.update(csrf(request))
        args['event_form'] = RequestEventForm()
        return render(request, 'jobportal/Company/requestevent.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def eventlist(request):
    event_list = Event.objects.filter(finalised=True)
    args = {'event_list': event_list}
    return render(request, 'jobportal/Student/event.html', args)
