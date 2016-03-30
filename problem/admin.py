from django.contrib import admin
from .models import Problem, ProblemData, Language, Submission
from guardian.admin import GuardedModelAdmin


class ProblemAdmin(GuardedModelAdmin):
    pass


#  admin.site.register(Problem)
admin.site.register(Language)
admin.site.register(ProblemData)
admin.site.register(Submission)
admin.site.register(Problem, ProblemAdmin)
