from os import write
from community.models import ComPost
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
# Create your views here.

def mypage(request):
    if request.user.is_authenticated:
        user=request.user
        return render(request,"users/mypage.html",{"user":user})
    else:
        return redirect("account_login")


def myinfo(request):
    user=request.user
    return render(request,"users/myinfo.html",{"user":user})


def edit(request):  # 개인만 쓸 페이지
    user = request.user
    return render(request, "users/edit.html", {"user": user})


def update(request):  # 개인만 쓸 함수
    update_profile = request.user.profile
    update_profile.tonnage = request.POST["tonnage"]
    update_profile.ship = request.POST["ship"]
    update_profile.ship_name = request.POST["ship_name"]
    update_profile.month = request.POST["month"]
    update_profile.active_sea = request.POST["active_sea"]
    update_profile.time_f = request.POST["time_f"]
    update_profile.my_info=update_profile.ship+" "+update_profile.ship_name+" "+update_profile.active_sea+" "+update_profile.tonnage+" "+update_profile.month+"월 "+update_profile.time_f
    update_profile.type_ck=0
    update_profile.save()

    return redirect("users:myinfo")

def introduce(request):  # 다른 사람들도 접속하면 볼 수 있는 페이지(iframe)
    return render(request, "introduce.html")
   
def myQnA(request):
    myQnA=ComPost.objects.filter(writer=request.user)
    for i in myQnA:
        print(i.id)
    return render(request,"users/myQnA.html",{"myQnA":myQnA})