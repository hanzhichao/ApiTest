from django.contrib import admin
from app.models import *

admin.site.site_header = 'ApiTest后台管理系统'
admin.site.site_title = 'ApiTest后台管理系统'


class ApiAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'url', 'method', 'data_type', 'description')
    search_fields = ('name', 'project', 'url')
    list_filter = ('project', 'method', 'data_type')
    # list_editable = ['description',]
    ordering = ('project', 'name')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'developer', 'description')
    search_fields = ('name', 'developer')
    list_filter = ('developer',)


# class ProjectEnvAdmin(admin.ModelAdmin):
#     list_display = ('env', 'project', 'url', 'sign', 'access_id', 'access_key', 'description')
#     search_fields = ('env', 'project', 'url')
#     list_filter = ('env', 'project', 'sign', 'access_id', 'access_key')


class ProjectEnvInline(admin.TabularInline):  # admin.StackedInline
    model = ProjectEnv


class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [ProjectEnvInline]


class SignAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


# class StepAdmin(admin.ModelAdmin):
#     list_display = ('case', 'api', 'data', 'assertion')
#     search_fields = ('case', 'api')
#     list_filter = ('case', 'api')


class StepInline(admin.TabularInline):  # admin.StackedInline
    model = Step


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan', 'description')
    search_fields = ('name', 'plan')
    list_filter = ('plan',)
    inlines = [StepInline]


class TestPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'environment', 'description')
    search_fields = ('name', 'environment')
    list_filter = ('environment',)


# class TestReportAdmin(admin.ModelAdmin):
#     list_display = ('name', 'test_plan', 'case_num', 'pass_num', 'fail_num', 'error_num', 'description')
#     search_fields = ('name', 'test_plan')
#     list_filter = ('test_plan',)


# class TestCaseResultAdmin(admin.ModelAdmin):
#     list_display = ('api', 'test_plan', 'report', 'status')
#     search_fields = ('api', 'test_plan', 'report', 'status')
#     list_filter = ('api', 'test_plan', 'report', 'status')


admin.site.register(Api, ApiAdmin)
admin.site.register(Sign, SignAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestPlan, TestPlanAdmin)


# admin.site.register(ProjectEnv, ProjectEnvAdmin)
# admin.site.register(Step, StepAdmin)
# admin.site.register(TestCaseResult, TestCaseResultAdmin)
# admin.site.register(TestReport, TestReportAdmin)




