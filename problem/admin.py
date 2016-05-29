from django.contrib import admin
from .models import Problem, ProblemDataInfo
from guardian.admin import GuardedModelAdmin


class ProblemAdmin(GuardedModelAdmin):
    pass

admin.site.register(ProblemDataInfo)
admin.site.register(Problem, ProblemAdmin)
