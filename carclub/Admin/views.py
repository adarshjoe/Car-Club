from django.shortcuts import render,redirect
from Admin.models import *
from Spare_Parts_Shop.models import *
from User.models import *
from Workshop.models import *
from django.db.models import Max
from django.contrib import messages
import datetime
from django.views.decorators.cache import cache_control
from django.views.decorators import cache
from django.http import JsonResponse
from django.contrib.auth.models import auth,User
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request): 
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')


def loginAction(request):
    ob=admin_tb.objects.filter(username=request.POST['username'],password=request.POST['password'])
    if ob.count()>0:
        request.session['admin_id']=ob[0].id
        admin=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        auth.login(request,admin)
        return redirect('/')
    else:
        shop=shop_tb.objects.filter(username=request.POST['username'],password=request.POST['password'])
        if shop.count()>0:
            if shop[0].status=="approved":
                request.session['spare_shop_id']=shop[0].id
                shop=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
                auth.login(request,shop)
                return redirect('/')
            else:
                messages.add_message(request,messages.INFO,"account not verified yet")
                return redirect('login')
        else:
            user=user_tb.objects.filter(username=request.POST['username'],password=request.POST['password'])
            if user.count()>0:
                request.session['user_id']=user[0].id
                user=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
                auth.login(request,user)
                return redirect('/')
            else:
                workshop=workshop_tb.objects.filter(username=request.POST['username'],password=request.POST['password'])
                if workshop.count()>0:
                    if workshop[0].status=="approved":
                        request.session['workshop_id']=workshop[0].id
                        wshop=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
                        auth.login(request,wshop)
                        return redirect('/')
                    else:
                        messages.add_message(request,messages.INFO,"account not verified yet")
                        return redirect('login')
                else:
                    messages.add_message(request,messages.INFO,"invalid username or password")
                    return redirect('login')

@login_required
def addCategory(request):
    vehicles=vehicle_tb.objects.all()
    return render(request,'add_category.html',{'data':vehicles})

@login_required
def addCategoryAction(request):
    v_id=vehicle_tb.objects.get(id=request.POST['vehicle'])
    category=part_category_tb.objects.filter(vehicle_id=request.POST['vehicle'],category=request.POST['category'])
    if(category.count()>0):
        messages.add_message(request,messages.INFO,"Already Added")
        return redirect('addCategory')
    else:
        category=part_category_tb(vehicle_id=v_id,category=request.POST['category'])
        category.save()
        messages.add_message(request,messages.INFO,"Added Successfully")
        return redirect('addCategory')

@login_required
def addBrand(request):
    vehicles=vehicle_tb.objects.all()
    return render(request,'add_brand.html',{'data':vehicles})

@login_required
def addBrandAction(request):
    v_id=vehicle_tb.objects.get(id=request.POST['vehicle'])
    brand=brand_tb.objects.filter(vehicle_id=request.POST['vehicle'],brand_name=request.POST['brand'])
    if(brand.count()>0):
        messages.add_message(request,messages.INFO,"Already Added")
        return redirect('addBrand')
    else:
        brand=brand_tb(vehicle_id=v_id,brand_name=request.POST['brand'])
        brand.save()
        messages.add_message(request,messages.INFO,"Added Successfully")
        return redirect('addBrand')

@login_required
def addModel(request):
    vehicles=vehicle_tb.objects.all()
    return render(request,'add_model.html',{'data':vehicles})

def getBrand(request):
    vid=request.GET.get('vehicle_id')
    brands=brand_tb.objects.filter(vehicle_id=vid)
    return render(request,'get_brand.html',{'data':brands})

