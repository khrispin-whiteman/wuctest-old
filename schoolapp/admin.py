from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from schoolapp.models import AssessmentType, Semester, Course, Session, Level, User, School, Program, Department, ProgramType, Student, \
    Admission, StudentNumber, Assessment, WrittenAssessment, WucFiles, SystemSettings, Payment, PaymentType, PaymentStructure, TakenCourse, FinalResult


# Register your models here.
# class TheUserAdmin(UserAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'phone', 'address', 'email', 'is_student', 'is_lecturer', 'is_admissions_officer', 'is_accounts_officer', 'is_dean_of_students_officer', 'is_ict_officer', 'is_registrars_officer', 'is_pg_coordinators_officer')
#     list_display_links = ('first_name', 'last_name', 'phone', 'address', 'email', 'is_student', 'is_lecturer',  'is_admissions_officer', 'is_accounts_officer', 'is_dean_of_students_officer', 'is_ict_officer', 'is_registrars_officer', 'is_pg_coordinators_officer' )
#     list_per_page = 10
#     search_fields = ('first_name', 'last_name', 'phone', 'address', 'email', 'is_student', 'is_lecturer', 'is_librarian', 'is_parent', )
class TheUserAdmin(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email', 'is_student', 'is_member_of_staff', 'user_group')
    list_display_links = ('first_name', 'last_name', 'phone', 'email', 'is_student', 'is_member_of_staff', 'user_group')
    list_per_page = 10
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'user_group')
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            'More Fields',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'phone',
                    'is_student',
                    'is_member_of_staff',
                    'user_group',
                ),
            },
        ),
    )


class SemesterAdmin(ImportExportModelAdmin):
    list_display = ('id', 'semester', 'session', 'is_current_semester')
    search_fields = ('semester', 'session')
    list_per_page = 10


class SessionAdmin(ImportExportModelAdmin):
    list_display = ('session', 'is_current_session', )
    search_fields = ('session', )
    list_per_page = 10


class CourseAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ('id', 'course_name', 'course_code', 'course_program', 'level', 'semester', 'full_or_half_course', 'contact_hours', 'credits')
    list_display_links = ('id', 'course_name', 'course_code', )
    search_fields = ('course_name', 'course_code', 'level')
    list_filter = ('level', 'semester')


class SchoolAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ('school_name', 'school_description')
    search_fields = ('school_name', 'school_description')


class ProgramAdmin(ImportExportModelAdmin):
    list_display = ('id', 'program_name', 'program_code', 'program_duration', 'program_type', 'program_coordinator', 'program_school', 'program_year', 'program_description')
    list_per_page = 10
    search_fields = ('program_name', 'program_code', 'program_duration', 'program_description')
    autocomplete_fields = ('program_type', 'program_coordinator', 'program_school')
    list_filter = ('program_type', 'program_duration', 'program_school', 'program_year')


class DepartmentAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ('department_name', 'hod', 'department_description')
    search_fields = ('department_name', 'hod', 'department_description')


class LevelAdmin(ImportExportModelAdmin):
    list_display = ('level',)
    list_display_links = ('level',)
    list_per_page = 10
    search_fields = ('level',)


class ProgramTypeAdmin(ImportExportModelAdmin):
    list_display = ('pg_type_name', 'pg_type_description')
    list_display_links = ('pg_type_name', 'pg_type_description')
    list_per_page = 10
    search_fields = ('pg_type_name', 'pg_type_description')


class StudentNumberAdmin(ImportExportModelAdmin):
    list_display = ('full_student_no',)
    list_display_links = ('full_student_no',)
    list_per_page = 10
    search_fields = ('full_student_no',)


class SystemSettingsAdmin(ImportExportModelAdmin):
    list_display = ('student_no_last_digits_length',)
    list_display_links = ('student_no_last_digits_length',)
    list_per_page = 10
    search_fields = ('student_no_last_digits_length',)


class StudentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'student_admission_details', 'level')
    list_display_links = ('id', 'user', 'student_admission_details', 'level')
    list_per_page = 10
    search_fields = ('user', 'student_admission_details__student_number', 'level')
    autocomplete_fields = ('user', 'student_admission_details', )
    date_hierarchy = 'student_registration_date'


class AdmissionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'nrc_no', 'phone_number', 'email', 'gender', 'program_applied_for')
    list_display_links = ('id', 'first_name', 'last_name', 'nrc_no', 'phone_number', 'email', 'gender', 'program_applied_for')
    list_per_page = 10
    search_fields = ('first_name', 'last_name', 'nrc_no', 'phone_number', 'student_number__full_student_no', 'email', 'gender', 'program_applied_for__program_name')
    date_hierarchy = 'admission_date'
    list_filter = ('application_status', 'gender', 'is_active')


#  accounts modules
class PaymentTypeAdmin(ImportExportModelAdmin):
    list_display = ('payment_type_name',)
    list_display_links = ('payment_type_name',)
    list_per_page = 10
    search_fields = ('payment_type_name',)


class PaymentStructureAdmin(ImportExportModelAdmin):
    list_display = ('payment_level', 'amount_to_be_paid', 'semester', 'payment_description')
    list_display_links = ('payment_level', 'amount_to_be_paid', 'semester', 'payment_description')
    list_per_page = 10
    search_fields = ('payment_level__level', 'amount_to_be_paid', 'payment_description__payment_type_name',)


class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('student', 'amountpaid', 'actualamountpaid', 'paymentstructure', 'balance', 'total_amount_to_be_paid', 'semester', 'paymentstatus', 'paymentdate')
    list_display_links = ('student', 'amountpaid', 'actualamountpaid', 'paymentstructure', 'balance', 'total_amount_to_be_paid', 'semester', 'paymentstatus', 'paymentdate')
    list_per_page = 10
    search_fields = ('student__user__username', 'amountpaid', 'actualamountpaid', 'paymentstructure__amount_to_be_paid', 'balance', 'total_amount_to_be_paid', 'paymentstatus', 'paymentdate')
    date_hierarchy = 'paymentdate'
    list_filter = ('semester', )


class TakenCourseAdmin(ImportExportModelAdmin):
    list_display = ('id', 'student', 'semester', 'course', )
    list_display_links = ('student', 'semester', 'course', )
    list_per_page = 10
    search_fields = ('student__full_student_no', 'semester',)
    list_filter = ('semester',)
    autocomplete_fields = ('student', 'semester', 'course', )


class FinalResultAdmin(ImportExportModelAdmin):
    list_display = ('student', 'course', 'semester', 'total', 'grade', 'comment')
    list_display_links = ('student', 'course', 'semester', 'total', 'grade', 'comment')
    list_per_page = 10
    search_fields = ('student', 'course', 'semester', 'total', 'grade', 'comment')
    list_filter = ('semester', 'grade', 'comment')
    autocomplete_fields = ('student', 'semester', 'course',)

    


class AssessmentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'assessment_name', 'course', 'created_by', 'total_marks', 'date',)
    list_display_links = ('assessment_name', 'course', 'created_by', 'total_marks', 'date',)
    list_per_page = 10
    search_fields = ('course__course_name',)
    list_filter = ('course', 'course__course_program')
    # date_hierarchy = 'date'
    autocomplete_fields = ('course', )


class AssessmentTypeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'assessment_type',)
    list_display_links = ('assessment_type', )
    list_per_page = 10


class WrittenAssessmentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'assessment', 'student', 'score', 'semester')
    list_display_links = ('id', 'assessment', 'student', 'score', 'semester')
    list_per_page = 10
    search_fields = ('id', 'student__user', 'assessment__assessment_name', 'semester')
    autocomplete_fields = ('student', 'assessment', 'semester')
    list_filter = ('semester', )


class WucFilesAdmin(ImportExportModelAdmin):
    list_display = ('file',)
    list_display_links = ('file',)
    list_per_page = 10
    search_fields = ('file',)


admin.site.register(Session, SessionAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(User, TheUserAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(ProgramType, ProgramTypeAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Admission, AdmissionAdmin)
admin.site.register(StudentNumber, StudentNumberAdmin)
admin.site.register(SystemSettings, SystemSettingsAdmin)
admin.site.register(PaymentType, PaymentTypeAdmin)
admin.site.register(PaymentStructure, PaymentStructureAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(TakenCourse, TakenCourseAdmin)
admin.site.register(FinalResult, FinalResultAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(WrittenAssessment, WrittenAssessmentAdmin)
admin.site.register(AssessmentType, AssessmentTypeAdmin)
admin.site.register(WucFiles, WucFilesAdmin)