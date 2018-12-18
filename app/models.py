from django.db import models


class Sign(models.Model):
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=100, blank=True, null=True)
    content = models.TextField('内容', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:  
        verbose_name = '签名设置'  
        verbose_name_plural = '签名设置' 


class Project(models.Model):
    name = models.CharField('名称', max_length=50)
    developer = models.CharField('开发负责人', max_length=50, blank=True, null=True)
    description = models.CharField('描述', max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:  
        verbose_name = '项目管理'  
        verbose_name_plural = '项目管理' 


class Environment(models.Model):
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:  
        verbose_name = '环境设置'  
        verbose_name_plural = '环境设置' 


class ProjectEnv(models.Model):
    env = models.ForeignKey('Environment', on_delete=models.CASCADE, verbose_name='环境')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='项目')
    url = models.CharField('Url地址', max_length=100)
    sign = models.ForeignKey('Sign', on_delete=models.CASCADE, blank=True, null=True, verbose_name='签名')
    access_id = models.CharField('AccessID',max_length=50, blank=True, null=True)
    access_key = models.CharField('AccessKey',max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.project.name

    class Meta:  
        verbose_name = '项目设置'  
        verbose_name_plural = '项目设置'
    

class Api(models.Model):
    METHOD = ((1, "POST"), (2, "GET"))
    DATA_TYPE = ((1, "JSON"), (2, "FORM"))
    
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=100, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='项目') 
    url = models.CharField('Url地址', max_length=100)
    method = models.IntegerField('请求方法', choices=METHOD)
    data_type = models.IntegerField('数据类型', choices=DATA_TYPE)
    request_body = models.TextField('请求数据', blank=True, null=True)
    response_body = models.TextField('响应数据', blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:  
        verbose_name = '接口管理'  
        verbose_name_plural = '接口管理' 


class Step(models.Model):
    sn = models.IntegerField('序号', blank=True, null=True)
    case = models.ForeignKey('TestCase', on_delete=models.CASCADE, verbose_name='用例')
    api = models.ForeignKey('Api', on_delete=models.CASCADE, verbose_name='接口')
    data = models.TextField('数据', blank=True, null=True)
    assertion = models.TextField('断言', blank=True, null=True)
    

    def __str__(self):
        return self.case.name

    class Meta:  
        verbose_name = '步骤管理'  
        verbose_name_plural = '步骤管理' 

    
class TestCase(models.Model):
    name = models.CharField('名称', max_length=50, blank=True, null=True)
    description = models.CharField('描述', max_length=100, blank=True, null=True)
    plan = models.ForeignKey('TestPlan', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:  
        verbose_name = '测试用例'  
        verbose_name_plural = '测试用例'


class TestPlan(models.Model):
    name = models.CharField('名称', max_length=50)
    environment = models.ForeignKey('Environment', on_delete=models.CASCADE, verbose_name='环境')
    description = models.CharField('描述', max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:  
        verbose_name = '测试计划'  
        verbose_name_plural = '测试计划'


class TestReport(models.Model):
    test_plan = models.ForeignKey('TestPlan', on_delete=models.CASCADE)
    content = models.TextField('内容', blank=True, null=True)
    case_num = models.IntegerField('用例数量', blank=True, null=True)
    pass_num = models.IntegerField('通过数量', blank=True, null=True)
    fail_num = models.IntegerField('失败数量', blank=True, null=True)
    error_num = models.IntegerField('出错数量', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:  
        verbose_name = '测试报告'  
        verbose_name_plural = '测试报告'

class StepResult(models.Model):
    # STATUS = ((1, "PASS"), (2, "FAIL"), (3, "SKIP"), (4, "ERROR"))
    test_case_result = models.ForeignKey('TestCaseResult', on_delete=models.CASCADE, verbose_name='测试用例结果')
    step = models.ForeignKey('Step', on_delete=models.CASCADE, verbose_name='步骤')
    api_name = models.CharField('接口名称', max_length=100, blank=True, null=True)
    api_url = models.CharField('接口Url', max_length=100, blank=True, null=True)
    api_data = models.CharField('请求数据', max_length=100, blank=True, null=True)
    api_response = models.CharField('响应内容', max_length=100, blank=True, null=True)
    status = models.CharField('状态', max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.step.case.name

    class Meta:  
        verbose_name = '步骤结果'  
        verbose_name_plural = '步骤结果'

    
class TestCaseResult(models.Model):
    # STATUS = ((1, "PASS"), (2, "FAIL"), (3, "SKIP"), (4, "ERROR"))
    report = models.ForeignKey('TestReport', on_delete=models.CASCADE, verbose_name='测试报告')
    case = models.ForeignKey('TestCase', on_delete=models.CASCADE, verbose_name='测试用例')
    status = models.CharField('状态', max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.case.name

    class Meta:  
        verbose_name = '用例结果'  
        verbose_name_plural = '用例结果'



