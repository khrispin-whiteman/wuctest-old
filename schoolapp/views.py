import socket
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected
import arrow
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from schoolapp.models import AssessmentType, FinalResult, User, Department, School, Program, Course, StudentNumber, SystemSettings, Admission, \
    Session, SchoolClass, Student, WrittenAssessment, WucFiles, Level, Assessment, Semester, TakenCourse, PaymentType, PaymentStructure, Payment
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .forms import CreateAssessmentForm, OnlineAdmissionForm, AddStaffForm, AddSchoolForm, AddDepartmentForm, UpdateOnlineApplicationForm, \
    AddStudentForm, PaymentCollectForm, RegisterCourseForm, AddPaymentTypeForm, AddPaymentStructureForm, AdminOnlineAdmissionForm
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import random
import string
from fpdf import FPDF
import pdfkit
from django.template.loader import get_template
import os
import tempfile

# html to pdf
from io import BytesIO
from xhtml2pdf import pisa


# Create your views here.
def index(request):
    # Get list of departments
    departments = Department.objects.all()
    # Get list of schools
    schools = School.objects.all()
    # return render(request, "schoolapp/landingpages/index.html",
    return render(request, "schoolapp/landingpages/index.html",
                  {
                      'departments': departments,
                      'schools': schools,
                  })


