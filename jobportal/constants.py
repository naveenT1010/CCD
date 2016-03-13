"""
Choices for model fields
"""
SEX = (
    ('M', 'Male'),
    ('F', 'Female'),
)

BOOL_CHOICES = (
    ('True', 'YES'),
    ('False', 'No')
)

JOB_AUDIENCE = (
    ('BTECH1', 'B. Tech 1st Year'),
    ('BTECH2', 'B. Tech 2nd Year'),
    ('BTECH3', 'B. Tech 3rd Year'),
    ('BTECH4', 'B. Tech 4th Year'),
    ('MTECH1', 'B. Tech 1st Year'),
    ('MTECH2', 'B. Tech 2nd Year'),
    ('PHD', 'Ph.D.'),
    ('ALUM', 'Alumni'),
)

CATEGORY = (
    ('GEN', 'GEN'),
    ('OBC', 'OBC'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('PH', 'PH'),
    ('Foreign', 'Foreign')
)

USER_CATEGORY = (
    ('Current Student', 'Current Student'),
    ('Alumni', 'Alumni'),
    ('Company', 'Company'),
    ('Admin', 'Admin')
)

DEPARTMENTS = (
    ('BT', 'Biotechnology[BT]'),
    ('CL', 'Chemical[CL]'),
    ('CHE', 'Chemistry[CHE]'),
    ('CE', 'Civil[CE]'),
    ('CSE', 'Computer Science[CSE]'),
    ('DD', 'Design[DD]'),
    ('EEE', 'Electrical[EEE]'),
    ('ECE', 'Electronics[ECE]'),
    ('HSS', 'Humanities & Social Sciences[HSS]'),
    ('MA', 'Mathematics[MA]'),
    ('ME', 'Mechanical[ME]'),
    ('EP', 'Physics[EP]'),
)

DEPARTMENTS_JOBCHOICE = DEPARTMENTS + (('ALL', 'All Departments'),)

CV_REQUIRED = (
    ('CV1', 'CV1'),
    ('CV2', 'CV2'),
    ('CV12', 'CV12')
)

PROGRAMMES = (
    ('BTECH', 'B.Tech.'),
    ('MTECH', 'M.Tech.'),
    ('PHD', 'Ph.D.'),
)

HOSTELS = (
    ('Barak', 'Barak'),
    ('Brahmaputra', 'Brahmaputra'),
    ('Dhansiri', 'Dhansiri'),
    ('Dibang', 'Dibang'),
    ('Dihing', 'Dihing'),
    ('Kameng', 'Kameng'),
    ('Kapili', 'Kapili'),
    ('Lohit', 'Lohit'),
    ('Manas', 'Manas'),
    ("Married Scholar's Hostel", "Married Scholar's Hostel"),
    ('Siang', 'Siang'),
    ('Subansiri', 'Subansiri'),
    ('Umiam', 'Umiam'),
    ('Other', 'Other'),
)

JOB_TYPE = (
    ('Internship', 'Internship'),
    ('Full Time', 'Full Time'),
)

CURRENT_YEAR = (
    ('1', 'FIRST'),
    ('2', 'SECOND'),
    ('3', 'THIRD'),
    ('4', 'FOURTH')
)

ORGANIZATION_TYPE = (
    ('Private', 'Private'),
    ('Government', 'Government'),
    ('PSU', 'PSU'),
    ('MNC(Indian Origin)', 'MNC(Indian Origin)'),
    ('MNC(Foreign Origin)', 'MNC(Foreign Origin)'),
    ('NGO', 'NGO'),
    ('Other', 'Other')

)

INDUSTRY_SECTOR = (
    ('Core Engg', 'Core Engg'),
    ('IT', 'IT'),
    ('Analytics', 'Analytics'),
    ('Management', 'Management'),
    ('Finance', 'Finance'),
    ('Education', 'Education'),
    ('Consulting', 'Consulting'),
    ('R&D', 'R&D'),
    ('Oil and Gas', 'Oil and Gas'),
    ('Ecommerce', 'Ecommerce'),
    ('FMCG', 'FMCG'),
    ('Manufacturing', 'Manufacturing'),
    ('Telecom', 'Telecom'),
    ('Other', 'Other')
)