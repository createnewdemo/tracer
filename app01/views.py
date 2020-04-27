from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from utils.tencent.sms import send_sms_single
from django.conf import settings

import random
# Create your views here.
def send_sms(request):
    """发送短信
        ?tpl=login  -> 590050
        ?tpl=register  ->590049
    """
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('模板不存在')
    code = random.randrange(1000,9999)
    res = send_sms_single('17190199811',template_id,[code,])
    print(res)
    if res['result'] == 0:
        return HttpResponse("success")
    else:
        return HttpResponse(res['errmsg'])

from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^^1(3|4|5|6|7|8|9)\d{9}$','手机号格式错误'),])
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput)
    # ModelForm 如果发现自己类中有的字段和models.py中的字段一样 则会选择覆盖重写这个字段
    # 如果发现自己类中的存在的字段 然而models.py中没有 则会自行增加这个字段  数据库中是没有的
    code = forms.CharField(label='验证码')
    class Meta:
        model = models.UserInfo#这里一定是model  没有s
        fields = ['username','email','password','confirm_password','mobile_phone','code']


    def __init__(self,*args,**kwargs):#每次实例化字段都会执行__init__方法的
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' %(field.label)

def register(request):
    form = RegisterModelForm() #实例化

    return render(request, 'app01/register.html', {'form':form})


from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
def index(request):
    # 去连接池中获取一个连接
    conn = get_redis_connection("default")
    conn.set('nickname', "武沛齐", ex=10)
    value = conn.get('nickname')
    print(value)
    return HttpResponse("OK")