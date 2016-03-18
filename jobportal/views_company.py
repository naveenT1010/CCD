import zipfile
import os
import StringIO

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from datetime import datetime
from datetime import timedelta
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import update_session_auth_hash
from .models import *
from .forms import *

COMPANY_LOGIN_URL = reverse_lazy('jobportal/companylogin')


# Signup
def signup(request):
    company_signup_form = CompanySignupForm(request.POST or None)
    print(company_signup_form)
    if request.method == 'POST':
        if company_signup_form.is_valid():
            company_signup_form.save()
            return redirect('signupconfirm')
        else:
            args = dict(signup_form=company_signup_form)
            return render(request, 'jobportal/Company/signup.html', args)
    else:
        args = dict(signup_form=company_signup_form)
        return render(request, 'jobportal/Company/signup.html', args)


# Signup confirmation
def signup_confirm(request):
    args = {}
    args.update(csrf(request))
    return render(request, 'jobportal/Company/signupconfirm.html', args)


def company_login(request):
    """
    Company login.
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    if request.method == 'POST':
        company_login_data = CompanyLoginForm(request.POST)
        if company_login_data.is_valid():
            username = company_login_data.cleaned_data['username']
            password = company_login_data.cleaned_data['password']
            # check authentication
            user = auth.authenticate(username=username, password=password)
            # if User exists
            if user is not None:
                # get User instance
                current_user = User.objects.get(username=username)
                # get UserProfile instance
                user_profile_instance = UserProfile.objects.get(user=current_user)
                # if UserProfile is Company
                if user_profile_instance.login_type == 'Company':
                    # login Company
                    auth.login(request, user)
                    # get Company instance
                    company_instance = Company.objects.get(user=user_profile_instance)
                    # Set session variables
                    request.session['company_instance_id'] = company_instance.id
                    request.session['user_type'] = 'Company'
                    return redirect('companyhome')
                # User exists but is not Company
                # TODO : Add redirect to correct login page
                else:
                    args = dict(login_form=company_login_data)
                    return render(request, 'jobportal/Company/login.html', args)
            # either username-password mismatch or User doesn't exist
            else:
                args = dict(login_form=company_login_data)
                return render(request, 'jobportal/Company/login.html', args)
        # invalid form submission
        else:
            args = dict(login_form=company_login_data)
            return render(request, 'jobportal/Company/login.html', args)
    else:
        args = dict(login_form=CompanyLoginForm())
        return render(request, 'jobportal/Company/login.html', args)


# Recruiters' logout
@login_required(login_url=COMPANY_LOGIN_URL)
def company_logout(request):
    auth.logout(request)
    return render(request, 'jobportal/logout.html')


# Home
@login_required(login_url=COMPANY_LOGIN_URL)
def company_home(request):
    try:
        company_instance = Company.objects.get(id=request.session['company_instance_id'])
        args = {'company_instance': company_instance}
        return render(request, 'jobportal/Company/home.html', args)
    except:
        raise Http404("Error 404")


# Change password
@login_required(login_url=COMPANY_LOGIN_URL)
def password_change_company(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("companyhome")
        else:
            args = {'form': form}
            return render(request, 'jobportal/Company/passwordchange.html', args)
    else:
        company_instance = get_object_or_404(Company, id=request.session['company_instance_id'])
        form = PasswordChangeForm(request)
        args = {'form': form, 'company_instance': company_instance}
        return render(request, 'jobportal/Company/passwordchange.html', args)


# Profile
@login_required(login_url=COMPANY_LOGIN_URL)
def company_profile(request):
    try:
        company_instance = Company.objects.get(id=request.session['company_instance_id'])
        args = {'company_instance': company_instance}
        return render(request, "jobportal/Company/profile.html", args)
    except:
        raise Http404("Error 404")


# Edit profile
@login_required(login_url=COMPANY_LOGIN_URL)
def company_edit_profile(request, companyid):
    company_instance = get_object_or_404(Company, id=companyid)
    company_profile_form = CompanyProfileEdit(request.POST or None, instance=company_instance)
    if request.POST:
        if company_profile_form.is_valid():
            company_profile_form.save()
            return redirect("companyprofile")
        else:
            args = dict(edit_profile_form=company_profile_form, company_instance_id=company_instance.id)
            return render(request, 'jobportal/Company/editprofile.html', args)
    else:
        args = dict(company_instance_id=company_instance.id, edit_profile_form=company_profile_form)
        return render(request, 'jobportal/Company/editprofile.html', args)


# View jobs/internships already posted by recruiter
@login_required(login_url=COMPANY_LOGIN_URL)
def view_jobs(request):
    company_instance = Company.objects.get(id=request.session['company_instance_id'])
    job_list = Job.objects.all().filter(company_owner=company_instance)
    args = {}
    args.update(csrf(request))
    args['job_list'] = job_list
    return render(request, 'jobportal/Company/postedjobs.html', args)


@login_required(login_url=COMPANY_LOGIN_URL)
def company_add_job(request):
    """
    Add new Job instance
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    # TODO: Look at security implication of this
    # get currently logged in Company instance
    company_instance = Company.objects.get(id=request.session['company_instance_id'])
    add_job_form = JobEditForm(request.POST or None)
    if request.method == "POST":
        # parse form data
        if add_job_form.is_valid():
            job_instance = add_job_form.save(commit=False)
            job_instance.company_owner = company_instance
            job_instance.posted_by_alumnus = False
            job_instance.posted_by_company = True
            job_instance.posted_on = datetime.now()
            job_instance.last_updated = datetime.now()
            job_instance.opening_date = datetime.now() + timedelta(days=30)
            job_instance.application_deadline = datetime.now() + timedelta(days=50)
            job_instance.save()
            print(job_instance.company_owner)
            job_prog_rel = ProgrammeJobRelation(job=job_instance)
            job_prog_rel.save()
            return redirect('companyviewjobs')
        else:
            return render(request, 'jobportal/Company/postjob.html', dict(add_job_form=add_job_form))
    else:
        return render(request, 'jobportal/Company/postjob.html', dict(add_job_form=add_job_form))


