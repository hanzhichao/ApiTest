from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    
    path('', index, name='index'),

    path('project/', prj_list, name='prj_list'),
    path('project/add/', prj_add, name='prj_add'),
    path('project/update/<int:prj_id>/', prj_update, name='prj_update'),
    path('project/del/<int:prj_id>/', prj_del, name='prj_del'),

    path('env/', env_list, name='env_list'),
    path('env/add/', env_add, name='env_add'),
    path('env/update/<int:env_id>/', env_update, name='env_update'),
    path('env/del/<int:env_id>/', env_del, name='env_del'),

    path('prj_env/', prj_env_list, name='prj_env_list'),
    path('prj_env/add/', prj_env_add, name='prj_env_add'),
    path('prj_env/update/<int:prj_env_id>/', prj_env_update, name='prj_env_update'),
    path('prj_env/del/<int:prj_env_id>/', prj_env_del, name='prj_env_del'),

    path('api/', api_list, name='api_list'),
    path('api/add/', api_add, name='api_add'),
    path('api/update/<int:api_id>/', api_update, name='api_update'),
    path('api/test/', api_test, name='api_test'),
    path('api/test/<int:api_id>/', api_test, name='api_test'),
    path('api/del/<int:api_id>/', api_del, name='api_del'),
    path('api_of_project/', api_of_project, name='api_of_project'),

    path('save_steps/', save_steps, name='save_steps'),

    path('case/', case_list, name='case_list'),
    path('case/add/', case_add, name='case_add'),
    path('case/update/<int:case_id>/', case_update, name='case_update'),
    path('case/del/<int:case_id>/', case_del, name='case_del'),

    path('plan/', plan_list, name='plan_list'),
    path('plan/add/', plan_add, name='plan_add'),
    path('plan/update/<int:plan_id>/', plan_update, name='plan_update'),
    path('plan/run/', plan_run, name='plan_run'),
    path('plan/del/<int:plan_id>/', plan_report, name='plan_report'),
    path('plan/del/<int:plan_id>/', plan_del, name='plan_del'),

    path('report/', report_list, name='report_list'),
    path('report/detail/<int:report_id>/', report_detail, name='report_detail'),
    path('report/del/<int:report_id>/', report_del, name='report_del'),

    path('sign/', sign_list, name='sign_list'),
    path('sign/detail/<int:sign_id>/', sign_detail, name='sign_detail'),
    path('sign/del/<int:sign_id>/', sign_del, name='sign_del'),


]
