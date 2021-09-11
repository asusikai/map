from users.views import myinfo
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json
from .acci_type.type import acci_type
import pandas as pd
from users.models import Profile
# Create your views here.

def show(request):

    trenches=Trench.objects.raw('select trench.trench_num, trench.longitude, trench.latitude, ml_result.acc from trench, ml_result where (trench.trench_num = ml_result.trench_num)')
    
    return render(request,'map.html',{"trenches":trenches, })

def ifr(request):
    return render(request,'iframemap.html')

def hi(requset):
    b=Trench.objects.extra(tables=['ml_result'], where=['trench.trench_num = ml_result.trench_num']).all()
    a= Trench.objects.raw('select trench.trench_num, trench.longitude, trench.latitude, ml_result.acc from trench, ml_result where (trench.trench_num = ml_result.trench_num)')
    print(a.query)

    for x in a:
        print(x.trench_num)
        print(x.acc) 
    return HttpResponse('hi')
    
def testjq(request):
    mine=Profile.objects.get(user=request.user)
    print(mine.my_type)
    return render(request,'jq.html',{"mine":mine})

@require_POST
def check(request):

    dataset = pd.read_csv('grid/acci_type/accident_dataset.csv',encoding='UTF-8')
    top_3={}
    data=json.loads(request.body)
    print(data["myinfo"])

    top_3=acci_type(data["myinfo"],dataset)

    ac_type=Profile.objects.get(user=request.user)
    ac_type.type_ck=1
    ac_type.my_type=top_3

    ac_type.save()

    return HttpResponse(json.dumps(top_3),content_type="application/json")
    
    
    