def view_job(request, jobid):
    """
    View for Company/Recruiters to view(reviw) an already posted job
    :param request: HttpRequest instance
    :param jobid: Job instance id
    :return: HttpResponse instance
    """
    job_instance = get_object_or_404(Job, id=jobid)
    rel_list = ProgrammeJobRelation.objects.filter(job=job_instance)
    args = dict(job_instance=job_instance, rel_list=rel_list)
    return render(request, 'jobportal/Company/job.html', args)


def add_progs(request, jobid):
    """
    View for Company to add programmes to an already posted job.
    :param request: HttpRequest instance
    :param jobid: Job instance id
    :return: HttpResponse instance
    """
    job_instance = get_object_or_404(Job, id=jobid)
    formset = JobProgFormSet(request.POST or None, instance=job_instance)
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('companyjob', jobid=job_instance.id)
        else:
            args = dict(formset=formset, job_instance=job_instance)
            return render(request, 'jobportal/Company/add_job_progs.html', args)
    else:
        args = dict(formset=formset, job_instance=job_instance)
        return render(request, 'jobportal/Company/add_job_progs.html', args)


# Edit an already posted job/internship
@login_required(login_url=COMPANY_LOGIN_URL)
def company_edit_job(request, jobid):
    job_instance = Job.objects.get(id=jobid)
    job_add_form = JobEditForm(request.POST or None, instance=job_instance)
    if request.method == "POST":
        if job_add_form.is_valid():
            job_instance = job_add_form.save(commit=False)
            job_instance.last_updated = datetime.now()
            job_instance.save()
            return redirect('companyviewjobs')
        else:
            args = dict(edit_job_form=job_add_form, job=job_instance)
            return render(request, 'jobportal/Company/editjob.html', args)

    else:
        args = dict(edit_job_form=job_add_form, job=job_instance)
        return render(request, 'jobportal/Company/editjob.html', args)


# Delete an existing job/internship entry
@login_required(login_url=COMPANY_LOGIN_URL)
def company_del_job(request, jobid):
    job = Job.objects.get(id=jobid)
    job.delete()
    return redirect('companyviewjobs')


