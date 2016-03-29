from django.contrib import admin
from .models import Problem, ProblemData
from guardian.admin import GuardedModelAdmin


class ProblemAdmin(GuardedModelAdmin):
    pass


#  admin.site.register(Problem)
admin.site.register(ProblemData)
admin.site.register(Problem, ProblemAdmin)
