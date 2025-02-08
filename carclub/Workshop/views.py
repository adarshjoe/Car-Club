from django.shortcuts import render,redirect
from Workshop.models import *
from Spare_Parts_Shop.models import *
from User.models import *
from Admin.models import *
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def workshopSignup(request):
    districts=district_tb.objects.all()
    return render(request,'workshop_signup.html',{'districts':districts})

def workshopSignupAction(request):
    logo_img=""
    proof=""
    if(len(request.FILES)>0):
        logo_img=request.FILES['logo']
        proof=request.FILES['proof']
    else:
        logo_img="no logo"
        proof="no proof"
    did=district_tb.objects.get(id=request.POST['district'])
    workshop=workshop_tb(logo=logo_img,shop_name=request.POST['shopname'],phone=request.POST['phone'],email=request.POST['email'],address=request.POST['address'],
                             district_id=did,place=request.POST['place'],proof=proof,username=request.POST['username'],
                             password=request.POST['password'],status='pending')
    workshop.save()
    workshop=User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
    workshop.save()
    messages.add_message(request,messages.INFO,"Signup successful")
    return redirect('workshopSignup')

@login_required
def updateProfileWorkshop(request):
    workshop=workshop_tb.objects.filter(id=request.session['workshop_id'])
    districts=district_tb.objects.all().exclude(id=workshop[0].district_id_id)
    return render(request,'update_profile_workshop.html',{'data':workshop,'districts':districts})

@login_required
def updateProfileWorkshopAction(request):
    logo_img=""
    proof=""
    workshop=workshop_tb.objects.filter(id=request.session['workshop_id'])
    if 'logo' in request.FILES:
        logo_img=request.FILES['logo']
    else:
        logo_img=workshop[0].logo

    if 'proof' in request.FILES:
        proof=request.FILES['proof']
    else:
        proof=workshop[0].proof
        
    sname=request.POST['shopname']
    phone=request.POST['phone']
    email=request.POST['email']
    address=request.POST['address']
    place=request.POST['place']
    username=request.POST['username']
    password=request.POST['password']
    did=district_tb.objects.get(id=request.POST['district'])

    shop_auth=User.objects.get(username=workshop[0].username)
    workshop_obj=workshop_tb.objects.get(id=request.session['workshop_id'])
    workshop_obj.logo=logo_img
    workshop_obj.shop_name=sname
    workshop_obj.phone=phone
    workshop_obj.email=email
    workshop_obj.address=address
    workshop_obj.district_id=did
    workshop_obj.place=place
    workshop_obj.proof=proof
    workshop_obj.username=username
    workshop_obj.password=password
    workshop_obj.save()
    shop_auth.username=username
    shop_auth.set_password(password)
    shop_auth.save()
    shop_auth=auth.authenticate(username=username,password=password)
    auth.login(request,shop_auth)
    request.session['workshop_id']=workshop[0].id
    messages.add_message(request,messages.INFO,"Updated Successfully")
    return redirect('updateProfileWorkshop')

@login_required
def addService(request):
    return render(request,'add_service.html')

@login_required
def addServiceAction(request):
    wid=workshop_tb.objects.get(id=request.session['workshop_id'])
    service_obj=service_tb(shop_id=wid,service=request.POST['service'],description=request.POST['description'],status='available',service_img=request.FILES['upload'])
    service_obj.save()
    messages.add_message(request,messages.INFO,"Added Successfully")
    return redirect('addService')

@login_required
def viewServicesByWorkshop(request):
    services=service_tb.objects.filter(shop_id=request.session['workshop_id']).order_by('-id')
    if(services.count()>0):
        if 'service_page' in request.session:
            page=request.session['service_page']
            del request.session['service_page']
        else:
            page=request.GET.get('page',1)
        paginator=Paginator(services,3)
        try:
            all_services=paginator.page(page)
        except PageNotAnInteger:
            all_services=paginator.page(1)
        except EmptyPage:
            all_services=paginator.page(paginator.num_pages)
        return render(request,'view_services_by_workshop.html',{'data':all_services})
    else:
        return render(request,'view_services_by_workshop.html',{'msg':'Not Added Single One'})

@login_required
def updateService(request,sid):
    service=service_tb.objects.filter(id=sid)
    return render(request,'update_service.html',{'data':service})

@login_required
def updateServiceAction(request):
    sid=request.POST['service_id']
    service_obj=service_tb.objects.get(id=sid)
    img=''
    if len(request.FILES)>0:
        img=request.FILES['upload']
    else:
        img=service_obj.service_img
    service_obj.service_img=img
    service_obj.service=request.POST['service']
    service_obj.description=request.POST['description']
    service_obj.status=request.POST['status']
    service_obj.save()
    messages.add_message(request,messages.INFO,"Updated Successfully")
    return redirect('updateService',sid=sid)

@login_required
def deleteService(request,sid,page):
    service=service_tb.objects.filter(id=sid).delete()
    request.session['service_page']=page
    messages.add_message(request,messages.INFO,"Deleted Successfully")
    return redirect('viewServicesByWorkshop')

@login_required
def viewReviewsByWorkshop(request):
    reviews=workshop_review_tb.objects.filter(shop_id=request.session['workshop_id']).order_by('-id')
    if(reviews.count()>0):
        page=request.GET.get('page',1)
        paginator=Paginator(reviews,3)
        try:
            all_reviews=paginator.page(page)
        except PageNotAnInteger:
            all_reviews=paginator.page(1)
        except EmptyPage:
            all_reviews=paginator.page(paginator.num_pages)
        return render(request,'view_review_by_workshop.html',{'reviews':all_reviews})
    else:
        return render(request,'view_review_by_workshop.html',{'msg':'No reviews'})

def returnToWorkshopHome(request):
    return render(request,'workshop_home.html')