@login_required
def addModelAction(request):
    v_id=vehicle_tb.objects.get(id=request.POST['vehicle'])
    b_id=brand_tb.objects.get(id=request.POST['brand'])
    vehicles=vehicle_tb.objects.all()
    model=model_tb.objects.filter(vehicle_id=request.POST['vehicle'],brand_id=request.POST['brand'],model_name=request.POST['model'])
    if(model.count()>0):
        messages.add_message(request,messages.INFO,"Already Added")
        return redirect('addModel')
    else:
        model=model_tb(vehicle_id=v_id,brand_id=b_id,model_name=request.POST['model'])
        model.save()
        messages.add_message(request,messages.INFO,"Added Successfully")
        return redirect('addModel')

@login_required
def viewSpareShop(request):
    shop=shop_tb.objects.all().order_by('-id')
    if(shop.count()>0):
        return render(request,'view_spare_shop.html',{'data':shop})
    else:
        return render(request,'view_spare_shop.html',{'msg':'No Registrations'})

@login_required
def shopDetails(request,sid):
    shop=shop_tb.objects.filter(id=sid)
    return render(request,'shop_details.html',{'data':shop})

@login_required
def approveSpareShop(request,sid):
    shop=shop_tb.objects.filter(id=sid)
    shop.update(status="approved")
    messages.add_message(request,messages.INFO,"Approved")
    return redirect('shopDetails',sid=sid)

@login_required
def rejectSpareShop(request,sid):
    shop=shop_tb.objects.filter(id=sid)
    shop.update(status="rejected")
    messages.add_message(request,messages.INFO,"Rejected")
    return redirect('shopDetails',sid=sid)

@login_required
def removeSpareShop(request,sid):
    shop=shop_tb.objects.filter(id=sid).delete()
    messages.add_message(request,messages.INFO,"Removed Successfully")
    return redirect('viewSpareShop')

@login_required
def salesReport(request):
    shop=shop_tb.objects.filter(status="approved")
    return render(request,'sales_report.html',{'shops':shop})

@login_required
def getTransactions(request):
    sid=request.GET.get('shop')
    transactions=payment_tb.objects.filter(shop_id=sid).order_by('-id')
    shop=shop_tb.objects.filter(id=sid)
    shops=shop_tb.objects.filter(status="approved")
    if(transactions.count()>0):
        return render(request,'sales_report.html',{'data':transactions,'shopdetails':shop,'shops':shops})
    else:
        return render(request,'sales_report.html',{'msg':'No Sales','shopdetails':shop,'shops':shops})

@login_required
def updateStatus(request,pid):
    transaction=payment_tb.objects.filter(id=pid)
    transaction.update(status="share received")
    transactions=payment_tb.objects.filter(shop_id=transaction[0].shop_id_id).order_by('-id')
    shop=shop_tb.objects.filter(id=transaction[0].shop_id_id)
    shops=shop_tb.objects.filter(status="approved")
    return render(request,'sales_report.html',{'data':transactions,'shopdetails':shop,'shops':shops})

@login_required
def viewComplaints(request):
    complaints=complaint_tb.objects.all().order_by('-id')
    if(complaints.count()>0):
        return render(request,'view_complaints.html',{'data':complaints})
    else:
        return render(request,'view_complaints.html',{'msg':'No Complaints'})

@login_required
def complaintDetails(request,cid):
    complaint=complaint_tb.objects.filter(id=cid)
    #reply=reply_tb.objects.filter(complaint_id=cid)
    return render(request,'view_complaint_details.html',{'data':complaint})

@login_required
def deleteComplaint(request,cid):
    complaint_obj=complaint_tb.objects.filter(id=cid).delete()
    messages.add_message(request,messages.INFO,"Deleted Successfully")
    return redirect('viewComplaints')

@login_required
def viewWorkshop(request):
    workshop=workshop_tb.objects.all().order_by('-id')
    if(workshop.count()>0):
        return render(request,'view_workshop.html',{'data':workshop})
    else:
        return render(request,'view_workshop.html',{'msg':'No Registrations'})

@login_required
def approveWorkshop(request,wid):
    workshop=workshop_tb.objects.filter(id=wid)
    workshop.update(status="approved")
    messages.add_message(request,messages.INFO,"Approved")
    return redirect('viewWorkshop')

