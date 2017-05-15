from django.utils.translation import ugettext_lazy as _


class EnumChoice(object):

    def __init__(self, *args):
        for x in args:
            if not isinstance(x, tuple) or len(x) != 2:
                raise Exception("Args Error")
        self.pairs = args
        self._pairs = dict(self.pairs)
        self._rpairs = dict([(k, v) for k, v in self.pairs])

    def __getattr__(self, item):
        if self._rpairs.has_key(item):
            return self._rpairs[item]
        return None

    def choice(self):
        return self.pairs

    def filter_choice(self):
        res = [('', 'All')]
        res.extend(list(self.pairs))
        return res

    def to_dict(self):
        if not self.pairs or len(self.pairs) == 0:
            return {}
        if self._pairs:
            return self._pairs
        self._pairs = dict(self.pairs)
        return self._pairs

    def keys(self):
        return [k for k, v in self.pairs]

    def values(self):
        return [v for k, v in self.pairs]

    def get_display_name(self, key):
        if not self.pairs:
            return None
        return self.to_dict().get(key, None)

LANGUAGE = EnumChoice(
    ('CPP03', 'GNU C++'),
    ('C', 'GNU C'),
    ('JAVA8', 'JAVA 8'),
    ('CPP11', 'GNU C++ 11'),
    ('CPP14', 'GNU C++ 14'),
    ('PY2', 'Python 2.7'),
    ('PY3', 'Python 3.5'),
    ('NASM', 'Assembly 32bit'),
    ('NASM64', 'Assembly 64bit'),
    ('PAS', 'Pascal')
)

LANGUAGE_MASK = EnumChoice(
    (1, 'CPP03'),
    (2, 'C'),
    (4, 'JAVA8'),
    (8, 'CPP11'),
    (16, 'CPP14'),
    (32, 'PY2'),
    (64, 'PY3'),
    (128, 'NASM'),
    (256, 'NASM64'),
    (512, 'PAS')
)

CONTEST_TYPE = EnumChoice(
    (0, 'ICPC'),
    (1, 'OI')
)

GENDER = EnumChoice(
    ('S', _('Secret')),
    ('F', _('Female')),
    ('M', _('Male'))
)

STATUS_CODE = EnumChoice(
    ('PD', 'Pending'),
    ('SE', 'System Error'),
    ('CL', 'Compiling'),
    ('CE', 'Compilation Error'),
    ('JD', 'Judging'),
    ('AC', 'Accepted'),
    ('PE', 'Presentation Error'),
    ('IR', 'Invalid Return'),
    ('WA', 'Wrong Answer'),
    ('RE', 'Runtime Error'),
    ('TLE', 'Time Limit Exceed'),
    ('MLE', 'Memory Limit Exceed'),
    ('OLE', 'Output Limit Exceed'),
    ('IE', 'Internal Error'),
)
PROBLEM_TITLE_LENGTH = 64
PROBLEM_MAX_LEN_DESC = 32768
PROBLEM_MAX_LEN_CODE = 65536
PROBLEM_DEFAULT_RUNNING_MEMORY = 65536
PROBLEM_DEFAULT_RUNNING_TIME = 1000
CONTEST_CACHE_EXPIRE_TIME = 5 * 60 * 60
CONTEST_CACHE_FLUSH_TIME = 5
