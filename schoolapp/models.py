from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseNotFound
from django.urls import reverse
import decimal
from django.template.defaultfilters import default
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
COUNTRIES = (
    ('Zambia', 'Zambia'),
    ('AD', 'Andorra'),
    ('AE', 'United Arab Emirates'),
    ('AF', 'Afghanistan'),
    ('AG', 'Antigua & Barbuda'),
    ('AI', 'Anguilla'),
    ('AL', 'Albania'),
    ('AM', 'Armenia'),
    ('AN', 'Netherlands Antilles'),
    ('Angola', 'Angola'),
    ('AQ', 'Antarctica'),
    ('AR', 'Argentina'),
    ('AS', 'American Samoa'),
    ('AT', 'Austria'),
    ('AU', 'Australia'),
    ('AW', 'Aruba'),
    ('AZ', 'Azerbaijan'),
    ('BA', 'Bosnia and Herzegovina'),
    ('BB', 'Barbados'),
    ('BD', 'Bangladesh'),
    ('BE', 'Belgium'),
    ('BF', 'Burkina Faso'),
    ('BG', 'Bulgaria'),
    ('BH', 'Bahrain'),
    ('BI', 'Burundi'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BN', 'Brunei Darussalam'),
    ('BO', 'Bolivia'),
    ('BR', 'Brazil'),
    ('BS', 'Bahama'),
    ('BT', 'Bhutan'),
    ('BV', 'Bouvet Island'),
    ('BW', 'Botswana'),
    ('BY', 'Belarus'),
    ('BZ', 'Belize'),
    ('CA', 'Canada'),
    ('CC', 'Cocos (Keeling) Islands'),
    ('CF', 'Central African Republic'),
    ('CG', 'Congo'),
    ('CH', 'Switzerland'),
    ('Ivory Coast', 'Ivory Coast'),
    ('CK', 'Cook Islands'),
    ('CL', 'Chile'),
    ('CM', 'Cameroon'),
    ('CN', 'China'),
    ('CO', 'Colombia'),
    ('CR', 'Costa Rica'),
    ('CU', 'Cuba'),
    ('Cape Verde', 'Cape Verde'),
    ('CX', 'Christmas Island'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('DE', 'Germany'),
    ('DJ', 'Djibouti'),
    ('DK', 'Denmark'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('Algeria', 'Algeria'),
    ('EC', 'Ecuador'),
    ('EE', 'Estonia'),
    ('Egypt', 'Egypt'),
    ('EH', 'Western Sahara'),
    ('Eritrea', 'Eritrea'),
    ('ES', 'Spain'),
    ('Ethiopia', 'Ethiopia'),
    ('FI', 'Finland'),
    ('FJ', 'Fiji'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FM', 'Micronesia'),
    ('FO', 'Faroe Islands'),
    ('FR', 'France'),
    ('FX', 'France, Metropolitan'),
    ('Gabon', 'Gabon'),
    ('GB', 'United Kingdom (Great Britain)'),
    ('GD', 'Grenada'),
    ('GE', 'Georgia'),
    ('GF', 'French Guiana'),
    ('Ghana', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GL', 'Greenland'),
    ('Gambia', 'Gambia'),
    ('Guinea', 'Guinea'),
    ('GP', 'Guadeloupe'),
    ('GQ', 'Equatorial Guinea'),
    ('GR', 'Greece'),
    ('GS', 'South Georgia and the South Sandwich Islands'),
    ('GT', 'Guatemala'),
    ('GU', 'Guam'),
    ('GW', 'Guinea-Bissau'),
    ('GY', 'Guyana'),
    ('HK', 'Hong Kong'),
    ('HM', 'Heard & McDonald Islands'),
    ('HN', 'Honduras'),
    ('HR', 'Croatia'),
    ('HT', 'Haiti'),
    ('HU', 'Hungary'),
    ('ID', 'Indonesia'),
    ('IE', 'Ireland'),
    ('IL', 'Israel'),
    ('IN', 'India'),
    ('IO', 'British Indian Ocean Territory'),
    ('IQ', 'Iraq'),
    ('IR', 'Islamic Republic of Iran'),
    ('IS', 'Iceland'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JO', 'Jordan'),
    ('JP', 'Japan'),
    ('Kenya', 'Kenya'),
    ('KG', 'Kyrgyzstan'),
    ('KH', 'Cambodia'),
    ('KI', 'Kiribati'),
    ('Comoros', 'Comoros'),
    ('KN', 'St. Kitts and Nevis'),
    ('KP', 'Korea, Democratic People\'s Republic of'),
    ('KR', 'Korea, Republic of'),
    ('KW', 'Kuwait'),
    ('KY', 'Cayman Islands'),
    ('KZ', 'Kazakhstan'),
    ('LA', 'Lao People\'s Democratic Republic'),
    ('LB', 'Lebanon'),
    ('LC', 'Saint Lucia'),
    ('LI', 'Liechtenstein'),
    ('LK', 'Sri Lanka'),
    ('Liberia', 'Liberia'),
    ('Lesotho', 'Lesotho'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('LV', 'Latvia'),
    ('Libya', 'Libya'),
    ('Morocco', 'Morocco'),
    ('MC', 'Monaco'),
    ('MD', 'Moldova, Republic of'),
    ('Madagascar', 'Madagascar'),
    ('MH', 'Marshall Islands'),
    ('Mali', 'Mali'),
    ('MN', 'Mongolia'),
    ('MM', 'Myanmar'),
    ('Macau', 'Macau'),
    ('MP', 'Northern Mariana Islands'),
    ('MQ', 'Martinique'),
    ('Mauritania', 'Mauritania'),
    ('MS', 'Monserrat'),
    ('MT', 'Malta'),
    ('Mauritius', 'Mauritius'),
    ('MV', 'Maldives'),
    ('Malawi', 'Malawi'),
    ('MX', 'Mexico'),
    ('MY', 'Malaysia'),
    ('Mozambique', 'Mozambique'),
    ('Namibia', 'Namibia'),
    ('NC', 'New Caledonia'),
    ('Niger', 'Niger'),
    ('NF', 'Norfolk Island'),
    ('Nigeria', 'Nigeria'),
    ('NI', 'Nicaragua'),
    ('NL', 'Netherlands'),
    ('NO', 'Norway'),
    ('NP', 'Nepal'),
    ('NR', 'Nauru'),
    ('NU', 'Niue'),
    ('New Zealand', 'New Zealand'),
    ('OM', 'Oman'),
    ('PA', 'Panama'),
    ('PE', 'Peru'),
    ('PF', 'French Polynesia'),
    ('PG', 'Papua New Guinea'),
    ('PH', 'Philippines'),
    ('PK', 'Pakistan'),
    ('PL', 'Poland'),
    ('PM', 'St. Pierre & Miquelon'),
    ('PN', 'Pitcairn'),
    ('PR', 'Puerto Rico'),
    ('PT', 'Portugal'),
    ('PW', 'Palau'),
    ('PY', 'Paraguay'),
    ('QA', 'Qatar'),
    ('RE', 'Reunion'),
    ('RO', 'Romania'),
    ('RU', 'Russian Federation'),
    ('Rwanda', 'Rwanda'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('Solomon Islands', 'Solomon Islands'),
    ('Seychelles', 'Seychelles'),
    ('Sudan', 'Sudan'),
    ('SE', 'Sweden'),
    ('SG', 'Singapore'),
    ('SH', 'St. Helena'),
    ('SI', 'Slovenia'),
    ('SJ', 'Svalbard & Jan Mayen Islands'),
    ('SK', 'Slovakia'),
    ('SL', 'Sierra Leone'),
    ('SM', 'San Marino'),
    ('Senegal', 'Senegal'),
    ('Somalia', 'Somalia'),
    ('SR', 'Suriname'),
    ('ST', 'Sao Tome & Principe'),
    ('SV', 'El Salvador'),
    ('SY', 'Syrian Arab Republic'),
    ('Swaziland', 'Swaziland'),
    ('TC', 'Turks & Caicos Islands'),
    ('Chad', 'Chad'),
    ('TF', 'French Southern Territories'),
    ('Togo', 'Togo'),
    ('TH', 'Thailand'),
    ('TJ', 'Tajikistan'),
    ('TK', 'Tokelau'),
    ('TM', 'Turkmenistan'),
    ('Tunisia', 'Tunisia'),
    ('Tonga', 'Tonga'),
    ('TP', 'East Timor'),
    ('Turkey', 'Turkey'),
    ('TT', 'Trinidad & Tobago'),
    ('TV', 'Tuvalu'),
    ('TW', 'Taiwan, Province of China'),
    ('Tanzania', 'Tanzania'),
    ('UA', 'Ukraine'),
    ('Uganda', 'Uganda'),
    ('UM', 'United States Minor Outlying Islands'),
    ('US', 'United States of America'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VA', 'Vatican City State (Holy See)'),
    ('VC', 'St. Vincent & the Grenadines'),
    ('VE', 'Venezuela'),
    ('VG', 'British Virgin Islands'),
    ('VI', 'United States Virgin Islands'),
    ('VN', 'Viet Nam'),
    ('VU', 'Vanuatu'),
    ('WF', 'Wallis & Futuna Islands'),
    ('WS', 'Samoa'),
    ('YE', 'Yemen'),
    ('YT', 'Mayotte'),
    ('Yugoslavia', 'Yugoslavia'),
    ('South Africa', 'South Africa'),
    ('Zambia', 'Zambia'),
    ('Zaire', 'Zaire'),
    ('Zimbabwe', 'Zimbabwe'),
    ('Unknown or unspecified country', 'Unknown or unspecified country'),
)


COURSE_REGISTRATION_TYPES = (
    ('Repeat Registration', "Repeat Registration"),
    ('Normal Registration', "Normal Registration"),
)


GENDER = (
    ('Male', "Male"),
    ('Female', "Female"),
    ('Other', "Other"),
)

MARITAL_STATUS = (
    ("---------", "---------"),
    ('Single', "Single"),
    ('Married', "Married"),
    ('Widowed', "Widowed"),
    ('Divorced', "Divorced"),
    ('Separated', "Separated"),
)

RELATIONSHIP_WITH_GUARDIAN = (
    ("Father", "Father"),
    ("Mother", "Mother"),
    ("Brother", "Brother"),
    ("Sister", "Sister"),
    ("Uncle", "Uncle"),
    ("Aunty", "Aunty"),
    ("Cousin", "Cousin"),
    ("Grand-Parent", "Grand-Parent"),
    ("Husband", "Husband"),
    ("Wife", "Wife"),
    ("Other", "Other"),
)

PROFESSIONAL_QUALIFICATION = (
    ('Certificate', "Certificate"),
    ('Diploma', "Diploma"),
    ('Degree', "Degree"),
)

APPLICATION_STATUS_CHOICES = (
    ('Verified', "Verified"),
    ('Pending', "Pending"),
    ('Approved', "Approved"),
    ('Rejected', "Rejected"),
)


REGISTRATION_STATUS_CHOICES = (
    ('Reported', "Reported"),
    ('Not Reported', "Not Reported"),
    ('Other', "Other"),
)


USER_GROUPS = (
    ('Admissions Office', 'Admissions Office'),
    ('Accounts Office', 'Accounts Office'),
    ('Dean Of Students Affairs Office', 'Dean Of Students Affairs Office'),
    ('ICT Office', 'ICT Office'),
    ('Program Coordinator or Principal Lecturer Office', 'Program Coordinator or Principal Lecturer Office'),
    ('Registrar Office', 'Registrar Office'),
    ('Lecturer', 'Lecturer'),
    ('Examinations Office', 'Examinations Office'),
    ('Other Staff', "Other Staff"),
)

A = "A"
B = "B"
C = "C"
D = "D"
F = "F"
PASS = "PASS"
FAIL = "FAIL"

GRADE = (
    (A, 'A'),
    (B, 'B'),
    (C, 'C'),
    (D, 'D'),
    (F, 'F'),
)

COMMENT = (
    (PASS, "PASS"),
    (FAIL, "FAIL"),
)

FIRST = "First"
SECOND = "Second"

SEMESTER = (
    ("Semester 1", "Semester 1"),
    ("Semester 2", "Semester 2"),
)

CLASS_ATTENDANCE = (
    ('Present', 'Present'),
    ('Absent', 'Absent'),
)

DAYS = (
    ("Sun", "Sunday"),
    ("Mon", "Monday"),
    ("Tue", "Tuesday"),
    ("Wed", "Wednesday"),
    ("Thur", "Thursday"),
    ("Fri", "Friday"),
    ("Sat", "Saturday"),
)

FULL_HALF_COURSE = (
    ('Half', 'Half'),
    ('Full', 'Full'),
)


class User(AbstractUser):
    is_student = models.BooleanField(default=False, blank=True, null=True)
    is_member_of_staff = models.BooleanField(default=False)
    # is_admissions_officer = models.BooleanField(default=False)
    # is_accounts_officer = models.BooleanField(default=False)
    # is_dean_of_students_officer = models.BooleanField(default=False)
    # is_ict_officer = models.BooleanField(default=False)
    # is_registrars_officer = models.BooleanField(default=False)
    # is_pg_coordinators_officer = models.BooleanField(default=False)
    user_group = models.CharField('User Group', max_length=60, blank=True, null=True, choices=USER_GROUPS)
    phone = models.CharField(max_length=60, blank=True, null=True)
    # address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(upload_to="users/pictures/%Y/%m/%d'", blank=True, null=True)
    email = models.EmailField(unique=False, blank=True, null=True)

    def get_picture(self):
        no_picture = f'{settings.STATIC_URL}schoolapp/systempages/assets/img/img_avatar.png'
        try:
            return self.picture.url
        except Exception:
            return no_picture

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username

    def __str__(self):
        return self.get_full_name()


class Department(models.Model):
    department_name = models.CharField(max_length=200)
    hod = models.ForeignKey(User, default='', null=True, help_text='Head of department', on_delete=models.SET_NULL)
    department_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.department_name


class School(models.Model):
    school_name = models.CharField(max_length=200)
    school_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.school_name


class ProgramType(models.Model):
    pg_type_name = models.CharField('Program Type Name', max_length=200)
    pg_type_description = models.TextField('Program Type Description', null=True, blank=True)

    def __str__(self):
        return self.pg_type_name


class Program(models.Model):
    program_name = models.CharField(max_length=200)
    program_code = models.CharField(null=True, blank=True, max_length=200)
    program_school = models.ForeignKey(School, on_delete=models.CASCADE)
    program_type = models.ForeignKey(ProgramType, blank=True, on_delete=models.CASCADE)
    program_description = models.TextField()
    program_year = models.ForeignKey('Level', blank=True, null=True, on_delete=models.SET_NULL)
    program_duration = models.CharField('Duration', null=True, blank=True, max_length=200)
    program_coordinator = models.ForeignKey(User, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.program_name


class Session(models.Model):
    session = models.CharField(max_length=200, unique=True, help_text='2022/2023')
    is_current_session = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return 'Academic Session: ' + self.session


class Semester(models.Model):
    semester = models.CharField(max_length=200, choices=SEMESTER, blank=True)
    is_current_semester = models.BooleanField(default=False, blank=True, null=True)
    # session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    session = models.CharField(max_length=200, unique=True, help_text='2022/2023')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{str(self.session)} - {str(self.semester)}'


class Level(models.Model):
    level = models.CharField('Year', max_length=200, help_text='Year, eg: Year 1 or Year 2')

    def __str__(self):
        return self.level

    class Meta:
        verbose_name_plural = 'Levels/Years of Study'
        verbose_name = 'Level/Year of Study'


class Course(models.Model):
    course_name = models.CharField('Course Name', max_length=200)
    course_code = models.CharField('Course Code', max_length=200)
    course_program = models.ForeignKey(Program, verbose_name='Program', null=True, help_text='Program to which the course belongs',
                                       on_delete=models.SET_NULL)
    course_description = models.TextField(verbose_name='Course Description', null=True, blank=True)
    semester = models.CharField('Semester', max_length=200, null=True, choices=SEMESTER)
    level = models.ForeignKey(Level, verbose_name='Year', help_text='Year, eg: Year 1 or Year 2', null=True, on_delete=models.SET_NULL)
    full_or_half_course = models.CharField('Full/half Course', max_length=200, null=True, choices=FULL_HALF_COURSE)
    contact_hours = models.CharField('Contact Hours', max_length=200, null=True, blank=True)
    credits = models.CharField('Credits', max_length=200, null=True, blank=True)

    def __str__(self):
        return self.course_name


class SchoolClass(models.Model):
    grade = models.ForeignKey(Level, verbose_name='Level', default='', on_delete=models.CASCADE)
    classname = models.CharField('Enter Class Title', max_length=200, default='', help_text='name of class, (eg. A)')
    lecturer = models.ForeignKey(User, verbose_name='Assign Lecturer', max_length=200, default='',
                                     on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, verbose_name='Choose Courses', related_name='class_subject',
                                     help_text='Hold Ctrl to choose multiple')

    def __str__(self):
        return 'Grade: ' + str(self.grade) + self.classname + ', Teacher: ' + str(self.lecturer)

    class Meta:
        verbose_name = 'School Class'
        verbose_name_plural = 'School Classes'


class Student(models.Model):
    user = models.OneToOneField(User, help_text='search by student number', on_delete=models.CASCADE)
    student_admission_details = models.ForeignKey('Admission', help_text='search by student number', null=True, blank=True, on_delete=models.SET_NULL)
    level = models.ForeignKey(Level, verbose_name='Current Year Of Study', default='Year 1', on_delete=models.CASCADE)
    registered_courses = models.ManyToManyField('Course', through='TakenCourse',)
    student_registration_date = models.DateField('Registration Date', auto_now_add=True,)

    def __str__(self):
        return f'{self.student_admission_details.student_number.full_student_no} - {self.user.get_full_name()} - {str(self.level)}'

    # def save(self, **kwargs):
    #     if not self.id:
    #         # set is_student to be true
    #         u = User.objects.get(pk=self.user.pk)
    #         u.is_student = True
    #         u.save(force_update=u.is_active)
    #         super(Student, self).save()

    # def get_absolute_url(self):
    #     return reverse('profile')


class StudentNumber(models.Model):
    full_student_no = models.CharField(max_length=10, verbose_name='Full Student Number')

    def __str__(self):
        return self.full_student_no

import datetime
def default_date_of_birth():
    return datetime.datetime(2005,1,1)

class WucFiles(models.Model):
    file = models.FileField(upload_to="wuc/files/%Y/%m/%d'", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.file)

    class Meta:
        verbose_name = 'Wuc File'
        verbose_name_plural = 'Wuc Files'

class Admission(models.Model):
    # Persanal particulars
    application_date = models.DateField(auto_now=True)
    first_name = models.CharField(max_length=200, default='', verbose_name='First Name')
    last_name = models.CharField(max_length=200, default='', verbose_name='Last Name')
    other_names = models.CharField(max_length=200, null=True, blank=True, verbose_name='Other Names')
    nrc_no = models.CharField(max_length=200, unique=True, help_text='each NRC can only be used once',
                              verbose_name='NRC Number')
    phone_number = models.CharField(max_length=13, default='', verbose_name='Phone Number', )
    email = models.EmailField(max_length=200, verbose_name='Email Address', help_text='Required for communication')
    gender = models.CharField(max_length=200, default='Male', choices=GENDER, verbose_name='Gender')
    date_of_birth = models.DateField(max_length=200, default=default_date_of_birth(), verbose_name='DOB', )
    nationality = models.CharField(max_length=200, choices=COUNTRIES, default='Zambia', verbose_name='Nationality', )
    # nationality = CountryField('Nationality', null=True, blank=True)
    marital_status = models.CharField(max_length=200, default='Single', choices=MARITAL_STATUS,
                                      verbose_name='Marital Status')
    physical_address = models.CharField(max_length=200, default='', verbose_name='Physical Address', )
    postal_address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Postal Address', )
    state_of_any_disabilities = models.CharField(max_length=200, null=True, blank=True,
                                                 verbose_name='State Disabilities If Any')

    # Part 2: Family Information
    sponsors_name_or_next_of_kin = models.CharField(max_length=200, null=True, blank=True,
                                                    verbose_name='Sponsor’s Name Or Next of Kin')
    relationship_with_sponsor_or_next_of_kin = models.CharField(max_length=200, null=True, blank=True,
                                                                choices=RELATIONSHIP_WITH_GUARDIAN,
                                                                verbose_name='Relationship with Sponsor Or Next Of Kin')
    sponsor_or_next_of_kin_cell_no = models.CharField(max_length=200, null=True, blank=True,
                                                      verbose_name='Sponsor Or Next of Kin Cell No')
    sponsor_or_next_of_kin_address = models.CharField(max_length=200, null=True, blank=True,
                                                      verbose_name='Sponsor Or Next of Kin Address')

    # Part 3: Qualifications and Program of choice
    program_applied_for = models.ForeignKey(Program, verbose_name='Program of Choice', blank=True, null=True,
                                            on_delete=models.DO_NOTHING)
    # Schools attended
    # School 1
    school_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='School Name')
    school_start_year = models.DateField(max_length=200, null=True, blank=True, verbose_name='Start Year')
    school_end_year = models.DateField(max_length=200, null=True, blank=True, verbose_name='End Year')
    # School 2
    # school_2_name = models.CharField(max_length=200, default='', verbose_name='School 2 Name')
    # school_2_years_from = models.CharField(max_length=200, default='', verbose_name='School 2 Years From')
    # school_2_years_to = models.CharField(max_length=200, default='', verbose_name='School 2 Years To')
    # Subjects and grades
    subject_english = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='English')
    subject_mathematics = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Mathematics')
    subject_biology_human_and_social = models.PositiveSmallIntegerField(null=True, blank=True,
                                                        verbose_name='Biology/Human & Social')
    subject_history = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='History')
    subject_religious_education = models.PositiveSmallIntegerField(null=True, blank=True,
                                                   verbose_name='Religious Education')
    subject_commerce = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Commerce')
    subject_home_economics = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Home Economics')
    subject_geography = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Geography')
    subject_physical_science = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Physical Science')
    subject_chemistry = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Chemistry')
    subject_physics = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Physics')
    subject_civic_education = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Civic Education')

    subject_art = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Art')
    subject_gmd = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Geometric And Mechanical Drawing (GMD)')
    subject_adma = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Additional Mathematics (ADMA)')
    subject_literature = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Literature')
    subject_agric_science = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Agriculture Science')

    # add other 

    has_certificate = models.BooleanField(max_length=200, default=False, verbose_name='Certificate')
    has_diploma = models.BooleanField(max_length=200, default=False, verbose_name='Diploma')
    has_degree = models.BooleanField(max_length=200, default=False, verbose_name='Degree')
    has_gce = models.BooleanField(max_length=200, default=False, verbose_name='GCE')

    # FILE ATTACHMENTS
    scanned_deposit_slip = models.FileField(upload_to="payments/deposits/%Y/%m/%d'", )
    scanned_nrc_front = models.FileField(null=True, blank=True, upload_to="id/nrc/%Y/%m/%d'", )
    scanned_nrc_back = models.FileField(null=True, blank=True, upload_to="id/nrc/%Y/%m/%d'", )
    scanned_statement_of_result = models.FileField(upload_to="qualifications/statement_of_result/%Y/%m/%d'", )
    scanned_pq_certificate = models.FileField(
        upload_to="qualifications/professional_qualification/%Y/%m/%d'", blank=True, null=True)
    scanned_pq_diploma = models.FileField(
        upload_to="qualifications/professional_qualification/%Y/%m/%d'", blank=True, null=True)
    scanned_pq_degree = models.FileField(
        upload_to="qualifications/professional_qualification/%Y/%m/%d'", blank=True, null=True)
    scanned_gce_results = models.ManyToManyField(WucFiles, blank=True,)

    # Part 4: Declaration
    # Applicant
    declaration_confirmation = models.BooleanField(default=False, verbose_name='I have read the declaration')

    student_number = models.ForeignKey(StudentNumber, max_length=200, default='', verbose_name='Student Number',
                                       on_delete=models.CASCADE)
    application_status = models.CharField(max_length=200, default='Pending', blank=True, null=True, choices=APPLICATION_STATUS_CHOICES,
                                          verbose_name='Application Status')
    registration_status = models.CharField(max_length=200, default='Reported', blank=True, null=True, choices=REGISTRATION_STATUS_CHOICES,
                                          verbose_name='Registration Status')
    application_stage = models.CharField(max_length=200, default='Admissions Office', choices=USER_GROUPS,
                                         verbose_name='Application Stage')

    # approvals
    # approvals
    admissions_office = models.BooleanField(max_length=200, default=False, verbose_name='Admissions Office')
    admissions_office_comment = models.TextField(blank=True, null=True, verbose_name='Admissions Office Comment')
    admissions_office_user = models.ForeignKey(User, related_name='admissions_office_user', blank=True, null=True,
                                               on_delete=models.DO_NOTHING)

    accounts_office = models.BooleanField(max_length=200, default=False, verbose_name='Accounts Office')
    accounts_office_comment = models.TextField(blank=True, null=True, verbose_name='Accounts Office Comment')
    accounts_office_user = models.ForeignKey(User, related_name='accounts_office', blank=True, null=True,
                                             on_delete=models.DO_NOTHING)

    dean_of_students_affairs_office = models.BooleanField(max_length=200, default=False, verbose_name='Dean Of Students Affairs')
    dean_of_students_affairs_office_comment = models.TextField(blank=True, null=True, verbose_name='Deans Office Comment')
    dean_of_students_affairs_office_user = models.ForeignKey(User, related_name='dean_of_students_affairs_user',
                                                             blank=True, null=True, on_delete=models.DO_NOTHING)

    ict_office = models.BooleanField(max_length=200, default=False, verbose_name='ICT Office')
    ict_office_comment = models.TextField(blank=True, null=True, verbose_name='ICT Office Comment')
    ict_office_user = models.ForeignKey(User, related_name='ict_office_user', blank=True, null=True,
                                        on_delete=models.DO_NOTHING)

    program_coordinator_or_principal_lecturer_office = models.BooleanField(max_length=200, default=False,
                                                                           verbose_name='Program Coordinator Or Principal Lecturer')
    program_coordinator_or_principal_lecturer_office_comment = models.TextField(blank=True, null=True, verbose_name='PG Coordinator Office Comment')
    program_coordinator_or_principal_lecturer_office_user = models.ForeignKey(User,
                                                                              related_name='program_coordinator_or_principal_lecturer_user',
                                                                              blank=True, null=True,
                                                                              on_delete=models.DO_NOTHING)
    registrar_office = models.BooleanField(max_length=200, default=False, verbose_name='Registrar')
    registrar_office_comment = models.TextField(blank=True, null=True, verbose_name='Registrar Office Comment')
    registrar_office_user = models.ForeignKey(User, related_name='registrar_office_user', blank=True, null=True,
                                              on_delete=models.DO_NOTHING)
    temp_password = models.CharField('Temp Password', max_length=200, null=True, blank=True)
    balance_due = models.CharField('Balance Due', max_length=200, null=True, blank=True)
    intake = models.ForeignKey(Session, verbose_name='In-take', null=True, blank=True, max_length=200, on_delete=models.DO_NOTHING)

    admission_date = models.DateTimeField('Admission Date', auto_now_add=True,)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class SystemSettings(models.Model):
    student_no_last_digits_length = models.IntegerField('Student No. Last Digits Length',
                                                        help_text='The number of digits after the date on the student number: YYMMdigits',
                                                        blank=True, null=True)
    staff_username_last_digits_length = models.IntegerField('Staff Username Last Digits Length',
                                                        help_text='',
                                                        blank=True, null=True)

    def __str__(self):
        return str(self.student_no_last_digits_length)

    class Meta:
        verbose_name_plural = 'System Settings'

class ExamTimeTable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    additional_info = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.course) + ', ' + str(self.venue) + ', ' + str(self.date)

class CourseAllocation(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name='allocated_course')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.lecturer.username

class SchoolDetails(models.Model):
    schoolname = models.CharField('Name Of School', max_length=500, default='')
    address = models.CharField('School Address', max_length=200, null=True, blank=True, default='School Address')
    email = models.CharField('Email Address', max_length=200, null=True, blank=True,
                             default='exampleemail@exampleemail.com')
    facebook = models.CharField('Facebook Page Link', max_length=1000, blank=True, null=True)
    twitter = models.CharField('Twitter', max_length=1000, blank=True, null=True)
    instagram = models.CharField('Instagram', max_length=1000, blank=True, null=True)
    phone = models.CharField('Tel/Cell', max_length=200, null=True, blank=True, default='Tel/Cell Number')
    photo = models.ImageField('School logo', upload_to='school/logo/%Y/%m/%d', default='', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'School Details'
        verbose_name = 'School Details'

    def __str__(self):
        return self.schoolname

class PupilAttendance(models.Model):
    nameofclass = models.ForeignKey(SchoolClass, verbose_name='Class', default='', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name='Student', default='', on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, verbose_name='Course', default='', on_delete=models.CASCADE)
    mark_attendance = models.CharField(max_length=50, default='Present', choices=CLASS_ATTENDANCE)
    daysdate = models.DateField('Attended On', default='')

    class Meta:
        verbose_name = 'Student Attendance'
        verbose_name_plural = 'Student Attendance'

    def __str__(self):
        return str(self.nameofclass) + ' - ' + str(self.student)

class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField('Day', choices=DAYS, max_length=20)
    start_time = models.TimeField('Start Time', )
    end_time = models.TimeField('End Time', )
    venue = models.CharField('Venue', max_length=200, null=True, blank=True, help_text='Optional')
    description = models.CharField('Description', max_length=200, null=True, blank=True, help_text='Optional')

    def __str__(self):
        return str(self.course.course_name)

class Announcement(models.Model):
    teacher = models.ForeignKey(User, max_length=200, verbose_name='Lecturers Name', on_delete=models.CASCADE)
    announcement = models.TextField('News Details', max_length=10000, )
    announcementdatetime = models.DateTimeField(auto_now=True, verbose_name='Date')
    class Meta:
        verbose_name_plural = 'Announcements'
        verbose_name = 'Announcement'

    def __str__(self):
        return str(self.teacher) + ' - ' + self.announcement

class DepartmentOfTeacher(models.Model):
    department = models.ForeignKey(Department, verbose_name='Name Of Department', default='',
                                   on_delete=models.CASCADE)
    lecturer = models.CharField('Lecturer', default='', max_length=200)

    class Meta:
        verbose_name = 'Lecturer And Department'
        verbose_name_plural = 'Lecturer And Department'

    def __str__(self):
        return str(self.department) + ' - ' + str(self.lecturer)

class AssessmentType(models.Model):
    assessment_type = models.CharField('Assessment Type', max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.assessment_type)

class Assessment(models.Model):
    assessment_name = models.CharField('Assessment Name', max_length=200, null=True, blank=True)
    course = models.ForeignKey(Course, blank=True, null=True, related_name='course_assessed', on_delete=models.SET_NULL)
    # semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    assessment_type = models.ForeignKey(AssessmentType, null=True, blank=True, on_delete=models.CASCADE, related_name='type_of_assessment')
    total_marks = models.FloatField('Score', blank=True, null=True, default=0)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Date Of Assessment')

    def __str__(self):
        return str(self.assessment_name) + ' - ' + str(self.course.course_name)

class WrittenAssessment(models.Model):
    assessment = models.ForeignKey(Assessment, null=True, blank=True, on_delete=models.CASCADE, related_name='written_assessment')
    student = models.ForeignKey(Student, related_name='student_written_assessment', on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    score = models.FloatField('Score', blank=True, null=True, default=0)
    written_on = models.DateField(auto_now_add=True, verbose_name='Written on',)

    def __str__(self):
        return str(self.assessment.course) + ' - ' + str(self.assessment.assessment_name) + ' - ' + str(self.student)
    


class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='taken_courses')
    assessment = models.ForeignKey(Assessment, null=True, blank=True, on_delete=models.CASCADE, related_name='course_assessment')
    is_active = models.BooleanField(default=False)
    registration_type = models.CharField(max_length=200, choices=COURSE_REGISTRATION_TYPES, default='Normal Registration')
    # ca = models.PositiveIntegerField(blank=True, null=True, default=0)
    # ca2 = models.PositiveIntegerField(blank=True, null=True, default=0)
    # exam = models.PositiveIntegerField(blank=True, null=True, default=0)
    # total = models.PositiveIntegerField(blank=True, null=True, default=0)
    # grade = models.CharField(choices=GRADE, max_length=1, blank=True)
    # comment = models.CharField(choices=COMMENT, max_length=200, blank=True)

    def __str__(self):
        return str(self.course.course_name)

    # def get_absolute_url(self):
    #     return reverse('update_score', kwargs={'pk': self.pk})

    # def get_total(self, ca, ca2, exam):
    #     return int(ca) + int(ca2) + int(exam)

    # def get_grade(self, ca, ca2, exam):
    #     total = int(ca) + int(ca2) + int(exam)
    #     if total >= 70:
    #         grade = A
    #     elif total >= 60:
    #         grade = B
    #     elif total >= 50:
    #         grade = C
    #     elif total >= 45:
    #         grade = D
    #     else:
    #         grade = F
    #     return grade

    # def get_comment(self, grade):
    #     if not grade == "F":
    #         comment = PASS
    #     else:
    #         comment = FAIL
    #     return comment

    # def calculate_gpa(self, total_unit_in_semester):
    #     current_semester = Semester.objects.get(is_current_semester=True)
    #     student = TakenCourse.objects.filter(student=self.student, course__level=self.student.level,
    #                                          course__semester=current_semester)
    #     p = 0
    #     point = 0
    #     for i in student:
    #         courseUnit = i.course.courseUnit
    #         if i.grade == A:
    #             point = 5
    #         elif i.grade == B:
    #             point = 4
    #         elif i.grade == C:
    #             point = 3
    #         elif i.grade == D:
    #             point = 2
    #         else:
    #             point = 0
    #         p += int(courseUnit) * point
    #     try:
    #         gpa = (p / total_unit_in_semester)
    #         return round(gpa, 1)
    #     except ZeroDivisionError:
    #         return 0

    # def calculate_cgpa(self):
    #     current_semester = Semester.objects.get(is_current_semester=True)
    #     previousResult = Result.objects.filter(student__id=self.student.id, level__lt=self.student.level)
    #     previousCGPA = 0
    #     for i in previousResult:
    #         if i.cgpa is not None:
    #             previousCGPA += i.cgpa
    #     cgpa = 0
    #     if str(current_semester) == SECOND:
    #         try:
    #             first_sem_gpa = Result.objects.get(student=self.student.id, semester=FIRST, level=self.student.level)
    #             first_sem_gpa += first_sem_gpa.gpa.gpa
    #         except:
    #             first_sem_gpa = 0

    #         try:
    #             sec_sem_gpa = Result.objects.get(student=self.student.id, semester=SECOND, level=self.student.level)
    #             sec_sem_gpa += sec_sem_gpa.gpa
    #         except:
    #             sec_sem_gpa = 0

    #         taken_courses = TakenCourse.objects.filter(student=self.student, student__level=self.student.level)
    #         TCU = 0
    #         for i in taken_courses:
    #             TCU += int(i.course.courseUnit)
    #         cpga = first_sem_gpa + sec_sem_gpa / TCU

    #         return round(cgpa, 2)
            


class FinalResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,)
    # written_assessment = models.ForeignKey(WrittenAssessment, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    total = models.FloatField(blank=True, editable=False, null=True, help_text='Adds All Assessments For the Current Semester')
    grade = models.CharField(choices=GRADE, editable=False, max_length=1, blank=True)
    comment = models.CharField(choices=COMMENT, editable=False, max_length=200, blank=True)
    

    # def get_total(self):
    #     # initialize final_score
    #     final_score = 0
        
    #     # get current semester
    #     try:
    #         current_semester = Semester.objects.get(is_current_semester=True)
    #     except Semester.DoesNotExist:
    #         return HttpResponseNotFound('Semester does not exist, contact support for help.')
    #     # get wriiten assessments for the student in the provided course for the current semester
    #     written_assessments = WrittenAssessment.objects.filter(student__user=self.student.user, assessment__course=self.course, semester=current_semester)
        
        # for wa in written_assessments:
        #     final_score =+ wa.score
        # return final_score

        # get final results for the student in the provided course for the current semester
        # try:
        #     final_results = FinalResult.objects.get(student=self.student, course=self.course, semester=current_semester)
        #     print('FINAL RESULT: %s' % final_results)
        #     for wa in written_assessments:
        #         if wa.student.user == final_results.student.user and wa.assessment.course == final_results.course and wa.semester == final_results.semester:
        #             final_score =+ wa.score
        #     # return final_score
        #     final_results.total = final_score
        #     final_results.save()
           
        # except FinalResult.DoesNotExist:
        #     for wa in written_assessments:
        #         final_score =+ wa.score
        #     return final_score

        # if final_results:
        #     for fa in final_results:
        #         for wa in written_assessments:
        #             final_results.total =+ wa.score
        #     final_results.save()
        
        # else:
        #     for wa in written_assessments:
        #         final_score =+ wa.score
        #     return final_score

    # def get_grade(self, written_assessment):
    #     for wa in written_assessment:
    #         final_score =+ wa.score 
            
    #     if final_score >= 70:
    #         grade = A
    #     elif final_score >= 60:
    #         grade = B
    #     elif final_score >= 50:
    #         grade = C
    #     elif final_score >= 45:
    #         grade = D
    #     else:
    #         grade = F
    #     return grade

    # def get_comment(self, grade):
    #     if not grade == "F":
    #         comment = PASS
    #     else:
    #         comment = FAIL
    #     return comment
    
    # Finally override the default save method
    # def save(self, *args, **kwargs):
    #     # Add custom logic here
    #     self.total = self.get_total()
    #     # self.grade = self.get_grade(self.written_assessment)
    #     # self.comment = self.get_comment(self.get_grade(self.written_assessment))
    #     super(FinalResult, self).save(*args, **kwargs)


class PaymentType(models.Model):
    payment_type_name = models.CharField('Payment Type', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Payment Type'
        verbose_name_plural = 'Payment Type'

    def __str__(self):
        return self.payment_type_name


class PaymentStructure(models.Model):
    program = models.ForeignKey(Program, verbose_name='Program', default='', on_delete=models.CASCADE)
    semester = models.CharField(verbose_name='Semester', max_length=200, null=True, choices=SEMESTER)
    payment_level = models.ForeignKey(Level, verbose_name='Year', default='', on_delete=models.CASCADE)
    amount_to_be_paid = models.DecimalField(verbose_name='Amount To Be Paid', max_digits=20, decimal_places=2, default=0)
    payment_description = models.ForeignKey(PaymentType, verbose_name='Payment Type', help_text='payment for?', default='', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Payment Structure'
        verbose_name_plural = 'Payment Structure'

    def __str__(self):
        return 'Type: ' + self.payment_description.payment_type_name + ', Amount: ' + str(self.amount_to_be_paid) + ', Level: ' + str(self.payment_level)


class Payment(models.Model):
    semester = models.ForeignKey(Semester, default='', blank=True, null=True,
                                 verbose_name='Academic Session', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name='Student Name', null=True, blank=True, on_delete=models.CASCADE)
    paymentstructure = models.ForeignKey(PaymentStructure, verbose_name='Payment Structure', null=True, blank=True,
                                  on_delete=models.CASCADE)
    amountpaid = models.DecimalField(verbose_name='Total Amount Paid', max_digits=20, decimal_places=2, default=0)
    actualamountpaid = models.DecimalField(verbose_name='Actual Amount Paid', max_digits=20, decimal_places=2,
                                           default=0, editable=False)
    balance = models.DecimalField(verbose_name='Balance', max_digits=20, decimal_places=2, default=0, editable=False)
    paymentstatus = models.CharField(max_length=30, default='Fully Paid', blank=True, null=True, editable=False)
    paymentdate = models.DateField('Payment Date', auto_now=True)
    total_amount_to_be_paid = models.DecimalField('Total Amount To Be Paid', max_digits=20, decimal_places=2, default=0, editable=False)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def save(self, **kwargs):

        if not self.id:
            payment = Payment.objects.filter(student__user_id=self.student.user.id).order_by('-id')[:1]
            actual_amount_to_be_paid = self.paymentstructure.amount_to_be_paid
            self.actualamountpaid = self.amountpaid
            amountEntered = decimal.Decimal(self.amountpaid)

            if payment:

                for f in payment:
                    print("")
                    print("SESSION: ", f.semester, "TOTAL: ", f.total_amount_to_be_paid, ", PAID: ", f.amountpaid)

                    # check if student over paid
                    if f.semester != self.semester and f.balance < 0:
                        print("FIRST IF STATEMENT:::::")
                        self.amountpaid = decimal.Decimal(self.amountpaid) + (f.amountpaid - f.total_amount_to_be_paid)
                        paid = self.amountpaid
                        self.balance = actual_amount_to_be_paid - paid
                        self.total_amount_to_be_paid = actual_amount_to_be_paid

                    # check if student under paid
                    if f.semester != self.semester and f.balance >= 0:
                        print("SECOND IF STATEMENT:::::")
                        self.amountpaid = decimal.Decimal(self.amountpaid) - f.balance
                        paid = decimal.Decimal(self.amountpaid)
                        self.balance = actual_amount_to_be_paid - paid
                        self.total_amount_to_be_paid = actual_amount_to_be_paid

                    # if f.academicsession == self.academicsession and actualfees > f.amountpaid > 0:
                    #     print("THIRD IF STATEMENT:::::")
                    #     self.amountpaid = decimal.Decimal(self.amountpaid) + f.amountpaid
                    #     paid = decimal.Decimal(self.amountpaid)
                    #     self.balance = actualfees - paid
                    #     self.total = actualfees

                    if f.semester == self.semester and f.balance >= 0:
                        print("FOURTH IF STATEMENT:::::")
                        self.amountpaid = decimal.Decimal(self.amountpaid) + f.amountpaid
                        # paid = decimal.Decimal(self.amountpaid)
                        self.balance = f.balance - amountEntered
                        self.total_amount_to_be_paid = actual_amount_to_be_paid

                    if f.semester == self.semester and f.balance < 0:
                        print("FIFTH IF STATEMENT:::::")
                        self.amountpaid = decimal.Decimal(self.amountpaid) + f.amountpaid
                        # paid = decimal.Decimal(self.amountpaid)
                        self.balance = f.balance - amountEntered
                        self.total_amount_to_be_paid = actual_amount_to_be_paid

            else:
                self.balance = actual_amount_to_be_paid - decimal.Decimal(self.amountpaid)
                self.total_amount_to_be_paid = actual_amount_to_be_paid

            if self.balance > 0:
                self.paymentstatus = 'Got Balance'

            # activate the user upon subscription
            # u = User.objects.get(pk=self.user.pk)
            # u.is_active = True
            # u.save(force_update=u.is_active)

            super(Payment, self).save()

    def __str__(self):
        return str(self.student) + ' - ' + str(self.amountpaid)

    
