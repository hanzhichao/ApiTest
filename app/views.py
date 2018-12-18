from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
import hashlib
import re
from app import sign
import requests
from django.views.decorators.csrf import csrf_exempt


# 登录操作 -----------------------------------------------------------------------------------------
def user_login(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                msg = '账户不可用'
        else:
            msg = '登录失败'
    
    return render(request, "login.html", {'msg': msg})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# 首页 -----------------------------------------------------------------------------------------
@login_required
def index(request):
    prj_num = len(Project.objects.all())
    api_num = len(Api.objects.all())
    plan_num = len(TestPlan.objects.all())
    case_num = len(TestCase.objects.all())
    
    return render(request, "index.html", {"prj_num": prj_num, "api_num": api_num, "plan_num": plan_num,
                                          "case_num": case_num})


# 项目操作 -----------------------------------------------------------------------------------------
@login_required
def prj_list(request):
    prj_list = Project.objects.all()
    return render(request, "project_list.html", {"prj_list": prj_list})


@login_required
def prj_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Project.objects.filter(name=name):
            messages.error(request, "项目已存在")
        else:
            description = request.POST.get('description')
            developer = request.POST.get('developer')
            prj = Project(name=name, developer=developer, description=description)
            prj.save()
            return HttpResponseRedirect('/project/')
    return render(request, "project_add.html")


@login_required
def prj_update(request, prj_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        developer = request.POST.get('developer')
        Project.objects.filter(id=prj_id).update(name=name, is_sign=is_sign, developer=developer, description=description)
        return HttpResponseRedirect('/project/')
    prj = get_object_or_404(Project, id=prj_id)
    return render(request, "project_update.html", {"prj": prj})


@login_required
def prj_del(request, prj_id):
    Project.objects.filter(id=prj_id).delete()
    return HttpResponseRedirect('/project/')


# 环境操作 -----------------------------------------------------------------------------------------
@login_required
def env_list(request):   # project_list
    env_list = Environment.objects.all()
    return render(request, "env_list.html", {"env_list": env_list})


@login_required
def env_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        env = Environment(name=name, description=description)
        env.save()
        return HttpResponseRedirect('/env/')
    return render(request, "env_add.html", {'prj_list': prj_list})


@login_required
def env_update(request, env_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Environment.objects.filter(id=env_id).update(name=name, description=description)
        return HttpResponseRedirect('/env/')
    env = get_object_or_404(Environment, id=env_id)
    return render(request, "env_update.html", {"env": env, 'prj_list': prj_list})


@login_required
def env_del(request, env_id):
    if request.method == 'GET':
        Environment.objects.filter(id=env_id).delete()
        return HttpResponseRedirect('/env/')



# 项目环境操作 -----------------------------------------------------------------------------------------
@login_required
def prj_env_list(request):   # project_list
    prj_env_list = ProjectEnv.objects.all()
    return render(request, "prj_env_list.html", {"prj_env_list": prj_env_list})


@login_required
def prj_env_add(request):
    if request.method == 'POST':
        env = get_object_or_404(Environment, id=request.POST.get('env_id'))
        project = get_object_or_404(Project, id=request.POST.get('prj_id'))
        sign = get_object_or_404(Sign, id=request.POST.get('sign_id'))
        url = request.POST.get('url')
        access_id = request.POST.get('access_id')
        access_key = request.POST.get('access_key')
        description = request.POST.get('description')
        prj_env = ProjectEnv(env=env, project=project, sign=sign, url=url, access_id=access_id,
                          access_key=access_key)
        prj_env.save()
        return HttpResponseRedirect('/prj_env/')
    prj_list = Project.objects.all()
    env_list = Environment.objects.all()
    sign_list = Sign.objects.all()
    return render(request, "prj_env_add.html", {'prj_list': prj_list, 'env_list': env_list, 'sign_list': sign_list})


@login_required
def prj_env_update(request, prj_env_id):
    if request.method == 'POST':
        env = get_object_or_404(Environment, id=request.POST.get('env_id'))
        project = get_object_or_404(Project, id=request.POST.get('prj_id'))
        sign = get_object_or_404(Sign, id=request.POST.get('sign_id'))
        url = request.POST.get('url')
        access_id = request.POST.get('access_id')
        access_key = request.POST.get('access_key')
        description = request.POST.get('description')
        ProjectEnv.objects.filter(id=prj_env_id).update(env=env, project=project, sign=sign, url=url, access_id=access_id,
                                                     access_key=access_key)
        return HttpResponseRedirect('/prj_env/')
    prj_env = get_object_or_404(ProjectEnv, id=prj_env_id)
    env_list = Environment.objects.all()
    prj_list = Project.objects.all()
    sign_list = Sign.objects.all()
    return render(request, "prj_env_update.html", {"prj_env": prj_env, 'prj_list': prj_list, 'env_list': env_list, 'sign_list': sign_list})


@login_required
def prj_env_del(request, prj_env_id):
    if request.method == 'GET':
        ProjectEnv.objects.filter(id=prj_env_id).delete()
        return HttpResponseRedirect('/prj_env/')


# 接口操作 -----------------------------------------------------------------------------------------
@login_required
def api_list(request):   # project_list
    api_list = Api.objects.all()
    env_list = Environment.objects.all()
    return render(request, "api_list.html", {"api_list": api_list, "env_list": env_list})


@login_required
def api_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        project = get_object_or_404(Project, id=request.POST.get('prj_id'))
        url = request.POST.get('url')
        method = request.POST.get('method')
        data_type = request.POST.get('data_type')
        description = request.POST.get('description')
        request_header = request.POST.get('request_header')
        request_body = request.POST.get('request_body')
        response_header = request.POST.get('response_header')
        response_body = request.POST.get('response_body')
        api = Api(name=name, project=project, url=url, method=method, data_type=data_type, 
                  description=description,  request_body=request_body,
                  response_body=response_body)
        api.save()
        return HttpResponseRedirect('/api/')
    prj_list = Project.objects.all()
    env_list = Environment.objects.all()
    return render(request, "api_add.html", {'prj_list': prj_list, 'env_list': env_list})


@login_required
def api_update(request, api_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        project = get_object_or_404(Project, id=request.POST.get('prj_id'))
        url = request.POST.get('url')
        method = request.POST.get('method')
        data_type = request.POST.get('data_type')
        description = request.POST.get('description')
        request_header = request.POST.get('request_header')
        request_body = request.POST.get('request_body')
        response_header = request.POST.get('response_header')
        response_body = request.POST.get('response_body')
        Api.objects.filter(id=api_id).update(name=name, project=project, url=url, method=method, data_type=data_type, 
                  description=description, request_body=request_body,
                  response_body=response_body)
        return HttpResponseRedirect('/api/')
    api = get_object_or_404(Api, id=api_id)
    prj_list = Project.objects.all()
    env_list = Environment.objects.all()
    return render(request, "api_update.html", {"api": api, 'prj_list': prj_list, 'env_list': env_list})


@login_required
@csrf_exempt
def api_test(request, api_id=None):
    env_id = request.POST.get('env_id')

    if not api_id:
        prj_id = request.POST.get('prj_id')
        url = request.POST.get('url')
        method = request.POST.get('method')
        data_type = request.POST.get('data_type')
        request_body = request.POST.get('request_body')
    else:
        api = get_object_or_404(Api, id=api_id)
        prj_id = str(api.project.id)
        url = api.url
        method = str(api.method)
        data_type = str(api.data_type)
        request_body = api.request_body

    project_env = get_object_or_404(ProjectEnv, env=env_id, project=prj_id)
    base_url = project_env.url
    access_id = project_env.access_id
    access_key = project_env.access_key
    sign_content = project_env.sign.content

    url = url if url.startswith("/") else "/" + url
    url = base_url + url
    try:
        data = json.loads(request_body)
    except Exception as e:
        return HttpResponse('请求数据, json格式有误')
        

    # 处理签名
    if sign_content:
        exec(sign_content)


    if method == '1':
        print("post请求")
        if data_type == '1':
            resp = requests.post(url=url, json=data)
        else:
            resp = requests.post(url=url, data=data)
    else:
        resp = requests.get(url=url)
        
    try:
        result = json.dumps(resp.json(), ensure_ascii=False, indent=2)
    except Exception as e:
        result = resp.text
    return HttpResponse(result)


@login_required
def api_del(request, api_id):
    if request.method == 'GET':
        Api.objects.filter(id=api_id).delete()
        return HttpResponseRedirect('/api/')


@login_required
@csrf_exempt
def api_of_project(request):
    prj_id = request.GET.get('prj_id')
    api_list = Api.objects.filter(project=prj_id)
    resp = []
    for api in api_list:
        resp.append((api.id, api.name))
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 步骤操作 -----------------------------------------------------------------------------------------
@login_required
@csrf_exempt
def save_steps(request):
    if request.method == 'POST':
        case_id = request.GET.get('case_id')
       
        if case_id:
            case = get_object_or_404(TestCase, id=case_id)
        else:
            case = TestCase(name='tmp_case')
            case.save()
        steps = json.loads(request.body)
        step_remains = []
        for step in steps:
            api=get_object_or_404(Api, id=int(step.get('api_id')))
            step_id = step.get('step_id')
            if step_id:
                step_remains.append(step_id) 
                Step.objects.filter(id=step_id).update(sn=step.get('sn'), data=step.get('data'), assertion=step.get('assertion'))
            else:
                new_step= Step(case=case, sn=step.get('sn'), api=api, data=step.get('data'), assertion=step.get('assertion'))
                new_step.save()
                step_remains.append(new_step.id) 

            # remove steps not remains
        Step.objects.exclude(id__in=step_remains).delete()
        return HttpResponse(json.dumps({"case_id": case.id}), content_type="application/json")


# 用例操作 -----------------------------------------------------------------------------------------
@login_required
def case_list(request):   # project_list
    case_list = TestCase.objects.all()
    env_list = Environment.objects.all()
    return render(request, "case_list.html", {"case_list": case_list, 'env_list': env_list})


@login_required
def case_add(request):
    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        plan = get_object_or_404(TestPlan, id=request.POST.get('plan_id'))
        TestCase.objects.filter(id=case_id).update(name=name, description=description, plan=plan)
        return HttpResponseRedirect('/case/')
    api_list = Api.objects.all()
    prj_list = Project.objects.all()
    plan_list = TestPlan.objects.all()
    env_list = Environment.objects.all()
    return render(request, "case_add.html", {'api_list': api_list, 'prj_list': prj_list, 'plan_list': plan_list, 'env_list': env_list})


@login_required
def case_update(request, case_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        plan = get_object_or_404(TestPlan, id=request.POST.get('plan_id'))
        TestCase.objects.filter(id=case_id).update(name=name, description=description, plan=plan)
        return HttpResponseRedirect('/case/')
    case = get_object_or_404(TestCase, id=case_id)
    api_list = Api.objects.all()
    plan_list = TestPlan.objects.all()
    step_list = case.step_set.all()
    env_list = Environment.objects.all()
    prj_list = Project.objects.all()
    return render(request, "case_update.html", {"case": case, 'api_list': api_list, 'plan_list': plan_list, 'step_list': step_list, 'env_list': env_list, 'prj_list': prj_list})


@login_required
def case_test(request, case_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        apis = Api.objects.filter(id__in=request.POST.getlist('apis'))
        description = request.POST.get('description')
        content = request.POST.get('content')
        case = get_object_or_404(TestCase, id=case_id)
        case.name=name
        case.description=description
        case.content=content
        case.apis.clear()
        for api in apis:
            case.apis.add(api)
        case.save()
        return HttpResponseRedirect('/case/')
    case = get_object_or_404(TestCase, id=case_id)
    api_list = Api.objects.all()
    return render(request, "case_test.html", {"case": case, 'api_list': api_list})


@login_required
def case_del(request, case_id):
    if request.method == 'GET':
        TestCase.objects.filter(id=case_id).delete()
        return HttpResponseRedirect('/case/')


# 测试计划操作 -----------------------------------------------------------------------------------------
@login_required
def plan_list(request):   # project_list
    plan_list = TestPlan.objects.all()
    case_list = TestCase.objects.all()
    return render(request, "plan_list.html", {"plan_list": plan_list, 'case_list': case_list})


@login_required
def plan_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        env = get_object_or_404(Environment, id=request.POST.get('env_id'))
        description = request.POST.get('description')
        plan = TestPlan(name=name, environment=env, description=description)
        plan.save()
        return HttpResponseRedirect('/plan/')
    case_list = TestCase.objects.all()
    env_list = Environment.objects.all()
    return render(request, "plan_add.html", {'case_list': case_list, 'env_list': env_list})


@login_required
def plan_update(request, plan_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        env = get_object_or_404(Environment, id=request.POST.get('env_id'))
        description = request.POST.get('description')
        plan = get_object_or_404(TestPlan, id=plan_id)
        plan.name = name
        plan.environment = env
        plan.description = description
        plan.test_cases.clear()
        return HttpResponseRedirect('/plan/')
    
    plan = get_object_or_404(TestPlan, id=plan_id)
    env_list = Environment.objects.all()
    case_list = TestCase.objects.all()
    return render(request, "plan_update.html", {"plan": plan, 'case_list': case_list, 'env_list': env_list})

# @login_required
@csrf_exempt
def plan_run(request):
    plan_id = request.GET.get('plan_id')
    plan = get_object_or_404(TestPlan, id=plan_id)
    env = get_object_or_404(Environment, id=plan.environment.id)
    
    cases = plan.testcase_set.all()

    plan_result = []
    case_num=len(cases)
    pass_num = 0
    fail_num = 0
    error_num = 0

    test_report = TestReport(test_plan=plan)
    test_report.save()

    for case in cases:
        case_result = {"steps":[], "result": "PASS"}
        test_case_result = TestCaseResult(report=test_report, case=case, status="PASS")
        test_case_result.save()

        for step in case.step_set.all():
            step_api = get_object_or_404(Api, id=step.api.id)
            step_data = step.data
            if step.assertion:
                step_assertion = step.assertion.split('\n')
            else:
                step_assertion = []
            
            project_env = get_object_or_404(ProjectEnv, env=env.id, project=step_api.project.id)
            base_url = project_env.url
            access_id = project_env.access_id
            access_key = project_env.access_key
            sign_content = project_env.sign.content

            url = step_api.url
            request_body = step_api.request_body
            data_type = step_api.data_type
            method = step_api.method

            url = url if url.startswith("/") else "/" + url
            url = base_url + url
            data = json.loads(request_body)
            
            if step_data:
                try:
                    step_data=json.loads(step_data)
                    data.update(step_data)
                except json.decoder.JSONDecodeError:
                    return HttpResponse('json格式错误, 请求数据: %s' % step_data)

            # 处理签名
            if sign_content:
                exec(sign_content)

            print("-----------------------------------------------")
            print(method, type(method))
            print(url)
            print(data)
            if method == 1:
                print("post请求")
                print(data_type, type(data_type))
                if data_type == 1:
                    resp = requests.post(url=url, json=data)
                else:
                    resp = requests.post(url=url, data=data)
            else:
                resp = requests.get(url=url)
    
            api_response = resp.text
            print(resp.text)

            # 结果断言
            status = "PASS"
            if step_assertion:
                print("=============")
                print(step_assertion)
                for assertion in step_assertion:
                    try:
                        assert eval(assertion)
                    except AssertionError:
                        status = 'FAIL'
                        case_result['result'] = status
                    except Exception as e:
                        status = 'ERROR'
                        case_result['result'] = status
                        api_response = repr(e)
                
            case_result["steps"].append({"api_name": step_api.name, "api_url": url, "api_data": data, "api_response": api_response, "api_result": status})
            step_result = StepResult(test_case_result=test_case_result, step=step, api_name=step_api.name, api_url=url, api_data=data, api_response=api_response, status=status)
            step_result.save()
        
        plan_result.append({"case_name": case.name, "case_result": case_result})

        # 判断用例状态
        print("==================================")
        print(case_result['result'])
        if case_result['result'] == 'PASS':
            pass_num += 1
            print("pass_num+1, pass_num: %d" % pass_num)
        elif case_result['result'] == 'FAIL':
            fail_num += 1
            TestCaseResult.objects.filter(id=test_case_result.id).update(status=status)
        else:
            error_num += 1
            print("error_num+1, error_num: %d" % error_num)
            TestCaseResult.objects.filter(id=test_case_result.id).update(status=status)
    print("pass_num: %d, error_num: %d" % (pass_num, error_num))
    TestReport.objects.filter(id=test_report.id).update(content=json.dumps(plan_result), case_num=case_num, pass_num=pass_num, fail_num=fail_num, error_num=error_num)
    # test_report = TestReport(test_plan=plan, content=json.dumps(plan_result), case_num=case_num, pass_num=pass_num, fail_num=fail_num, error_num=error_num)
    # test_report.save()
    return HttpResponse(json.dumps(plan_result))


@login_required
def plan_report(request, plan_id):
    report_list = TestReport.objects.filter(test_plan=plan_id)
    return render(request, "report_list.html", {"report_list": report_list})



@login_required
def plan_del(request, plan_id):
    if request.method == 'GET':
        TestPlan.objects.filter(id=plan_id).delete()
        return HttpResponseRedirect('/plan/')


# 测试报告 -----------------------------------------------------------------------------------------
@login_required
def report_list(request):
    report_list = TestReport.objects.all()
    return render(request, "report_list.html", {"report_list": report_list})


@login_required
def report_detail(request, report_id):
    if request.method == 'GET':
        report = get_object_or_404(TestReport, id=report_id)
        case_result_list = TestCaseResult.objects.filter(report=report_id)
        step_result_list = StepResult.objects.filter(test_case_result__in=case_result_list)
        return render(request, "report_detail.html", {"report": report, 'case_result_list': case_result_list, 'step_result_list': step_result_list})


@login_required
def report_del(request, report_id):
    if request.method == 'GET':
        TestReport.objects.filter(id=report_id).delete()
        return HttpResponseRedirect('/report/')


# 签名报告 -----------------------------------------------------------------------------------------
@login_required
def sign_list(request):  
    sign_list = Sign.objects.all()
    return render(request, "sign_list.html", {"sign_list": sign_list})


@login_required
def sign_detail(request, sign_id):
    if request.method == 'GET':
        sign = get_object_or_404(Sign, id=sign_id) 
        return render(request, "sign_detail.html", {"sign": sign})


@login_required
def sign_del(request, sign_id):
    if request.method == 'GET':
        Sign.objects.filter(id=sign_id).delete()
        return HttpResponseRedirect('/sign/')

# 搜索 -----------------------------------------------------------------------------------------
def search(request, str):
    pass
