from django.contrib import admin
from .models import Problem, ProblemDataInfo, Language, Submission
from guardian.admin import GuardedModelAdmin


class ProblemAdmin(GuardedModelAdmin):
    pass

admin.site.register(Language)
admin.site.register(ProblemDataInfo)
admin.site.register(Submission)
admin.site.register(Problem, ProblemAdmin)
