from django.urls import path
from schoolapp import views

urlpatterns = [
    # testing urls
    path('testtemplate/', views.testtemplate, name='testtemplate'),
    # path('applicationreport/<int:id>/', views.application_report, name='application_report'),
    # path('generatestudentno/', views.generateStudentNumber, name='generateStudentNumber'),
    path('generatestudentnorandomly/', views.generateStudentNumberRandomDigits, name='generateStudentNumberRandomDigits'),

  # Lectures starts
    path('lecturer/', views.lecturer, name='lecture'),
    path('lecturer/modules', views.lecturers_modules),
    path('lecturer/add_module', views.add_modules),
    path('lecturer/edit_module', views.edit_modules),
    path('lecturer/students', views.lecturers_students),
    path('lecturer/student_details', views.lecturers_students_details),
    path('lecturer/edit_student', views.lecturers_students_results),
    # Lecture Ends
    # system urls
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('departments/', views.departments, name='departments'),

    path('programs/', views.programs, name='programs'),
    path('programs/admin/', views.admin_list_programs, name='admin_list_programs'),
    path('programs/admin/<int:program_id>/courses/', views.program_details_admin, name='program_details_admin'),
    path('programs/admin/courses/<int:course_id>', views.admin_list_assessments_incourse, name='admin_list_assessments_incourse'),
    
    path('schools/<int:school_id>/programs/', views.school_details, name='school_details'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.course_details, name='course_details'),
    path('online-admission/', views.online_admission, name='online-admission'),
    path('admin-student-registration/', views.admin_online_student_registration, name='admin_student_registration'),
    path('application-status/', views.templogintocheckapplicationstatus, name='templogintocheckapplicationstatus'),
    path('api/forgot-password/', views.user_forgot_password, name='user_forgot_password'),
    path('api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('admin-admissions/', views.admin_admissions_list, name='admin_admissions_list'),
    path('admin-admissions/<int:admission_id>/', views.admin_admissions_detail, name='admin_admissions_detail'),
    path('update-online-application/<str:student_no>/', views.updateonlineapplication, name='updateonlineapplication'),
    path('admin-admissions/<int:admission_id>/approve/', views.admin_approve_application, name='admin_approve_application'),
    path('admin-add-staff/', views.add_staff, name='add_staff'),
    path('admin-search-application/', views.search_applicant_by_student_no, name='search_applicant_by_student_no'),
    path('admin-add-student/<int:application_id>/', views.add_student, name='add_student'),
    path('admin-add-school/', views.add_school, name='add_school'),
    path('admin-list-staff/', views.list_staff, name='list_staff'),
    path('admin-list-student/', views.list_students, name='list_students'),
    path('admin-list-school/', views.list_schools, name='list_schools'),
    path('admin-add-department/', views.add_department, name='add_department'),
    path('generatestudno/', views.generateStudentNumberRandomDigits, name='generateStudentNumberRandomDigits'),

    # accounts urls
    path('accounts/payments/types/', views.payment_types_list, name='payment_types_list'),
    path('accounts/payments/structures/', views.payment_structures_list, name='payment_structures_list'),
    path('accounts/payments/collections/', views.payment_collections_list, name='payment_collections_list'),
    path('accounts/payments/collect/', views.payment_collect, name='payment_collect'),
    path('accounts/payments/types/add/', views.add_payment_type, name='add_payment_type'),
    path('accounts/payments/structures/add/', views.add_payment_structure, name='add_payment_structure'),

    # results
    path('score/add/', views.add_score, name='add_score'),
    path('score/<int:assessment_id>/<int:course_id>/', views.add_score_for, name='add_score_for'),
    path('admin-create-assessment/<int:course_id>', views.create_assessment, name='create_assessment'),
    path('admin-list-assessments/', views.admin_list_assessment, name='admin_list_assessment'),
    path('admin-list-years-of-study/', views.admin_list_years_of_study, name='admin_list_years_of_study'),
    path('admin-list-years/<int:level_id>', views.admin_list_school_years_details, name='admin_list_school_years_details'),
    path('admin-add-final-results-programs-list/', views.admin_add_final_results_get_programs_list, name='admin_add_final_results_get_programs_list'),
    path('admin-view-final-results-list/', views.admin_view_final_results_list, name='admin_view_final_results_list'),
    path('admin-generate-final-result/<int:program_id>/<int:course_id>/', views.admin_generate_final_result_for, name='admin_generate_final_result_for'),
    path('admin-list-courses/', views.admin_list_courses, name='admin_list_courses'),

    # student urls
    path('student-register-course/', views.student_register_course, name='student_register_course'),
    path('student-list-courses-taken/', views.student_taken_course_list, name='student_taken_course_list'),
    path('student-list-assessments-written/', views.student_view_written_assessments_results, name='student_view_written_assessments_results'),
    path('student-list-final-results/', views.student_view_final_results, name='student_view_final_results'),
    path('student-auto-course-registration/', views.auto_course_registration, name='auto_course_registration'),
    path('student-view-payment-history/', views.student_view_payment_history, name='student_view_payment_history'),

    # reports
    path('student-application-report/<int:id>/', views.generate_pdf_for_student_application, name='generate_pdf_for_student_application'),
    path('student-results-report/', views.generate_results_transcript_pdf, name='generate_results_transcript_pdf'),
    path('student-results-view-pdf-report/', views.ViewResultsPDF.as_view(), name='view_results_transcript_pdf'),
    path('student-application-details-view-pdf-report/<int:id>/', views.ViewApplicationDetailsPDF.as_view(), name='view_pdf_for_student_application'),
    
]
