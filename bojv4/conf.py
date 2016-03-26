from django.utils.translation import ugettext_lazy as _
class CONST():
    LANGUAGE = (
        ( 'g++', 'GNU C++'),
        ( 'gcc', 'GNU C'),
        ( 'java', 'java'),
        ( 'g+11', 'GNU C++ 11'),
    )

    GENDER = (
        ( 'S', _('Secret')),
        ( 'F', _('Female')),
        ( 'M', _('Male')),
    )
    STATUS_CODE = (
        ( 'PD', 'Pending'),
        ( 'SE', 'System Error'),
        ( 'CL', 'Compiling'),
        ( 'CE', 'Compilation Error'),
        ( 'JD', 'Judging'),
        ( 'AC', 'Accepted'),
        ( 'PE', 'Presentation Error'),
        ( 'WA', 'Wrong Answer'),
        ( 'RE', 'Runtime Error'),
        ( 'TLE', 'Time Limit Exceed'),
        ( 'MLE', 'Memory Limit Exceed'),
        ( 'OLE', 'Output Limit Exceed'),
        ( 'EXT', 'Extended Judge Result'),
        ( 'NUM', 'Judge Score'),
    )
    PROBLEM_TITLE_LENGTH = 64
    PROBLEM_MAX_LEN_DESC = 32768
    PROBLEM_MAX_LEN_CODE = 65536
    PROBLEM_DEFAULT_RUNNING_MEMORY = 65536
    PROBLEM_DEFAULT_RUNNING_TIME = 1000