@login_required
def rejectWorkshop(request,wid):
    workshop=workshop_tb.objects.filter(id=wid)
    workshop.update(status="rejected")
    messages.add_message(request,messages.INFO,"Rejected")
    return redirect('viewWorkshop')

@login_required
def removeWorkshop(request,wid):
    workshop=workshop_tb.objects.filter(id=wid).delete()
    messages.add_message(request,messages.INFO,"Removed Successfully")
    return redirect('viewWorkshop')


def forgotPassword(request):
    return render(request,'forgot_password.html')

def getNext(request):
    username=request.POST['username']
    admin=admin_tb.objects.filter(username=username)
    
    if(admin.count()>0):
        return render(request,'change_password.html',{'username':username})
    else:
        shop=shop_tb.objects.filter(username=username)
        if(shop.count()>0):
            return render(request,'shop_data.html',{'username':username})
        else:
            wshop=workshop_tb.objects.filter(username=username)
            if(wshop.count()>0):
                return render(request,'shop_data.html',{'username':username})
            else:
                user=user_tb.objects.filter(username=username)
                if(user.count()>0):
                    return render(request,'user_data.html',{'username':username})
                else:
                    messages.add_message(request,messages.INFO,"Invalid Username")
                    return redirect('forgotPassword')

def changePasswordAction(request):
    new_password=request.POST['password']
    confirm_password=request.POST['confirm_password']
    username=request.POST['username']
    admin=admin_tb.objects.filter(username=username)
    shop=shop_tb.objects.filter(username=username)
    wshop=workshop_tb.objects.filter(username=username)
    user=user_tb.objects.filter(username=username)
    if(admin.count()>0):
        admin.update(password=new_password)
    elif(shop.count()>0):
        shop.update(password=new_password)
    elif(wshop.count()>0):
        wshop.update(password=new_password)
    else:
        user.update(password=new_password)
    user=User.objects.get(username=username)
    user.set_password(new_password)
    user.save()
    messages.add_message(request,messages.INFO,"Password Changed Succesfully")
    return redirect('login')

def validateShopData(request):
    shop_name=request.POST['shop_name']
    phone=request.POST['phone']
    email=request.POST['email']
    username=request.POST['username']
    shop=shop_tb.objects.filter(shop_name=shop_name,phone=phone,email=email,username=username)
    work_shop=workshop_tb.objects.filter(shop_name=shop_name,phone=phone,email=email,username=username)
    if((shop.count()>0) or (work_shop.count()>0)):
        return render(request,'change_password.html',{'username':username})
    else:
        return render(request,'shop_data.html',{'msg':'Invalid Data','username':username})

def validateUserData(request):
    name=request.POST['name']
    dob=request.POST['dob']
    email=request.POST['email']
    username=request.POST['username']
    user=user_tb.objects.filter(name=name,dob=dob,email=email,username=username)
    if(user.count()>0):
        return render(request,'change_password.html',{'username':username})
    else:
        return render(request,'user_data.html',{'username':username,'msg':'Invalid Data'})

@login_required
def workshopDetails(request,sid):
    workshop=workshop_tb.objects.filter(id=sid)
    return render(request,'workshop_details.html',{'data':workshop})

@login_required
def replyAction(request):
    complaint_id=request.POST['complaint_id']
    complaint=complaint_tb.objects.get(id=complaint_id)
    subject=request.POST['subject']
    reply=request.POST['reply']
    reply=reply_tb(complaint_id=complaint,user_id=complaint.user_id,subject=subject,reply=reply,date=datetime.date.today())
    reply.save()
    messages.add_message(request,messages.INFO,"Reply Sent Successfully")
    return redirect('complaintDetails',cid=complaint_id)

@login_required
def viewCategory(request):
    categories=part_category_tb.objects.all()
    return render(request,'categories.html',{'data':categories})