# Candidates for a job; both alumns and students
@login_required(login_url=COMPANY_LOGIN_URL)
def company_candidates(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    stud_list = [e.stud for e in StudentJobRelation.objects.filter(job=job_instance)]
    # Magic
    hide_jobaction = True if job_instance.application_deadline > datetime.now().date() else False
    args = dict(jobid=job_instance.id, stud_list=stud_list, hide_jobaction=hide_jobaction)
    return render(request, 'jobportal/Company/candidates.html', args)


# Student Job Relation Views
@login_required(login_url=COMPANY_LOGIN_URL)
def job_stud_relation(request, jobid, studid):
    stud_instance = get_object_or_404(Student, id=studid)
    job_instance = get_object_or_404(Job, id=jobid)
    relation_instance = get_object_or_404(StudentJobRelation, stud=stud_instance, job=job_instance)
    args = dict(stud_instance=stud_instance, job_instance=job_instance, relation_instance=relation_instance)
    return render(request, 'jobportal/Company/jobactions.html', args)


# Student Shortlist
@login_required(login_url=COMPANY_LOGIN_URL)
def job_shortlist(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.shortlist_init = True
    relation_instance.save()
    return redirect("jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


# Student Unshortlist
@login_required(login_url=COMPANY_LOGIN_URL)
def job_unshortlist(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.shortlist_init = False
    relation_instance.save()
    return redirect("jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


# Student Place
@login_required(login_url=COMPANY_LOGIN_URL)
def job_place(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.placed_init = True
    relation_instance.save()
    return redirect("jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


# Student Unplace
@login_required(login_url=COMPANY_LOGIN_URL)
def job_unplace(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.placed_init = False
    relation_instance.save()
    return redirect("jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


@login_required(login_url=COMPANY_LOGIN_URL)
def job_drop(request, jobid):
    # TODO: Check no shortlist bug
    job_instance = get_object_or_404(Job, id=jobid)
    stud_rels = list(StudentJobRelation.objects.get(job=job_instance, dropped=False))
    approval_error = False
    for rel in stud_rels:
        if rel.shortlist_init is True and rel.shortlist_approved is not True:
            approval_error = True
            break
        if rel.placed_init is True and rel.placed_approved is not True:
            approval_error = True
            break
    if not approval_error:
        for rel in stud_rels:
            rel.round += 1
            if rel.shortlist_init is False:
                rel.dropped = True
            rel.save()
    # TODO: Message framework
    # TODO: change to render
    return redirect('companycandidates', jobid=job_instance.id)


# Alum Job Relation Views
@login_required(login_url=COMPANY_LOGIN_URL)
def job_alum_relation(request, jobid, alumid):
    alum_instance = get_object_or_404(Alumni, id=alumid)
    job_instance = get_object_or_404(Job, id=jobid)
    relation_instance = get_object_or_404(AlumJobRelation, alum=alum_instance, job=job_instance)
    args = {'alum_instance': alum_instance,
            'job_instance': job_instance,
            'relation_instance': relation_instance
            }
    return render(request, 'jobportal/Company/jobactions.html', args)


# Alum Shortlist
@login_required(login_url=COMPANY_LOGIN_URL)
def job_shortlist2(request, relationid):
    relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    relation_instance.shortlist_status = True
    relation_instance.save()
    return redirect("jobaction2", jobid=relation_instance.job.id, alumid=relation_instance.alum.id)


# Alum Unshortlist
@login_required(login_url=COMPANY_LOGIN_URL)
def job_unshortlist2(request, relationid):
    relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    relation_instance.shortlist_status = False
    relation_instance.save()
    return redirect("jobaction2", jobid=relation_instance.job.id, alumid=relation_instance.alum.id)


# Alum Place
@login_required(login_url=COMPANY_LOGIN_URL)
def job_place2(request, relationid):
    relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    relation_instance.placed_init=True
    relation_instance.save()
    return redirect("jobaction2", jobid=relation_instance.job.id, alumid=relation_instance.alum.id)


# Alum Unplace
@login_required(login_url=COMPANY_LOGIN_URL)
def job_unplace2(request, relationid):
    relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    relation_instance.placed_init = False
    relation_instance.save()
    return redirect("jobaction2", jobid=relation_instance.job.id, alumid=relation_instance.alum.id)


# Issue: Not working as intended; Most probably it's not using relative path
# SO solution isn't working
# TODO: Debug; Think of some workaround
# TODO: Download CVs as zip
@login_required(login_url=COMPANY_LOGIN_URL)
def download_cvs(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    relation_list = get_list_or_404(StudentJobRelation, job = job_instance)
    filelist = []
    for relation in relation_list:
        if bool(relation.cv1):
            filelist.append(relation.stud.cv1.url)
        if bool(relation.cv2):
            filelist.append(relation.stud.cv2.url)

    zip_subdir = "cvs_for_" + str(job_instance.description)
    zip_filename = "%s.zip" % zip_subdir

    s = StringIO.StringIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in filelist:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)

    zf.close()

    response = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return response


# Events and status
@login_required(login_url=COMPANY_LOGIN_URL)
def company_eventsandstatus(request):
    company_instance = get_object_or_404(Company, id=request.session['company_instance_id'])
    args = {'event_list': Event.objects.filter(company_owner=company_instance)}
    return render(request, 'jobportal/Company/eventsandstatus.html', args)