class ChangePasswordView(APIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_forgot_password(request):
    return render(request, "schoolapp/systempages/forgot-password.html", {})

@login_required
def dashboard(request):
    global student
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # Get all students
    students = Student.objects.all()
    courses = Course.objects.all()
    programs = Program.objects.all()
    staff = User.objects.filter(is_member_of_staff=True)

    # Get list of departments
    departments = Department.objects.all()

    if request.user.is_student:
        student = Student.objects.get(user=request.user)
        student_courses = TakenCourse.objects.filter(student=student).count()
        student_registered_dashbord_count = TakenCourse.objects.filter(student=student)
        print('COURSE COUNT: ', student_courses)
        student_written_assessments = WrittenAssessment.objects.filter(student=student)
        # student_details = Admission.objects.get(user=student.user)
        # get courses for current semester for a specific programme
        courses_in_program = Course.objects.filter(semester=current_semester.semester, course_program=student.student_admission_details.program_applied_for)
    else:
        student = ''
        student_courses = ''
        student_registered_dashbord_count = ''
        student_written_assessments = ''
        student_details = ''
        courses_in_program = ''
    

    # Get list of schools
    schools = School.objects.all()
    return render(request, "schoolapp/systempages/index.html",
                  {
                      'departments': departments,
                      'schools': schools,
                      'courses': courses,
                      'programs': programs,
                      'students': students,
                      'current_semester': current_semester,
                      'student': student,
                      'student_courses': student_courses,
                      'student_registered_dashbord_count': student_registered_dashbord_count,
                      'student_written_assessments': student_written_assessments,
                      'courses_in_program': courses_in_program,
                      'staff': staff,
                    #   'student_details': student_details,
                  })


                   # Lecturer's Dashboard Start

             
def lecturer(request):
     departments = Department.objects.all()
     # Get list of schools

     return render(request, 'schoolapp/lecturers_dashboard/index.html')


def lecturers_modules(request):
    departments = Department.objects.all()
    # Get list of schools
    schools = School.objects.all()
    return render(request, 'schoolapp/lecturers_dashboard/modules.html')


def edit_modules(request):
    departments = Department.objects.all()
    # Get list of schools
    schools = School.objects.all()
    return render(request, 'schoolapp/lecturers_dashboard/edit_module.html')


def add_modules(request):
    departments = Department.objects.all()
    # Get list of schools
    schools = School.objects.all()
    return render(request, 'schoolapp/lecturers_dashboard/add_module.html')


def lecturers_students(request):
    return render(request, 'schoolapp/lecturers_dashboard/students.html')

    
def lecturers_students_results(request):
    return render(request, 'schoolapp/lecturers_dashboard/edit_students.html')


def lecturers_students_details(request):
    return render(request,
                  'schoolapp/lecturers_dashboard/student_details.html')

# End Lecture's Dashboard

def testtemplate(request):
    return render(request, 'schoolapp/landingpages/templogin.html', {})


def templogintocheckapplicationstatus(request):
    print('Method Called')
    if request.method == 'POST':
        student_no = request.POST.get('student_no')
        tmp_password = request.POST.get('tmp_password')
        print('STUDENT NO: ', student_no)
        print('PASSWORD: ', tmp_password)
        if Admission.objects.filter(student_number__full_student_no=student_no, temp_password__exact=tmp_password):
            print('FOUND')
            application_details = Admission.objects.get(student_number__full_student_no=student_no,
                                                        temp_password__exact=tmp_password)
            return render(request, 'schoolapp/landingpages/checkapplicationstatus.html',
                          {
                              'application_detail': application_details,
                              'student_no': student_no
                          })
        else:
            return render(request, 'schoolapp/landingpages/templogin.html',
                          {
                              'message': 'Student Number or Password not correct!'
                          })
    else:
        return render(request, 'schoolapp/landingpages/templogin.html', {})


def checkapplicationstatus(request, nrc_no):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    return render(request, 'schoolapp/landingpages/checkapplicationstatus.html',
                  {
                      'nrc_no': nrc_no,
                      'current_semester': current_semester
                  })


def generateStudentNumberRandomDigits():
    # get the year and month
    year_month = arrow.now().format('YYMM')

    # get the length of the last digits from the database
    ss = SystemSettings.objects.all().first()
    if ss:
        length = ss.student_no_last_digits_length
    else:
        length = 4
    random_str = ''.join(
        random.choice(string.digits) for _ in range(length)
    )

    # random_str = int(random_str) + 1
    # txt = str(random_str)
    # x = txt.zfill(length)
    x = random_str.zfill(length)

    student_number = year_month + x
    # print('STUDENT NO: ', student_number + str(type(student_number)))
    # check if number already taken
    if StudentNumber.objects.filter(full_student_no__exact=student_number):
        print('Number Already Taken!')
        generateStudentNumberRandomDigits()
    else:
        return student_number


# generate student number
# def generateStudentNumber(request):
#     student_number = arrow.now().format('YYMM')
#     num_from_db = StudentNumber.objects.all().aggregate(Max('digit'))['digit__max']
#     # print('NUM FROM DB: ', num_from_db)
#     lenth = 4
#     num_from_db = num_from_db + 1
#     txt = str(num_from_db)
#     x = txt.zfill(lenth)
#
#     student_number = student_number + x
#     # print('STUDENT NO: ', student_number + str(type(student_number)))
#     # check if number already taken
#     if StudentNumber.objects.filter(full_student_no__exact=student_number):
#         print('Number Already Taken!')
#         student_no = generateStudentNumberRandomDigits(request)
#         return student_no
#     else:
#         obj = StudentNumber()
#         return HttpResponse(student_number)


# generate temp password for application status checking
def generateTempPassword(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def online_admission(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    programs = Program.objects.all()
    if request.method == 'POST':
        application_form = OnlineAdmissionForm(request.POST, request.FILES)
        print('PROGRAM ID: ', request.POST.get('program_applied_for'))

        if application_form.is_valid():
            print('FORM IS VALID')
            # get temp password
            tmp_password = generateTempPassword(10)
            application_form.temp_password = tmp_password
            # print('PASSWORD: ', tmp_password)

            # get program using id
            program = Program.objects.get(id=request.POST.get('program_applied_for'))

            # generate student number
            student_no = generateStudentNumberRandomDigits()
            sn_obj = StudentNumber.objects.create(full_student_no=student_no)
            print('STUDENT NO: ', sn_obj.full_student_no)

            obj = application_form.save(commit=False)
            print('CREATED FORM INSTANCE:', obj)

            # get the files from POST
            files_list=[]
            
            # print('FILES LIST:', files_list)
            # obj.scanned_gce_results = request.FILES.getlist('scanned_gce_results')
            obj.program_applied_for = program
            obj.student_number = sn_obj
            obj.temp_password = tmp_password
            try:
                obj.intake = Session.objects.get(is_current_session=True)
            except Session.DoesNotExist:
                return HttpResponse('No Intake/Session defined in database')
            obj.save()

            files = request.FILES.getlist('scanned_gce_results')
            
            for f in files:
                print('FILES: ', f.name)
                # files_list.append(f)
                # obj.scanned_gce_results = f
                # obj.save(commit=False)
                newfile, created = WucFiles.objects.get_or_create(file=f)
                obj.scanned_gce_results.add(newfile)
            obj.save()

            # notify applicant via mail
            # get email content
            firstname = application_form.cleaned_data.get('first_name')
            subject = 'WUC Online Application'
            message = 'Dear, ' + application_form.cleaned_data.get(
                "first_name") + ' ' + application_form.cleaned_data.get("last_name") + '\n\n' \
                                                                                       'Your application for the program ' + str(
                application_form.cleaned_data.get('program_applied_for')) + \
                      ' has been successfully submitted, you will be notified once it has been reviewed by the school' \
                      ' administration. You can check the status of your application via this link https://wucsmstest.pythonanywhere.com/application-status/ \n' \
                      'You will be required to provide your Student Number and the temporal system generated password.\n\n' \
                      'STUDENT NO.: ' + sn_obj.full_student_no + '\n' \
                      'PASSWORD: ' + tmp_password + '\n' \
                       'LINK: https://wucsmstest.pythonanywhere.com/application-status/\n\n' \
                       'Keep the information above safe or you will be unable to see your application status.\n\n' \
                       'You can go back and make changes to your application details before close of application,\n' \
                       'For more information, contact the academic office on: 0900000000 or 0700000000'

            from_email = 'chrispinkay@gmail.com'
            try:
                send_mail(subject, message, from_email, recipient_list=[application_form.cleaned_data.get('email'), ],
                          fail_silently=False)

            except socket.gaierror:
                print('NO INTERNET ACCESS')
                return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
            except ConnectionError:
                print('CONNECTION ERROR')
                return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
            except SMTPAuthenticationError:
                return HttpResponse('Host Email Username and Password not accepted, Email Not Sent!')

            # add a success page to be rendered
            messages.success(request, 'Application Successfully Submitted!')
            context = {
                'message': messages,
                'form': application_form,
                'programs': programs,
                'current_semester': current_semester
            }
            return render(request, 'schoolapp/landingpages/application_successful.html', context)
            # return redirect('index')

        else:
            print('FORM IS NOT VALID', application_form.errors)
            messages.error(request, application_form.errors)
            context = {
                'message': application_form.errors,
                'form': application_form,
                'programs': programs,
                'current_semester': current_semester
            }
            return render(request, 'schoolapp/landingpages/online_registration.html', context)
    else:
        # Get list of departments
        departments = Department.objects.all()

        # Get list of schools
        schools = School.objects.all()

        # Get list of programs
        programs = Program.objects.all()

        application_form = OnlineAdmissionForm()
        return render(request, "schoolapp/landingpages/online_registration.html",
                      {
                          'departments': departments,
                          'schools': schools,
                          'programs': programs,
                          'form': application_form,
                          'current_semester': current_semester
                      })


def updateonlineapplication(request, student_no):
    if request.method == 'POST':
        application = Admission.objects.get(student_number__full_student_no=student_no)
        form = UpdateOnlineApplicationForm(request.POST, request.FILES, instance=application)
        print('INSIDE POST')
        print(form.errors)
        if form.is_valid():
            print('FORM IS VALID')
            form.save()

            # pre-populate the form with an existing band
            # return redirect('templogintocheckapplicationstatus')
            return render(request, 'schoolapp/landingpages/checkapplicationstatus.html',
                          {
                              'application_detail': application,
                              'student_no': student_no
                          })
        else:
            return render(request, 'schoolapp/landingpages/update_application.html',
                          {
                              'form': form,
                              'application': application,
                              'student_no': student_no
                          })

    application = Admission.objects.get(student_number__full_student_no=student_no)
    form = UpdateOnlineApplicationForm(instance=application)
    return render(request, 'schoolapp/landingpages/update_application.html',
                  {
                      'form': form,
                      'application': application,
                  })


def departments(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # Get list of departments
    departments = Department.objects.all()

    # Get list of schools
    schools = School.objects.all()
    return render(request, "schoolapp/systempages/departments.html",
                  {
                      'departments': departments,
                      'schools': schools,
                      'current_semester': current_semester
                  })


def add_department(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    if request.method == 'POST':
        add_department_form = AddDepartmentForm(request.POST, request.FILES)
        print('INSIDE POST')
        if add_department_form.is_valid():
            print('FORM VALID')
            print(add_department_form.cleaned_data['department_name'])
            print(add_department_form.cleaned_data['department_description'])
            print(add_department_form.cleaned_data['hod'])
            add_department_form.save()
            return redirect('departments')
            # departments = Department.objects.all()
            # return render(request, 'schoolapp/systempages/departments.html',
            #               {
            #                   'departments': departments,
            #               })

        else:
            add_department_form = AddDepartmentForm()
            return render(request, 'schoolapp/systempages/add-department.html',
                          {
                              'add_department_form': add_department_form,
                              'current_semester': current_semester
                          })
    add_department_form = AddDepartmentForm()
    return render(request, 'schoolapp/systempages/add-department.html',
                  {
                      'add_department_form': add_department_form,
                      'current_semester': current_semester
                  })


def school_details(request, school_id):
    # Get list of departments
    departments = Department.objects.all()

    # Get list of schools
    schools = School.objects.all()

    # Get the school
    school = School.objects.get(id=school_id)

    # get a list of programs in that selected school
    programs = Program.objects.filter(program_school_id=school_id)
    return render(request, "schoolapp/landingpages/programs_list.html",
                  {
                      'departments': departments,
                      'schools': schools,
                      'school': school,
                      'programs': programs,
                  })


def programs(request):
    # Get list of departments
    departments = Department.objects.all()

    # Get list of schools
    schools = School.objects.all()

    # Get list of programs
    programs = Program.objects.all()
    return render(request, "schoolapp/landingpages/programs_list.html",
                  {
                      'departments': departments,
                      'schools': schools,
                      'programs': programs,
                  })


# lists teachers
@login_required()
def admin_list_programs(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    programs = Program.objects.all()
    return render(request, 'schoolapp/systempages/admin_program_list.html', {
        'programs': programs,
        'current_semester': current_semester
    })


# lists teachers
@login_required()
def program_details_admin(request, program_id):
    # get_program using program_id
    program = Program.objects.get(pk=program_id)

    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')

    courses = Course.objects.filter(course_program=program, semester=current_semester.semester)
    return render(request, 'schoolapp/systempages/admin_program_details.html', {
        'program': program,
        'courses': courses,
        'current_semester': current_semester
    })



def program_details(request, program_id):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # Get list of departments
    departments = Department.objects.all()

    # Get list of schools
    schools = School.objects.all()

    # Get the program
    program = Program.objects.get(id=program_id)

    # get a list of courses in that selected program
    courses = Course.objects.filter(course_program_id=program_id)
    return render(request, "schoolapp/landingpages/courses_list.html",
                  {
                      'program': program,
                      'courses': courses,
                      'departments': departments,
                      'schools': schools,
                      'current_semester': current_semester
                  })


def course_details(request, course_id):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # Get list of departments
    departments = Department.objects.all()

    # Get list of schools
    schools = School.objects.all()

    # Get the course details
    try:
        course_details = Course.objects.get(id=course_id)
    except:
        return HttpResponse('Not Found')

    return render(request, "schoolapp/landingpages/course_details.html",
                  {
                      'course_details': course_details,
                      'departments': departments,
                      'schools': schools,
                      'current_semester': current_semester
                  })


def courses(request):
    # Get list of departments
    departments = Department.objects.all()
    # Get list of schools
    schools = School.objects.all()
    # Get list of courses
    courses = Course.objects.all()
    return render(request, "schoolapp/landingpages/courses_list.html",
                  {
                      'departments': departments,
                      'schools': schools,
                      'courses': courses,
                  })


@login_required()
def admin_admissions_list(request):
    global admissions
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    users = User.objects.all()

    if request.user.user_group == 'Admissions Office':
        print('Admissions Office')
        admissions = Admission.objects.filter(is_active=True, application_stage='Admissions Office')

    elif request.user.user_group == 'Accounts Office':
        print('Accounts Office')
        admissions = Admission.objects.filter(is_active=True, application_stage='Accounts Office')

    elif request.user.user_group == 'Dean Of Students Affairs Office':
        print('Dean Of Students Affairs Office')
        admissions = Admission.objects.filter(is_active=True, application_stage='Dean Of Students Affairs Office')

    elif request.user.user_group == 'ICT Office':
        print('ICT Office')
        admissions = Admission.objects.filter(is_active=True, application_stage='ICT Office')

    elif request.user.user_group == 'Program Coordinator or Principal Lecturer Office':
        print('Program Coordinator or Principal Lecturer Office')
        admissions = Admission.objects.filter(is_active=True, application_stage='Program Coordinator or Principal Lecturer Office')

    elif request.user.user_group == 'Registrar Office':
        print('Registrar Office')
        admissions = Admission.objects.filter(is_active=True, application_stage='Registrar Office')

    elif request.user.is_staff or request.user.is_superuser:
        print('Super User')
        admissions = Admission.objects.filter(is_active=True)

    return render(request, 'schoolapp/systempages/admin_admissions_list.html',
                  {
                      'admissions': admissions,
                      'current_semester': current_semester
                  })
    # return HttpResponse('Yoh!')


@login_required()
def admin_admissions_detail(request, admission_id):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    admission_details = Admission.objects.get(id=admission_id)
    print('INSIDE ADMIN ADMISSIONS DETAIL')
    if request.method == 'POST':
        print('INSIDE POST')
        online_admission_form = OnlineAdmissionForm(request.POST, request.FILES)
        if online_admission_form.is_valid():
            print('FORM VALID')
            online_admission_form.save()

            return HttpResponse('Approved!')
        else:
            return render(request, 'schoolapp/systempages/admin_admissions_details.html',
                          {'online_admission_form': online_admission_form})
    online_admission_form = OnlineAdmissionForm()
    return render(request, 'schoolapp/systempages/admin_admissions_details.html',
                  {
                      'admission_details': admission_details,
                      'online_admission_form': online_admission_form,
                      'current_semester': current_semester
                  })


@login_required()
def admin_approve_application(request, admission_id):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    form = OnlineAdmissionForm()
    # get the admission with given id
    admission_details = Admission.objects.get(id=admission_id)
    if request.user.user_group == 'Admissions Office':
        if request.method == 'POST':
            # print('INSIDE POST')
            # if the status picked is 'Verified'
            if request.POST['application_status'] == 'Verified':
                admission_details.application_status = request.POST['application_status']
                admission_details.admissions_office_comment = request.POST['admissions_office_comment']
                admission_details.application_stage = 'Accounts Office'
                admission_details.admissions_office = True
                admission_details.admissions_office_user = request.user
                print('ADMINISTER USER: ', request.user)
                admission_details.save()

    if request.user.user_group == 'Accounts Office':
        if request.method == 'POST':
            # print('INSIDE POST')
            # if the status picked by accounts is 'Verified'
            if request.POST['application_status'] == 'Verified':
                # admission_details.balance_due = request.POST['balance_due']
                admission_details.accounts_office_comment = request.POST['accounts_office_comment']
                admission_details.application_status = request.POST['application_status']
                admission_details.application_stage = 'Registrar Office'
                admission_details.accounts_office = True
                admission_details.accounts_office_user = request.user
                print('ACCOUNTS USER: ', request.user)
                admission_details.save()

            if request.POST['application_status'] == 'Pending':
                admission_details.balance_due = request.POST['balance_due']
                admission_details.accounts_office_comment = request.POST['accounts_office_comment']
                admission_details.application_status = request.POST['application_status']
                admission_details.application_stage = 'Accounts Office'
                admission_details.accounts_office = False
                admission_details.accounts_office_user = request.user
                print('ACCOUNTS USER: ', request.user)
                admission_details.save()

    # if request.user.user_group == 'Dean Of Students Affairs Office':
    #     admission_details.application_stage = 'ICT Office'
    #     admission_details.dean_of_students_affairs_office = True
    #     admission_details.dean_of_students_affairs_office_user = request.user
    #     print('ICT USER: ', request.user)
    #     admission_details.save()

    # if request.user.user_group == 'ICT Office':
    #     if request.method == 'POST':
    #         # print('INSIDE POST')
    #         admission_details.ict_office_comment = request.POST['ict_office_comment']
    #         admission_details.save()
    #
    #     admission_details.application_stage = 'Program Coordinator or Principal Lecturer Office'
    #     admission_details.ict_office = True
    #     admission_details.ict_office_user = request.user
    #     admission_details.save()

    # if request.user.user_group == 'Program Coordinator or Principal Lecturer Office':
    #     if request.method == 'POST':
    #         # print('INSIDE POST')
    #         admission_details.program_coordinator_or_principal_lecturer_office_comment = request.POST['program_coordinator_or_principal_lecturer_office_comment']
    #         admission_details.save()
    #
    #     admission_details.application_stage = 'Registrar Office'
    #     admission_details.program_coordinator_or_principal_lecturer_office = True
    #     admission_details.program_coordinator_or_principal_lecturer_office_user = request.user
    #     admission_details.save()

    if request.user.user_group == 'Registrar Office':
        if request.POST['application_status'] == 'Rejected':
            print('INSIDE POST')
            admission_details.registrar_office_comment = request.POST['registrar_office_comment']
            admission_details.application_status = request.POST['application_status']
            admission_details.application_stage = 'Registrar Office'
            admission_details.accounts_office = False
            admission_details.accounts_office_user = request.user
            print('REGISTRAR USER: ', request.user)
            admission_details.save()

            # notify applicant via mail
            subject = 'Admission Confirmation'

            message = 'Dear Mr./Mrs./Ms. ' + str(admission_details.last_name) + '\n' \
                                                                                'Thank you for your application for admission to [name of college]. \n' \
                                                                                'After reviewing your application and supporting documentation, we regret that we must decline your application at this time. \n' \
                                                                                'The applicant pool for this academic year has exceeded our available openings for admission. \n' \
                                                                                'The decision has been difficult, and although you show outstanding potential as a student, the competition is intense. \n' \
                                                                                'You are welcome to apply after you complete your GRE testing, which was not included in this year’s application. \n' \
                                                                                'It is a requirement for admission at Woodlands University College.\n\n' \
                                                                                'We appreciate your consideration of Woodlands University College, along with the time and effort you put into your application. \n' \
                                                                                'We wish you the best of success in your academic endeavors. We encourage you to continue pursuit of your academic goals.\n\n' \
 \
            'Sincerely,\n\n' \
 \
            '' + request.user.get_full_name()

        from_email = 'chrispinkay@gmail.com'

        try:
            if request.POST['application_status'] == 'Rejected':
                send_mail(subject, message, from_email, recipient_list=[admission_details.email, ],
                          fail_silently=False)

        except socket.gaierror:
            print('NO INTERNET ACCESS')
            return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
        except ConnectionError:
            print('CONNECTION ERROR')
            return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
        except IntegrityError:
            return redirect('list_teacher')

    if request.POST['application_status'] == 'Approved':
        print('INSIDE POST')
        admission_details.registrar_office_comment = request.POST['registrar_office_comment']
        admission_details.application_status = request.POST['application_status']
        admission_details.application_stage = 'Registrar Office'
        admission_details.application_stage = 'Approved'
        admission_details.registrar_office = True
        admission_details.registrar_office_user = request.user
        admission_details.save()

        # notify applicant via mail
        subject = 'Admission Confirmation'

        message = 'Dear ' + str(admission_details.first_name) + ', \n\n' \
                                                                'This is ' + request.user.get_full_name() + ' from the registrars office of Woodlands University College, ' \
                                                                                                            'I want to congratulate you that you have been qualified for Admission ' + str(
            admission_details.program_applied_for) + ', and you ' \
                                                     'are requested to contact the administration department for further process. Your first semester classes ' \
                                                     'will start on (Date). \n\n' \
                                                     'Kindly meet the concerned person for fee structure, and course details, etc. ' \
                                                     'You are among those lucky people who have got the chance to study in such a renowned university. ' \
                                                     'Looking forward to your action against this letter and hope that you will contact us as early as possible.\n\n ' \
                                                     'You can go back and make changes before close of application.\n\n' \
                                                     'Yours sincerely, \n\n' \
                                                     'Name… \n' \
                                                     'Registrars Office \n\n' \
                                                     'Woodlands University College \n\n' \
                                                     '09777777777 or 09888888888'

        from_email = 'chrispinkay@gmail.com'

        try:
            if request.POST['application_status'] == 'Approved':
                send_mail(subject, message, from_email, recipient_list=[admission_details.email, ],
                          fail_silently=False)

        except socket.gaierror:
            print('NO INTERNET ACCESS')
            return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
        except ConnectionError:
            print('CONNECTION ERROR')
            return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
        except IntegrityError:
            return redirect('list_teacher')

    # get all admissions
    global admissions
    if request.user.user_group == 'Admissions Office':
        admissions = Admission.objects.filter(application_stage='Admissions Office')
    elif request.user.user_group == 'Accounts Office':
        admissions = Admission.objects.filter(application_stage='Accounts Office')
    # elif request.user.user_group == 'Dean Of Students Affairs Office':
    #     admissions = Admission.objects.filter(application_stage='Dean Of Students Affairs Office')
    elif request.user.user_group == 'ICT Office':
        admissions = Admission.objects.filter(application_stage='ICT Office')
    elif request.user.user_group == 'Program Coordinator or Principal Lecturer Office':
        admissions = Admission.objects.filter(application_stage='Program Coordinator or Principal Lecturer Office')
    elif request.user.user_group == 'Registrar Office':
        admissions = Admission.objects.filter(application_stage='Registrar Office')
    print('STATUS: ', status)
    message = 'Application Successfully Verified!'
    if request.user.user_group == 'Registrar Office':
        message = 'Application Successfully Approved!'
    return render(request, 'schoolapp/systempages/admin_admissions_list.html',
                  {
                      'success_message': message,
                      'admissions': admissions,
                      'current_semester': current_semester
                  })


# lists teachers
@login_required()
def list_staff(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    staff = User.objects.filter(is_active=True, is_staff=True, is_member_of_staff=True)
    return render(request, 'schoolapp/systempages/staff.html', {
        'staff': staff,
        'current_semester': current_semester
    })


# add teacher
@login_required()
def add_staff(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    if request.method == 'POST':
        add_staff_form = AddStaffForm(request.POST, request.FILES)
        print('INSIDE POST')

        if add_staff_form.is_valid():
            print('FORM VALID')
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(5))

            form = add_staff_form.save(commit=False)
            print('USERNAME: ', add_staff_form.cleaned_data.get('first_name'))
            f_name = add_staff_form.cleaned_data.get('first_name')
            email = add_staff_form.cleaned_data.get('email')
            print('EMAIL: ', email)
            # form.username = request.POST.get('first_name')
            # form.username = f_name.lower()
            form.username = email.lower()
            form.is_member_of_staff = True
            form.is_staff = True

            form.set_password(result_str)
            print('FORM VALID', result_str)
            try:
                form.save()
            except IntegrityError:
                return redirect('list_staff')

            # notify agent via mail
            subject = 'User Account Creation'
            message = 'Dear, ' + str(f_name) + '\n\n' \
                                               'Your account on Woodlands University College web portal was successfully created.\n\n' \
                                               'Your Login credentials are below:\n\n' \
                                               'USERNAME: ' + str(email.lower()) + '\n' \
                                                                            'PASSWORD: ' + str(result_str) + '\n\n' \
                                                                                                             'Log into your account by Visiting the link below:\n\n' \
                      + request.get_host()

            from_email = 'chrispinkay@gmail.com'

            try:
                send_mail(subject, message, from_email, recipient_list=[add_staff_form.cleaned_data.get('email'), ],
                          fail_silently=False)

            except socket.gaierror:
                print('NO INTERNET ACCESS')
                return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
            except ConnectionError:
                print('CONNECTION ERROR')
                return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
            except SMTPServerDisconnected:
                print('CONNECTION ERROR')
                return HttpResponse('Connection unexpectedly closed. Email not sent')
            except IntegrityError:
                return redirect('list_staff')

            staff = User.objects.filter(is_member_of_staff=True)
            return render(request, 'schoolapp/systempages/staff.html', {
                'add_staff_form': add_staff_form,
                'success_message': 'Staff Added Successfully',
                'staff': staff,
                'current_semester': current_semester
            })

    add_staff_form = AddStaffForm()
    return render(request, 'schoolapp/systempages/add-staff.html', {
        'add_staff_form': add_staff_form,
        'error_message': 'Staff Not Added',
        'current_semester': current_semester
    })


# lists teachers
@login_required()
def list_students(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    students = Student.objects.all()
    return render(request, 'schoolapp/systempages/students.html', {
        'students': students,
        'current_semester': current_semester
    })


@login_required()
def search_applicant_by_student_no(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    if request.method == 'POST':
        try:
            application_id = Admission.objects.get(student_number__full_student_no=request.POST.get('student_number'))
            # redirect to the add student form
            if application_id:
                print('Student Found: %s' %application_id)
            return redirect('add_student', application_id=application_id.id)
        except Admission.DoesNotExist:
            return render(request, 'schoolapp/systempages/search_applicant_by_student_no.html',
                          {
                              'error_message': 'Student number not found',
                              'current_semester': current_semester
                          })
    else:
        return render(request, 'schoolapp/systempages/search_applicant_by_student_no.html')


# add student
@login_required()
def add_student(request, application_id):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # get application
    application_details = Admission.objects.get(pk=application_id)
    # student_obj = Student()
    add_student_form = AddStudentForm()
    print('APPLICATION DETAILS: ', application_details)

    # get all programs
    programs_list = Program.objects.all()

    # generate password
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))

    if request.method == 'POST':
        # add_student_form = AddStudentForm(request.POST, request.FILES)
        print('INSIDE POST! ', application_details.student_number)
        
        # check if user already exists
        try:
            user_object = User.objects.get(username=request.POST.get('first_name'))
            print('USER EXISTS:', user_object)
        except User.DoesNotExist:
            print('USER DOES NOT EXISTS:')
            # create or get a new user instance
            user_object = User.objects.create_user(is_student=True, username=str(application_details.student_number), first_name=request.POST.get('first_name'), phone=application_details.phone_number, last_name=request.POST.get('last_name'), email=request.POST.get('email'))
            user_object.set_password(result_str)
            user_object.save()

        # get level object
        level_obj = Level.objects.get(id=request.POST.get('level'))
        print('USER ALREADY EXISTS!')

        
        # create student number
        student_number_obj = StudentNumber.objects.create(full_student_no=str(application_details.student_number))
        student_number_obj.save()

    
        # create a new Student instance
        try:
            student_obj = Student.objects.create(user=user_object, student_admission_details=application_details, level=level_obj)
            student_obj.save()

            application_details.is_active = False
            application_details.save()
        except IntegrityError:
            # except IntegrityError:
            print('INTEGRITY ERROR: ', IntegrityError)
            students = Student.objects.all()
            return render(request, 'schoolapp/systempages/add-student.html', {
                'application_details': application_details,
                'programs_list': programs_list,
                'add_student_form': add_student_form,
                'students': students,
                'error_message': 'Provided student number: '+student_number_obj.full_student_no+' already taken',
                'current_semester': current_semester
            })


        # except User.DoesNotExist:
        #     print('USER DOES NOT EXIST!')
            
            # create or get a new user instance
            # user_object = User.objects.create_user(username=request.POST.get('first_name'), first_name=request.POST.get('first_name'), password=request.POST.get('first_name'), last_name=request.POST.get('last_name'), email=request.POST.get('email'))
            # user_object.user.set_password(result_str)
            # user_object.save()

            # create a student details instance
            # student_obj.create(user=user_object, student_admission_details=application_details, level=request.POST.get('level'))
            # student_obj.save()

            # if user_object:
            #     print('USER CREATED!')
            #     user_object.save()
        
                # create student admission details
                # add_student_form.student_admission_details = application_details
                # add_student_form.save()



        # if add_student_form.is_valid():
        # print('FORM VALID!')

        # get form instance
        # form = add_student_form.save(commit=False)

        # generate password
        # letters = string.ascii_lowercase
        # result_str = ''.join(random.choice(letters) for i in range(5))
        # form.user.set_password(result_str)
        # form.user = user_object

        # generate student number
        # student_no = generateStudentNumberRandomDigits()
        # f_name = add_student_form.cleaned_data.get('first_name')
        # program = add_student_form.cleaned_data.get('program')
        # student_number = request.POST.get('student_number')
        # student_number_obj = StudentNumber.objects.create(full_student_no=student_number)
        # print('STUDENT NO: ', student_number_obj.full_student_no)
        # print('USERNAME: ', student_number_obj.full_student_no)

        # set the username to be student number
        # form.username = student_number_obj
        # form.is_student = True

        # try:
        #     form.save()
        #     user = User.objects.get(username=student_number_obj.full_student_no)
        #     print('USER: ', user)
        #     student = Student.objects.create(user=user, student_number=student_number_obj,
        #                                         level=add_student_form.cleaned_data.get('level'),
        #                                         program=add_student_form.cleaned_data.get('program'))

        #     student.save()


        # notify agent via mail
        subject = 'Student Account Creation'
        message = 'Dear, ' + str(application_details.first_name) + '\n\n' \
                    'Your student account on Woodlands University College web portal for the program '+ str(application_details.program_applied_for) +' was successfully created.\n\n' \
                    'Your Login credentials are below:\n\n' \
                    'USERNAME: ' + str(student_number_obj.full_student_no) + '\n' \
                    'PASSWORD: ' + str(result_str) + '\n' \
                    'Log into your account by Visiting the link below:\n\n' \
                    + request.get_host()

        from_email = 'chrispinkay@gmail.com'

        try:
            send_mail(subject, message, from_email, recipient_list=[application_details.email, ],
                        fail_silently=False)

        except socket.gaierror:
            print('NO INTERNET ACCESS')
            return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
        except ConnectionError:
            print('CONNECTION ERROR')
            return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
        except IntegrityError:
            return redirect('list_students')

        students = Student.objects.all()
        return render(request, 'schoolapp/systempages/students.html', {
            'add_student_form': add_student_form,
            'success_message': 'Student Added Successfully',
            'students': students,
            'current_semester': current_semester
        })
    else:
        add_student_form = AddStudentForm()
        print('ERRORS: ', add_student_form.errors)
        students = Student.objects.all()
        return render(request, 'schoolapp/systempages/add-student.html', {
            'add_student_form': add_student_form,
            'application_details': application_details,
            'programs_list': programs_list,
            'students': students,
            'current_semester': current_semester
            # 'error_message': 'Student Not Added!',
        })
    # add_student_form = AddStudentForm()
    # return render(request, 'schoolapp/systempages/add-student.html', {
    #     'add_student_form': add_student_form,
    #     'application_details': application_details,
    #     'programs_list': programs_list
    # })


# lists teachers
@login_required()
def list_schools(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    schools = School.objects.all()
    return render(request, 'schoolapp/systempages/schools.html', {
        'schools': schools,
        'current_semester': current_semester
    })


# add teacher
@login_required()
def add_school(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    if request.method == 'POST':
        add_school_form = AddSchoolForm(request.POST, request.FILES)
        print('INSIDE POST')

        if add_school_form.is_valid():
            print('FORM VALID')
            add_school_form.save()
            print('SCHOOL NAME: ', add_school_form.cleaned_data.get('school_name'))

            schools = School.objects.all()
            return render(request, 'schoolapp/systempages/schools.html', {
                'add_school_form': add_school_form,
                'success_message': 'School Added Successfully',
                'schools': schools,
                'current_semester': current_semester
            })
        else:
            add_school_form = AddSchoolForm()
            return render(request, 'schoolapp/systempages/add-school.html', {
                'add_school_form': add_school_form,
                'error_message': 'School Not Added',
                'current_semester': current_semester
            })

    add_school_form = AddSchoolForm()
    return render(request, 'schoolapp/systempages/add-school.html', {
        'add_school_form': add_school_form,
        'error_message': 'School Not Added',
        'current_semester': current_semester
    })


# class StudentAddView(CreateView):
#     model = User
#     form_class = StudentAddForm
#     template_name = 'schoolapp/systempages/add-student.html'
#     classlist = SchoolClass.objects.all()
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'student'
#         # kwargs['classlist'] = course_list
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         user = form.save()
#         return redirect('list_students')


def application_report(request, id):
    application_details = Admission.objects.get(id=id)
    sales = [
        {"item": "Keyboard", "amount": "$120,00"},
        {"item": "Mouse", "amount": "$10,00"},
        {"item": "House", "amount": "$1 000 000,00"},
    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 5, 'WOODLANDS UNIVERSITY COLLEGE', 0, 1)
    pdf.set_font('Arial', '', 13)
    pdf.cell(40, 5, 'Ibex Hill 2457 Main Street', 0, 1)
    pdf.set_font('Arial', '', 13)
    pdf.cell(40, 5, 'Lusaka', 0, 1)
    pdf.cell(40, 5, 'E-mail: woodlandsuniversity@wuc.uni', 0, 1)
    pdf.cell(40, 12, 'CALL: 0966186239', 0, 1)
    pdf.set_font('Times', 'B', 15)
    pdf.cell(40, 5, 'Personal Particulars', 0, 1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Full Name'.ljust(30)} {'Student Number'.ljust(20)}", 0, 1)
    pdf.cell(200, 8,
             f"{application_details.first_name + ' ' + application_details.other_names + ' ' + application_details.last_name + ' '.ljust(30)} {'Student Number'.ljust(20)}",
             0, 1)
    # pdf.cell(200, 8, f"{application_details.first_name.ljust(30)} {'Student Number'.ljust(20)}", 0, 1)
    # pdf.line(10, 30, 150, 30)
    # pdf.line(10, 38, 150, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    pdf.output('Wuc Application Form.pdf', 'F')
    return FileResponse(open('Wuc Application Form.pdf', 'rb'), as_attachment=True, content_type='application/pdf')


def generate_pdf_for_student_application(request, id):
    # Get data from the model
    application_details = Admission.objects.get(pk=id)

    data = {'application_details': application_details}
    
    # Render the HTML template with the data
    template = get_template('schoolapp/reports/student_application_report.html')
    html_string = template.render(data)

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'enable-local-file-access': '',
    }

    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_string(html_string, False, options=options)

    # write PDF content to file
    with open('tmp_student_application_report.pdf', 'wb') as f:
        f.write(pdf)

    # create response indicating success
    pdfresponse = HttpResponse(pdf, content_type='application/pdf')
    pdfresponse['Content-Disposition'] = 'attachment; filename="tmp_student_application_report.pdf"'
    return pdfresponse


@login_required
def profile(request):
    """ Show profile of any user that fire out the request """
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    if request.user.user_group == 'Lecturer':
        print("IF LECTURER::")
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).filter(
            semester=current_semester)
        return render(request, 'schoolapp/profile.html', {"courses": courses, })
    
    elif request.user.user_group == 'Examinations Office':
        assessments = Assessment.objects.filter(created_by=request.user)
        return render(request, 'schoolapp/profile.html', {"assessments": assessments, })
    
    elif request.user.is_student:
        print("IF STUDENT::")
        student_details = Student.objects.get(user__pk=request.user.id)
        level = Student.objects.get(user__pk=request.user.id)
        courses = TakenCourse.objects.filter(student__user__id=request.user.id, course__level=level.level)

        context = {
            'courses': courses,
            'student_details': student_details,
            'current_semester': current_semester,
            'level': level
        }
        return render(request, 'schoolapp/profile.html', context)
    elif request.user.is_superuser:
        print("IF SUPERUSER::")
        # level = Student.objects.get(user__pk=request.user.id)
        # courses = TakenCourse.objects.filter(student__user__id=request.user.id, course__level=level.level)
        #
        # context = {
        #     'courses': courses,
        #     'level': level,
        # }
        return render(request, 'schoolapp/profile.html', {'current_semester': current_semester})
    # elif request.user.is_parent:
    #     print("IF parent::")
    #     parent = Parent.objects.get(user__pk=request.user.id)
    #     students = Children.objects.filter(parent__user__pk=request.user.id)
    #     # courses = TakenCourse.objects.filter(student__user__id=parent.student.id, )
    #
    #     context = {
    #         # 'courses': courses,
    #         'students': students,
    #         'parent': parent,
    #     }
    #     return render(request, 'schoolapp/profile.html', context)
    # elif request.user.is_librarian:
    #     print("IF LIBRARIAN::")
    #     books = Book.objects.all()
    #     return render(request, 'account/profile.html',
    #                   {
    #                       "books": books,
    #                   })
    else:
        staff = User.objects.filter(is_member_of_staff=True)
        return render(request, 'schoolapp/profile.html', {"staff": staff, 'current_semester': current_semester})

@login_required()
def payment_types_list(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # Get list of payment types
    paymenttypes = PaymentType.objects.all()

    return render(request, "schoolapp/systempages/paymenttypes.html",
                  {
                      'paymenttypes': paymenttypes,
                      'current_semester': current_semester
                  })


@login_required()
def add_payment_type(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    if request.method == 'POST':
        add_payment_type_form = AddPaymentTypeForm(request.POST, request.FILES)
        print('INSIDE POST')
        if add_payment_type_form.is_valid():
            print('FORM VALID')
            print(add_payment_type_form.cleaned_data['payment_type_name'])

            add_payment_type_form.save()
            # return redirect('payment_types_list')
            paymenttypes = PaymentType.objects.all()
            return render(request, 'schoolapp/systempages/paymenttypes.html',
                          {
                              'paymenttypes': paymenttypes,
                              'success_message': 'Payment Type Added',
                              'current_semester': current_semester
                          })

        else:
            add_payment_type_form = AddPaymentTypeForm()
            return render(request, 'schoolapp/systempages/add-payment-type.html',
                          {
                              'add_payment_type_form': add_payment_type_form,
                              'error_message': 'Payment Type Not Added',
                              'current_semester': current_semester
                          })
    add_payment_type_form = AddPaymentTypeForm()
    return render(request, 'schoolapp/systempages/add-payment-type.html',
                  {
                      'add_payment_type_form': add_payment_type_form,
                      'error_message': 'Payment Type Not Added',
                      'current_semester': current_semester
                  })


@login_required()
def payment_structures_list(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # Get list of payment structures
    paymentstructures = PaymentStructure.objects.all()

    return render(request, "schoolapp/systempages/paymentstructures.html",
                  {
                      'paymentstructures': paymentstructures,
                      'current_semester': current_semester
                  })


@login_required()
def add_payment_structure(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    if request.method == 'POST':
        add_payment_structure_form = AddPaymentStructureForm(request.POST, request.FILES)
        print('INSIDE POST')
        if add_payment_structure_form.is_valid():
            print('FORM VALID')
            # print(add_payment_structure_form.cleaned_data['payment_type_name'])

            add_payment_structure_form.save()
            # return redirect('payment_types_list')
            paymentstructures = PaymentStructure.objects.all()
            return render(request, 'schoolapp/systempages/paymentstructures.html',
                          {
                              'paymentstructures': paymentstructures,
                              'success_message': 'Payment Structure Added',
                              'current_semester': current_semester
                          })

        else:
            add_payment_structure_form = AddPaymentStructureForm()
            return render(request, 'schoolapp/systempages/add-payment-structure.html',
                          {
                              'add_payment_structure_form': add_payment_structure_form,
                              'error_message': 'Payment Structure Not Added',
                              'current_semester': current_semester
                          })
    add_payment_structure_form = AddPaymentStructureForm()
    return render(request, 'schoolapp/systempages/add-payment-structure.html',
                  {
                      'add_payment_structure_form': add_payment_structure_form,
                      'error_message': 'Payment Structure Not Added',
                      'current_semester': current_semester
                  })


@login_required()
def payment_collections_list(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # Get list of payment
    payments = Payment.objects.all()

    return render(request, "schoolapp/systempages/paymentscollection.html",
                  {
                      'payments': payments,
                      'current_semester': current_semester
                  })


@login_required()
def payment_collect(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    if request.method == 'POST':
        add_payment_form = PaymentCollectForm(request.POST, request.FILES)
        print('INSIDE POST')

        if add_payment_form.is_valid():
            print('FORM VALID')

            add_payment_form.save()
            # print('SCHOOL NAME: ', payment_collect_form.cleaned_data.get('school_name'))

            payments = Payment.objects.all()
            return render(request, 'schoolapp/systempages/paymentscollection.html', {
                'add_payment_form': add_payment_form,
                'success_message': 'Payment Added Successfully',
                'payments': payments,
                'current_semester': current_semester
            })
        else:
            add_payment_form = PaymentCollectForm()
            return render(request, 'schoolapp/systempages/add-payment.html', {
                'add_payment_form': add_payment_form,
                'error_message': 'Payment Not Added',
                'current_semester': current_semester
            })

    add_payment_form = PaymentCollectForm()
    return render(request, 'schoolapp/systempages/add-payment.html', {
        'add_payment_form': add_payment_form,
        'error_message': 'Payment Not Added',
        'current_semester': current_semester
    })


@login_required()
def admin_online_student_registration(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    programs = Program.objects.all()
    if request.method == 'POST':
        application_form = AdminOnlineAdmissionForm(request.POST, request.FILES)
        print('PROGRAM: ', request.POST.get('program_applied_for'))

        if application_form.is_valid():
            print('FORM IS VALID')
            # get temp password
            tmp_password = generateTempPassword(10)
            application_form.temp_password = tmp_password
            # print('PASSWORD: ', tmp_password)

            # get program using id
            program = Program.objects.get(id=request.POST.get('program_applied_for'))

            # generate student number
            student_no = generateStudentNumberRandomDigits()
            sn_obj = StudentNumber.objects.create(full_student_no=student_no)
            print('STUDENT NO: ', sn_obj.full_student_no)

            obj = application_form.save(commit=False)

            
            files = request.FILES.getlist('scanned_gce_results')
            print('FILES LIST:', files)
            for f in files:
                print('FILES: ', f)
                fileObject, created = WucFiles.objects.get_or_create(file=f)
                
            # obj.scanned_gce_results = fileObject
            obj.program_applied_for = program
            obj.student_number = sn_obj
            obj.temp_password = tmp_password
            obj.intake = Session.objects.get(is_current_session=True)
            obj.save()

            # notify applicant via mail
            # get email content
            firstname = application_form.cleaned_data.get('first_name')
            subject = 'WUC Online Application'
            message = 'Dear, ' + application_form.cleaned_data.get(
                "first_name") + ' ' + application_form.cleaned_data.get("last_name") + '\n\n' \
                'Your application for the program ' + str(
                application_form.cleaned_data.get('program_applied_for')) + \
                      ' has been successfully submitted, you will be notified once it has been reviewed by the school' \
                      ' administration. You can check the status of your application via this link https://wucsmstest.pythonanywhere.com/application-status/ \n' \
                      'You will be required to provide your Student Number and the temporal system generated password.\n\n' \
                      'STUDENT NO.: ' + sn_obj.full_student_no + '\n' \
                      'PASSWORD: ' + tmp_password + '\n' \
                       'LINK: https://wucsmstest.pythonanywhere.com/application-status/\n\n' \
                       'Keep the information above safe or you will be unable to see your application status.\n\n' \
                       'You can go back and make changes to your application details before close of application,\n' \
                       'For more information, contact the academic office on: 0900000000 or 0700000000'

            from_email = 'chrispinkay@gmail.com'
            try:
                send_mail(subject, message, from_email, recipient_list=[application_form.cleaned_data.get('email'), ],
                          fail_silently=False)

            except socket.gaierror:
                print('NO INTERNET ACCESS')
                return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
            except ConnectionError:
                print('CONNECTION ERROR')
                return HttpResponse('Check Your Internet Connection And Try Again. Email not sent')
            except SMTPAuthenticationError:
                return HttpResponse('Host Email Username and Password not accepted, Email Not Sent!')
            except SMTPServerDisconnected:
                return HttpResponse('Connection unexpectedly closed!')

            # add a success page to be rendered
            messages.success(request, 'Application Successfully Submitted!')
            context = {
                'message': messages,
                'form': application_form,
                'programs': programs,
                'current_semester': current_semester
            }
            return render(request, 'schoolapp/systempages/admin_student_registration_successful.html', context)
            # return redirect('index')

        else:
            print('FORM IS NOT VALID', application_form.errors)
            messages.error(request, application_form.errors)
            context = {
                'message': application_form.errors,
                'form': application_form,
                'programs': programs,
                'current_semester': current_semester
            }
            return render(request, 'schoolapp/systempages/admin_online_student_registration_form.html', context)
    else:
        # Get list of departments
        departments = Department.objects.all()

        # Get list of schools
        schools = School.objects.all()

        # Get list of programs
        programs = Program.objects.all()

        application_form = OnlineAdmissionForm()
        return render(request, "schoolapp/systempages/admin_online_student_registration_form.html",
                      {
                          'departments': departments,
                          'schools': schools,
                          'programs': programs,
                          'form': application_form,
                          'current_semester': current_semester
                      })


@login_required
def add_score(request):
    """
    Shows a page where an exam officer will select a course for score entry.
    in a specific semester and session

    """
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # get current semester
    current_semester = Semester.objects.get(is_current_semester=True)
    courses = Course.objects.filter(semester=current_semester.semester)
    assessments = Assessment.objects.all()
    context = {
        "courses": courses,
        "current_semester": current_semester,
        "assessments": assessments,
    }
    return render(request, 'schoolapp/systempages/add_score.html', context)


@login_required
def add_score_for(request, assessment_id, course_id):
    """
    Shows a page where an examination officer will add score for students that are taking courses
    in a specific semester and session
    """
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    current_semester = Semester.objects.get(is_current_semester=True)
    courses = Course.objects.filter(semester=current_semester.semester)
    # get the Course instance
    course_obj = Course.objects.get(pk=course_id)
    assessments = Assessment.objects.all()
    assessment = Assessment.objects.get(pk=assessment_id)
    written_assessments = WrittenAssessment.objects.all()
    print("CURRENT SEMESTER: ", current_semester)
    if request.method == 'GET':
        # course = Course.objects.get(pk=id)
        course = assessment.course
        print('COURSE: ', course.course_name)
        print('ASSESSMENT: ', assessment)
        students = TakenCourse.objects.filter(course=course).filter(semester=current_semester)
        for s in students:
            print('STUDENTS: ID = ', str(s.student.id) + ', NAME = ', s.student.student_admission_details.first_name)
        
        context = {
            "current_semester": current_semester,
            "courses": courses,
            "course": course,
            "students": students,
            "assessments": assessments,
            "assessment": assessment,
            "written_assessments": written_assessments,
            'current_semester': current_semester
        }
        return render(request, 'schoolapp/systempages/add-score-for.html', context)

    if request.method == 'POST':
        # Whats neeedd: Selected Course ID, Student IDs under the Course and the Score of specific Students 
        # STEPS
        # - Get the selected course ID from POST request
        # - Get the specific Course object using the acquire course ID
        # - Get IDs of the students under the selected course from POST request
        # - Get the specific Student object using the acquire student ID during each iteration
        # - Get the score on each iteration from POST request
        # - Create an AssessmentScore instance with the collected score to be passed to the Assessment model
        # - Get an Assessment using the id
        # - Update the Assessment instance with the the new assessmentscore, Student
        # - Get the TakenCourse By Student and Course
        # - Update the the TakenCourse instance
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)  # gather all the all students id (i.e the keys) in a tuple
        print('STUDENT IDS: ', ids)
        for s in range(0, len(ids)):  # iterate over the list of student ids gathered above
            # student = TakenCourse.objects.get(id=ids[s])
            # print("CURRENT STUDENT: ", str(student.student))
            # Create a new or update a WrittenAssessment object
            # REQUIREMENTS: Selected Assessment object, current Student object in the loop
            # 
            # Get the selected assessment instance
            retrieved_assessment_obj = Assessment.objects.get(pk=id)
            print("RETRIEVED ASSESSMENT OBJ: ", str(retrieved_assessment_obj))
            # 
            # Get the Student object currently in the loop
            student_obj = Student.objects.get(pk=ids[s])
            print("RETRIEVED STUDENT OBJ: ", str(student_obj))
            # 
            # Get the Score
            score = data.getlist(ids[s])  # get list of score for current student in the loop
            weight = score[0]  # subscript the list to get the fisrt value > ca score
            print("SCORE FROM POST: ", str(weight))

            try:
                # check if the a WrittenAssessment object already exists
                written_ass = WrittenAssessment.objects.get(assessment=assessment, student=student_obj, semester=current_semester)
                if written_ass:
                    written_ass.assessment = assessment
                    written_ass.student = student_obj
                    written_ass.score = weight
                    written_ass.save()

            except WrittenAssessment.DoesNotExist:
                written_assessment, created = WrittenAssessment.objects.get_or_create(assessment=assessment, student=student_obj, score=weight, semester=current_semester)
                if created:
                    written_assessment.save()
           
            # create an assessmentscore instance to be passed to assessment model
            # assessment_score_obj = AssessmentScore.objects.create(assessment_score=weight)
            # print("CREATED ASSESSMENT SCORE OBJ: ", str(assessment_score_obj))


            



            # for ass in assessments:
            #     print('SCORES: ', ass.score.assessment_score)
            #     for ss in ass.participating_students.all():
            #         print("STUDS: ", ss + ', ASS: ', ass)
            #         if ss == student_obj:
            #             print('STUDENT SCORE: ID = ', str(ss.id) + ', NAME = ', ss.student_admission_details.first_name + ', COURSE: ', str(ass.course) + ', SCORE: ', ass.score)




            # # get and update the assessment instance by assigning the assessment_score_obj and student
            # retrieved_assessment_obj = Assessment.objects.get(pk=id)
            # print("RETRIEVED ASSESSMENT OBJ: ", str(retrieved_assessment_obj))

            # get the TakenCourse instance for specified Student and Course
            # try:
            #     taken_course_obj = TakenCourse.objects.get(student=student_obj, course=course_obj)  # get the current student data
            #     print("RETRIEVED TAKEN COURSE OBJ: ID =", str(taken_course_obj.id) + ' - COURSE =' + str(taken_course_obj))
            # except TakenCourse.DoesNotExist:
            #     return HttpResponse('Does not exist!')
            # assessment_score_obj = assessment.score = weight
            # assessment_score_obj.save()

            # retrieved_assessment_obj.score = assessment_score_obj
            # retrieved_assessment_obj.participating_students.add(student_obj)
            # assessment_obj = retrieved_assessment_obj.save()

            # assign the assessment_obj to the takencourse
            # taken_course_obj.assessment = assessment_obj  # set current student assessment score

            # obj.ca2 = ca2 
            # obj.exam = exam  # set current student exam score
            # obj.total = obj.get_total(ca=ca, ca2=ca2, exam=exam)
            # obj.grade = obj.get_grade(ca=ca, ca2=ca2, exam=exam)
            # obj.comment = obj.get_comment(obj.grade)
            #obj.carry_over(obj.grade)
            #obj.is_repeating()
            # taken_course_obj.save()
            # assessment_obj = assessment.save()
            # gpa = obj.calculate_gpa(total_unit_in_semester)
            # cgpa = obj.calculate_cgpa()
            # try:
            #     a = Result.objects.get(student=student.student, semester=current_semester, level=student.student.level)
            #     a.gpa = gpa
            #     a.cgpa = cgpa
            #     a.save()
            # except:
            #     Result.objects.get_or_create(student=student.student, gpa=gpa, semester=current_semester, level=student.student.level)
        messages.success(request, 'Successfully Recorded! ')
        return HttpResponseRedirect(reverse_lazy('add_score_for', kwargs={'assessment_id': id, 'course_id': course_id}))
    return HttpResponseRedirect(reverse_lazy('add_score_for', kwargs={'assessment_id': id, 'course_id': course_id}))


@login_required()
def student_taken_course_list(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
        # get logged in student details
        if request.user.is_student:
            student = Student.objects.get(user=request.user)
            print('CURRENT SEMESTER: ', current_semester)
            print('STUDENT: ', student)
            print('STUDENT PROGRAM: ', student.student_admission_details.program_applied_for)
        else:
            pass

        print('INSIDE TRY!')

        # get courses for current semester for a specific programme
        courses_in_program = Course.objects.filter(semester=current_semester.semester, course_program=student.student_admission_details.program_applied_for)
        for c in courses_in_program:
            print('COURSE: ', c)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    except Course.DoesNotExist:
        print('COURSE DOES NOT EXIST')
        # pass
    
    # Get list of payment
    taken_courses = TakenCourse.objects.filter(student__user=request.user, semester=current_semester)

    return render(request, "schoolapp/systempages/student_taken_courses_list.html",
                  {
                      'taken_courses': taken_courses,
                      'current_semester': current_semester,
                      'courses_in_program': courses_in_program
                  })


# register course
@login_required
def student_register_course(request):
    try:
        # get current semester
        current_semester = Semester.objects.get(is_current_semester=True)

        # get logged in student details
        if request.user.is_student:
            student = Student.objects.get(user=request.user)
        else:
            pass

        # get courses for current semester for a specific programme
        courses_in_program = Course.objects.filter(semester=current_semester.semester, course_program=student.student_admission_details.program_applied_for)

        # get registered courses
        taken_courses = TakenCourse.objects.filter(student__user=request.user)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    except Student.DoesNotExist:
        return HttpResponse('Student does not exist, contact support for help.')
    except Course.DoesNotExist:
        return HttpResponse('Course does not exist, contact support for help.')
    except TakenCourse.DoesNotExist:
        return HttpResponse('Registered Course does not exist, contact support for help.')
    

    if request.method=='POST':
        register_course_form = RegisterCourseForm(request.POST, request.FILES)
        print('INSIDE REGISTER COURSE POST')

        if register_course_form.is_valid():
            rcf = register_course_form.save(commit=False)
            print('FORM VALID!')
            print('STUDENT: ', Student.objects.get(user=request.user))
            print('SEMESTER: ', Semester.objects.get(is_current_semester=True))
            rcf.student = Student.objects.get(user=request.user)
            rcf.semester = Semester.objects.get(is_current_semester=True)
            rcf.registration_type = 'Repeat Registration'
            
            try:
                rcf.save()
            except IntegrityError:
                print("INTEGRITY ERROR: ", str(register_course_form.errors))
                return redirect('student_taken_course_list')

            
            return render(request, 'schoolapp/systempages/student_taken_courses_list.html', {
                'register_course_form': register_course_form,
                'success_message': 'Course Registered Successfully',
                'courses_in_program': courses_in_program,
                'taken_courses': taken_courses,
                'current_semester': current_semester
            })
        else:
            register_course_form = RegisterCourseForm()
            return render(request, 'schoolapp/systempages/student_register_course.html', {
                'register_course_form': register_course_form,
                'error_message': 'Course Not Registered: '+ str(register_course_form.errors),
                'courses_in_program': courses_in_program,
                'taken_courses': taken_courses,
                'current_semester': current_semester
            })
    else:
        register_course_form = RegisterCourseForm()
        return render(request, 'schoolapp/systempages/student_register_course.html', {
            'register_course_form': register_course_form,
            'taken_courses': taken_courses,
            'courses_in_program': courses_in_program,
            'current_semester': current_semester
            # 'error_message': 'Course Not Registered: '+ str(register_course_form.errors)
        })


@login_required()
def create_assessment(request, course_id):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
        # print('CURRENT SEMESTER: ' + str(current_semester))
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')

    course = Course.objects.get(pk=course_id, semester=current_semester.semester)

    assessments = Assessment.objects.filter(course__semester=current_semester.semester)

    if request.method == 'POST':
        # create_assessment_form = CreateAssessmentForm(request.POST, request.FILES)
        print('INSIDE POST: ')
        print('COURSE ID FROM POST: ' + str(request.POST.get('course_id')))
        print('ASSESSMENT NAME: ' + str(request.POST.get('assessment_name')))
        print('TOTAL MARKS: ' + str(request.POST.get('total_marks')))
        print('DATE: ' + str(request.POST.get('date')))
        print('COURSE DB: ' + str(course.course_name))

        try:
            Assessment.objects.create(assessment_name=request.POST.get('assessment_name'), created_by=request.user, course=course, total_marks=request.POST.get('total_marks'), date=request.POST.get('date'))
            return render(request, 'schoolapp/systempages/admin_list_assessments.html',
                  {
                      'success_message': 'Assessment added successfully',
                      'course_id': course_id,
                      'course': course,
                      'assessments': assessments,
                      'current_semester': current_semester
                  })
        except:
            return render(request, 'schoolapp/systempages/add-assessment.html',
                  {
                      'error_message': 'Failed To Add Assessment',
                      'course_id': course_id,
                      'course': course,
                      'current_semester': current_semester
                  })
        
        # return redirect('admin_list_assessment')
        # if create_assessment_form.is_valid():
        #     print('FORM VALID')
        #     print(create_assessment_form.cleaned_data['assessment_name'])
        #     print('COURSE ID: ', request.POST.get('course_id'))
        #     # print(create_assessment_form.cleaned_data['semester'])
        #     # create_assessment_form.course = Course.objects.get(pk=request.POST.get('course_id'))
        #     create_assessment_form.save()
        #     return redirect('add_score')

        # else:
        #     create_assessment_form = CreateAssessmentForm()
        #     print(create_assessment_form.errors)
        #     return render(request, 'schoolapp/systempages/add-assessment.html',
        #                   {
        #                       'create_assessment_form': create_assessment_form,
        #                       'course_id': course_id,
        #                       'course': course,
        #                   })
    # create_assessment_form = CreateAssessmentForm()
    else:
        return render(request, 'schoolapp/systempages/add-assessment.html',
                  {
                    #   'create_assessment_form': create_assessment_form,
                      'course_id': course_id,
                      'course': course,
                      'current_semester': current_semester
                  })
    # return render(request, 'schoolapp/systempages/add-assessment.html',
    #               {
    #                 #   'create_assessment_form': create_assessment_form,
    #                   'course_id': course_id,
    #                   'course': course,
    #               })


@login_required()
def admin_list_assessment(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')

    assessments = Assessment.objects.filter(course__semester=current_semester.semester)
    return render(request, 'schoolapp/systempages/admin_list_assessments.html', {
        'assessments': assessments,
        'current_semester': current_semester
    })


@login_required
def admin_list_years_of_study(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    years_of_study = Level.objects.all()
    return render(request, 'schoolapp/systempages/admin_school_years_list.html', 
    {
        'years_of_study': years_of_study,
        'current_semester': current_semester
    })


@login_required
def admin_list_school_years_details(request, level_id):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    year_of_study = Level.objects.get(pk=level_id)
    programs = Program.objects.filter(program_year=year_of_study)
    return render(request, 'schoolapp/systempages/admin_program_list.html', 
    {
        'programs': programs,
        'current_semester': current_semester
    })


@login_required
def admin_list_assessments_incourse(request, course_id):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
        course = Course.objects.get(id=course_id)
        assessments = Assessment.objects.filter(course=course)
        return render(request, 'schoolapp/systempages/admin_list_assessments_in_course.html', 
        {
            'assessments': assessments,
            'current_semester': current_semester
        })
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    except Course.DoesNotExist:
        pass
    
    return render(request, 'schoolapp/systempages/admin_list_assessments_in_course.html', 
    {
        'current_semester': current_semester
    })


@login_required
def admin_add_final_results_get_programs_list(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    programs = Program.objects.all()
    return render(request, 'schoolapp/systempages/admin_add_final_result_list_programs.html', 
    {
        'programs': programs,
        'current_semester': current_semester
    })


@login_required
def admin_view_final_results_list(request):
        # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    final_results = FinalResult.objects.all()
    return render(request, 'schoolapp/systempages/admin_view_final_result_list.html', 
    {
        'final_results': final_results,
        'current_semester': current_semester
    })


@login_required
def admin_generate_final_result_for(request, program_id, course_id):
    """
    Shows a page where an examination officer will add score for students that are taking courses
    in a specific semester and session
    """
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # get the Course instance
    program_obj = Program.objects.get(pk=program_id)
    # get courses under the above Program
    courses = Course.objects.filter(course_program=program_obj, semester=current_semester.semester)
    # get the Course instance
    course_obj = Course.objects.get(pk=course_id)
    # assessments = Assessment.objects.all()
    # assessment = Assessment.objects.get(pk=id)
    # written_assessments = WrittenAssessment.objects.all()
    print("CURRENT SEMESTER: ", current_semester)
    if request.method == 'GET':
        # course = Course.objects.get(pk=id)
        # course = assessment.course
        # print('COURSE: ', course.course_name)
        # print('ASSESSMENT: ', assessment)
        students = TakenCourse.objects.filter(course=course_obj).filter(semester=current_semester)
        for s in students:
            print('STUDENTS: ID = ', str(s.student.id) + ', NAME = ', s.student.student_admission_details.first_name)
        
        context = {
            "program_obj": program_obj,
            "courses": courses,
            "course": course_obj,
            "students": students,
            # "assessments": assessments,
            # "assessment": assessment,
            # "written_assessments": written_assessments,
            'current_semester': current_semester
        }
        return render(request, 'schoolapp/systempages/admin-generate-final-result-for.html', context)



    if request.method == 'POST':
        # Whats neeedd: Selected Course ID, Student IDs under the Course and the Score of specific Students 
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)  # gather all the students id (i.e the keys) in a tuple
        print('STUDENT IDS: ', ids)
        for s in range(0, len(ids)):  # iterate over the list of student ids gathered above
            # print("RETRIEVED ASSESSMENT OBJ: ", str(retrieved_assessment_obj))
            # 
            # Get the Student object currently in the loop
            student_obj = Student.objects.get(pk=ids[s])
            print("RETRIEVED STUDENT OBJ: ", str(student_obj))
            # 
            # Get the Choice
            choices = data.getlist(ids[s])  # get list of score for current student in the loop
            choice = choices[0]  # subscript the list to get the fisrt value > ca score
            print("CHOICE FROM POST: ", str(choice))

            # get wriiten assessments for the student in the provided course for the current semester
            written_assessments = WrittenAssessment.objects.filter(student=student_obj, assessment__course=course_obj, semester=current_semester)
            
            # initlize final score to zero
            final_score = 0

            # get final results for the student in the provided course for the current semester
            try:
                final_results = FinalResult.objects.get(student=student_obj, course=course_obj, semester=current_semester)
                print('FINAL RESULT: %s' % final_results)
                if final_results:
                    for wa in written_assessments:
                        # if wa.student == final_results.student and wa.assessment.course == final_results.course and wa.semester == final_results.semester:
                        final_score =+ wa.score
                        print('WRITTEN ASSESSMENT: %s' % wa.student)
                # return final_score
                final_results.total = final_score
                final_results.course = course_obj
                final_results.save()
            
            except FinalResult.DoesNotExist:
                for wa in written_assessments:
                    final_score =+ wa.score
                
                final_result, created = FinalResult.objects.get_or_create(student=student_obj, course=course_obj,  total=final_score, semester=current_semester)
                if created:
                    final_result.save()
            # try:
            #     # check if the a WrittenAssessment object already exists
            #     written_ass = WrittenAssessment.objects.get(assessment=assessment, student=student_obj, semester=current_semester)
            #     if written_ass:
            #         written_ass.assessment = assessment
            #         written_ass.student = student_obj
            #         written_ass.score = weight
            #         written_ass.save()

            # except WrittenAssessment.DoesNotExist:
            #     written_assessment, created = WrittenAssessment.objects.get_or_create(assessment=assessment, student=student_obj, score=weight, semester=current_semester)
            #     if created:
            #         written_assessment.save()
           
        messages.success(request, 'Successfully Created Final Results Record!')
        return HttpResponseRedirect(reverse_lazy('admin_generate_final_result_for', kwargs={"program_id": program_id,'course_id': course_id,}))
    return HttpResponseRedirect(reverse_lazy('admin_generate_final_result_for', kwargs={"program_id": program_id,'course_id': course_id,}))


@login_required
def student_view_final_results(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    results = FinalResult.objects.filter(student__user=request.user, semester=current_semester)
    return render(request, 'schoolapp/systempages/student-view-results.html',
    {
        'results': results,
    })


@login_required
def student_view_written_assessments_results(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # Get list of student_registered_courses
    # student_registered_courses = TakenCourse.objects.filter(student__user=request.user, semester=current_semester)
    # total = 0
    # for src in student_registered_courses:
    #     print('REGISTERED COURSE:', src.course)
    #     written_assessments_by_course = WrittenAssessment.objects.filter(assessment__course=src.course, student__user=request.user, semester=current_semester)
    #     for wa in written_assessments_by_course:
    #         print('STUDENT REGISTERED COURSE IN WA:', wa.assessment.course.course_name + ', ASSESSMENT: ' + str(wa.assessment) + ', SCORE: ' + str(wa.score))
    #         total += wa.score
    #     print('ASSESSMENTS TOTAL: ', total)
    #     print('')
    #     # reset total to 0
    #     total = 0

    # Get list of student_registered_courses
    student_registered_courses = TakenCourse.objects.filter(student__user=request.user, semester=current_semester)
    written_assessmentss = WrittenAssessment.objects.filter(student__user=request.user, semester=current_semester)
    total = 0
    for src in student_registered_courses:
        print('REGISTERED COURSE:', src.course)
        # written_assessments_by_course = WrittenAssessment.objects.filter(assessment__course=src.course, student__user=request.user, semester=current_semester)
        for wa in written_assessmentss:
            if src.course == wa.assessment.course:
                print('STUDENT REGISTERED COURSE IN WA:', wa.assessment.course.course_name + ', ASSESSMENT: ' + str(wa.assessment) + ', SCORE: ' + str(wa.score))
                total += wa.score
        print('ASSESSMENTS TOTAL: ', total)
        print('')
        # reset total to 0
        total = 0

    written_assessments = WrittenAssessment.objects.filter(student__user=request.user, semester=current_semester)
    
    # for wa in written_assessments:
    #     print('STUDENT REGISTERED COURSE IN WA:', wa.assessment.course.course_name)
    return render(request, 'schoolapp/systempages/student-view-written-assessments-results.html',
    {
        'current_semester': current_semester,
        'student_registered_courses': student_registered_courses,
        'written_assessments': written_assessments,
    })


def generate_results_transcript_pdf(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # Get list of student_registered_courses
    student_registered_courses = TakenCourse.objects.filter(student__user=request.user, semester=current_semester)
    written_assessmentss = WrittenAssessment.objects.filter(student__user=request.user, semester=current_semester)

    data = {
            'student_registered_courses': student_registered_courses, 
            'written_assessmentss':written_assessmentss,
            'current_semester': current_semester
            }
    
    # Render the HTML template with the data
    template = get_template('schoolapp/reports/student_results_transcript_report.html')
    html = template.render(data)
    
    # Generate the PDF using pdfkit
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'enable-local-file-access': '',
    }
    pdf_content = pdfkit.from_string(html, False, options=options)
    
    # write PDF content to file
    with open('tmp_student_results_transcript_report.pdf', 'wb') as f:
        f.write(pdf_content)

    # create response indicating success
    pdfresponse = HttpResponse(pdf_content, content_type='application/pdf')
    pdfresponse['Content-Disposition'] = 'attachment; filename="tmp_student_application_report.pdf"'
    return pdfresponse


@login_required
def auto_course_registration(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
        if request.user.is_student:
            student_obj = Student.objects.get(user=request.user)
        else:
            return redirect('login')
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    except Student.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        print('POST DATA: ', data)
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            # ids = ids + (str(key),)  # gather all the all students id (i.e the keys) in a tuple
            print('COURSE ID: ', key)
            course = Course.objects.get(pk=key)
            taken_course_obj, created = TakenCourse.objects.get_or_create(student=student_obj, semester=current_semester, course=course)
            
    return redirect('student_taken_course_list')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

class ViewResultsPDF(View):
    def get(self, request, *args, **kwargs):
        # get current semester
        current_semester = Semester.objects.get(is_current_semester=True)

        # Get list of student_registered_courses
        student_registered_courses = TakenCourse.objects.filter(student__user=request.user, semester=current_semester)
        written_assessmentss = WrittenAssessment.objects.filter(student__user=request.user, semester=current_semester)

        data = {
                'student_registered_courses': student_registered_courses, 
                'written_assessmentss':written_assessmentss,
                'current_semester': current_semester
                }
        pdf = render_to_pdf('schoolapp/reports/student_results_transcript_report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class ViewApplicationDetailsPDF(View):
    def get(self, request, id, *args, **kwargs):
        # Get data from the model
        application_details = Admission.objects.get(pk=id)

        data = {'application_details': application_details}

        pdf = render_to_pdf('schoolapp/reports/student_application_report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    

@login_required
def admin_list_courses(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    courses = Course.objects.filter(semester=current_semester.semester)
    return render(request, 'schoolapp/systempages/admin_list_courses.html', 
                    {
                        'courses': courses,
                    })


@login_required
def student_view_payment_history(request):
    # get current semester
    try:
        current_semester = Semester.objects.get(is_current_semester=True)
    except Semester.DoesNotExist:
        return HttpResponse('Semester does not exist, contact support for help.')
    
    # check if logged in user is a student
    if request.user.is_student:
        payment_history = Payment.objects.filter(student__user=request.user)
        current_semester_balances = Payment.objects.filter(student__user=request.user, semester=current_semester)
    else:
        payment_history = Payment.objects.all()
    return render(request, 'schoolapp/systempages/student_view_payment_history.html', 
                  {
                    'payment_history': payment_history,
                    'current_semester_balances': current_semester_balances,
                  })