@login_required
def updateCategory(request,cid):
    category=part_category_tb.objects.filter(id=cid)
    return render(request,'edit_category.html',{'data':category})

@login_required
def editCategoryAction(request):
    cid=request.POST['cid']
    category=request.POST['category']
    cat=part_category_tb.objects.filter(id=cid).update(category=category)
    messages.add_message(request,messages.INFO,"Updated Successfully")
    return redirect('updateCategory',cid=cid)

@login_required
def viewBrand(request):
    brands=brand_tb.objects.all()
    return render(request,'brand.html',{'data':brands})

@login_required
def updateBrand(request,bid):
    brand=brand_tb.objects.filter(id=bid)
    return render(request,'edit_brand.html',{'data':brand})

@login_required
def editBrandAction(request):
    bid=request.POST['bid']
    brand=request.POST['brand']
    br=brand_tb.objects.filter(id=bid).update(brand_name=brand)
    messages.add_message(request,messages.INFO,"Updated Successfully")
    return redirect('updateBrand',bid=bid)

@login_required
def deleteBrand(request,bid):
    br=brand_tb.objects.filter(id=bid).delete()
    messages.add_message(request,messages.INFO,"Deleted Successfully")
    return redirect('viewBrand')

@login_required
def viewModel(request):
    models=model_tb.objects.all()
    return render(request,'model.html',{'data':models})

@login_required
def updateModel(request,mid):
    model=model_tb.objects.filter(id=mid)
    return render(request,'edit_model.html',{'data':model})

@login_required
def editModelAction(request):
    mid=request.POST['mid']
    model=request.POST['model']
    model=model_tb.objects.filter(id=mid).update(model_name=model)
    messages.add_message(request,messages.INFO,"Updated Successfully")
    return redirect('updateModel',mid=mid)

@login_required
def deleteModel(request,mid):
    model=model_tb.objects.filter(id=mid).delete()
    messages.add_message(request,messages.INFO,"Deleted Successfully")
    return redirect('viewModel')

def checkUsername(request):
    status=''
    uname=request.GET.get('username')
    shop=shop_tb.objects.filter(username=uname)
    workshop=workshop_tb.objects.filter(username=uname)
    user=user_tb.objects.filter(username=uname)
    admin=admin_tb.objects.filter(username=uname)
    if((workshop.count()>0) or (shop.count()>0) or (user.count()>0) or (admin.count()>0)):
        status='exists'
    else:
        status='not exists'
    return JsonResponse({'status':status})

def checkUsernameUpdate(request):
    status=''
    uname=request.GET.get('username')
    if 'user_id' in request.session:
        user=user_tb.objects.filter(username=uname).exclude(id=request.session['user_id'])
    else:
        user=user_tb.objects.filter(username=uname)

    if 'spare_shop_id' in request.session:
        shop=shop_tb.objects.filter(username=uname).exclude(id=request.session['spare_shop_id'])
    else:
        shop=shop_tb.objects.filter(username=uname)

    if 'workshop_id' in request.session:
        workshop=workshop_tb.objects.filter(username=uname).exclude(id=request.session['workshop_id'])
    else:
        workshop=workshop_tb.objects.filter(username=uname)
        
    admin=admin_tb.objects.filter(username=uname)
    if((workshop.count()>0) or (shop.count()>0) or (user.count()>0) or (admin.count()>0)):
        status='exists'
    else:
        status='not exists'
    return JsonResponse({'status':status})

def getModelDrop(request):
    bid=request.GET.get('brand_id')
    models=model_tb.objects.filter(brand_id=bid)
    return render(request,'get_model_drop.html',{'data':models})

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'admin_id' in request.session:
        del request.session['admin_id']
    if 'spare_shop_id' in request.session:
        del request.session['spare_shop_id']
    if 'workshop_id' in request.session:
        del request.session['workshop_id']
    auth.logout(request)
    return redirect('/')
    
    

