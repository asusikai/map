from django.shortcuts import render, get_object_or_404
from users.models import Profile
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json
from acci_type.type import acci_type
import pandas as pd
from .models import *


def mainpage(request):

    trenches=Trench.objects.raw('select trench.trench_num, trench.longitude, trench.latitude, ml_result.acc from trench, ml_result where (trench.trench_num = ml_result.trench_num)')
    

    return render(request,'mainpage.html',{"trenches":trenches })
   
   

@require_POST
def check(request):

    dataset = pd.read_csv('acci_type/accident_dataset.csv',encoding='UTF-8')
    top_3={}
    data=json.loads(request.body)
    print(data["myinfo"])

    top_3=acci_type(data["myinfo"],dataset)

    ac_type=Profile.objects.get(user=request.user)
    ac_type.type_ck=1
    ac_type.my_type=top_3

    ac_type.save()

    return HttpResponse(json.dumps(top_3),content_type="application/json")
    
    
    
