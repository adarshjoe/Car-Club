from django.shortcuts import render,redirect
from Spare_Parts_Shop.models import *
from Admin.models import *
from User.models import *
from Workshop.models import *
import datetime
import time
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import auth,User
from django.contrib.auth.decorators import login_required

# Create your views here.
def get_part_list(parts):
    splist=[]
    for s in parts:
        spdic=s.__dict__
        spdic['brand_id']=s.brand_id
        spdic['vehicle_id']=s.vehicle_id
        spdic['shop_id']=s.shop_id
        spdic['category_id']=s.category_id
        spdic['part_obj']=s
        pmodels=part_model_tb.objects.filter(part_id=s.id).values('model_id__model_name')
        plist=[]
        for p in pmodels:
            plist.append(p['model_id__model_name'])
        st=','
        mod=st.join(plist)
        spdic['models']=mod
        splist.append(spdic)
    return splist

def shopSignup(request):
    districts=district_tb.objects.all()
    return render(request,'shop_signup.html',{'districts':districts})

def getState(request):
    cid=request.GET.get('country_id')
    states=state_tb.objects.filter(country_id=cid)
    return render(request,'get_state.html',{'states':states})

def getDistrict(request):
    sid=request.GET.get('state_id')
    districts=district_tb.objects.filter(state_id=sid)
    return render(request,'get_district.html',{'districts':districts})

def shopSignupAction(request):
    logo_img=""
    proof=""
    if(len(request.FILES)>0):
        logo_img=request.FILES['logo']
        proof=request.FILES['proof']
    else:
        logo_img="no logo"
        proof="no proof"
    did=district_tb.objects.get(id=request.POST['district'])
    shop=shop_tb(logo=logo_img,shop_name=request.POST['shopname'],phone=request.POST['phone'],email=request.POST['email'],address=request.POST['address'],
                     district_id=did,place=request.POST['place'],proof=proof,username=request.POST['username'],password=request.POST['password'],
                     status='pending')
    shop.save()
    shop=User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
    shop.save()
    messages.add_message(request,messages.INFO,"Signup successful")
    return redirect('shopSignup')

@login_required
def addSpareParts(request):
    return render(request,'add_spare_parts.html')
        
def getModel(request):
    bid=request.GET.get('brand_id')
    models=model_tb.objects.filter(brand_id=bid)
    return render(request,'get_model.html',{'data':models})

def getCategory(request):
    vid=request.GET.get('vehicle_id')
    category=part_category_tb.objects.filter(vehicle_id=vid)
    return render(request,'get_category.html',{'data':category})

@login_required
def addSparePartsAction(request):
    part_img=""
    vid=vehicle_tb.objects.get(id=request.POST['vehicle'])
    bid=brand_tb.objects.get(id=request.POST['brand'])
    #mid=model_tb.objects.get(id=request.POST['model'])
    s_id=shop_tb.objects.get(id=request.session['spare_shop_id'])
    cid=part_category_tb.objects.get(id=request.POST['category'])
    
    if(len(request.FILES)>0):
        part_img=request.FILES['part_img']
    else:
        part_img="no image"
    if 'model' not in request.POST:
        messages.add_message(request,messages.INFO,"Please select a model")
    else:
    
        spare_part=spare_part_tb(path=part_img,vehicle_id=vid,brand_id=bid,category_id=cid,part_name=request.POST['part_name'],details=request.POST['details'],
                                 price=request.POST['price'],stock=request.POST['stock'],shop_id=s_id)
        spare_part.save()
        part_obj=spare_part_tb.objects.filter(shop_id=request.session['spare_shop_id']).order_by('-id')[0]
        modellist=request.POST.getlist('model')
        for m in modellist:
            mid=model_tb.objects.get(id=m)
            part_model=part_model_tb(part_id=part_obj,model_id=mid)
            part_model.save()
        messages.add_message(request,messages.INFO,"Added Successfully")
    return redirect('addSpareParts')

@login_required
def viewSpareParts(request):
    splist=[]
    s_id=shop_tb.objects.get(id=request.session['spare_shop_id'])
    part=spare_part_tb.objects.filter(shop_id=s_id).order_by('-id')
    for s in part:
        spdic=s.__dict__
        spdic['brand_id']=s.brand_id
        spdic['vehicle_id']=s.vehicle_id
        spdic['shop_id']=s.shop_id
        spdic['category_id']=s.category_id
        spdic['part_obj']=s
        pmodels=part_model_tb.objects.filter(part_id=s.id).values('model_id__model_name')
        plist=[]
        for p in pmodels:
            plist.append(p['model_id__model_name'])
        st=','
        mod=st.join(plist)
        spdic['models']=mod
        splist.append(spdic)
    if part.count()>0:
        page=request.GET.get('page',1)
        all_parts=sparePartPages(splist,page)
        return render(request,'view_spare_part.html',{'data':all_parts})
    else:
        return render(request,'view_spare_part.html',{'msg':'No Parts'})

def sparePartPages(part,page):
    paginator=Paginator(part,4)
    try:
        all_parts=paginator.page(page)
    except PageNotAnInteger:
        all_parts=paginator.page(1)
    except EmptyPage:
        all_parts=paginator.page(paginator.num_pages)
    return all_parts

@login_required
def updateSparePart(request,pid):
    part=spare_part_tb.objects.filter(id=pid)
    vehicle=vehicle_tb.objects.all()
    brand=brand_tb.objects.filter(vehicle_id=part[0].vehicle_id_id).exclude(id=part[0].brand_id_id)
    model=model_tb.objects.filter(brand_id=part[0].brand_id_id)
    part_model=part_model_tb.objects.filter(part_id=pid)
    category=part_category_tb.objects.filter(vehicle_id=part[0].vehicle_id_id)
    return render(request,'update_spare_part.html',{'data':part,'vehicle':vehicle,'brand':brand,'model':model,'part_model':part_model,'category':category})

@login_required
def updateSparePartAction(request):
    part_img=""
    pid=request.POST['part_id']
    vid=vehicle_tb.objects.get(id=request.POST['vehicle'])
    bid=brand_tb.objects.get(id=request.POST['brand'])
    category=part_category_tb.objects.get(id=request.POST['category'])
    if(len(request.FILES)>0):
        part_img=request.FILES['part_img']
    else:
        ob=spare_part_tb.objects.filter(id=pid)
        part_img=ob[0].path
    #spare_part=spare_part_tb.objects.filter(id=pid).update(path=part_img,vehicle_id=vid,brand_id=bid,
                                                           #model_id=mid,part_name=request.POST['part_name'],
                                                          #details=request.POST['details'],price=request.POST['price'],stock=request.POST['stock'])
    if 'model' not in request.POST:
        messages.add_message(request,messages.INFO,"Please select a model")
    else:
        spare_part=spare_part_tb.objects.get(id=pid)
        spare_part.path=part_img
        spare_part.vehicle_id=vid
        spare_part.brand_id=bid
        spare_part.category_id=category
        spare_part.part_name=request.POST['part_name']
        spare_part.details=request.POST['details']
        spare_part.price=request.POST['price']
        spare_part.stock=request.POST['stock']
        spare_part.save()
        part_model=part_model_tb.objects.filter(part_id=pid).delete()
        modellist=request.POST.getlist('model')
        for m in modellist:
            mid=model_tb.objects.get(id=m)
            part_model=part_model_tb(part_id=spare_part,model_id=mid)
            part_model.save()
        messages.add_message(request,messages.INFO,"Updated Successfully")
    return redirect('updateSparePart',pid=pid)

@login_required
def deleteSparePart(request,pid):
    part=spare_part_tb.objects.filter(id=pid).delete()
    return redirect('viewSpareParts')
    
@login_required
def viewOrders(request):
    status=['rejected','cancelling verified']
    orders=order_tb.objects.filter(shop_id=request.session['spare_shop_id']).exclude(status__in=status).order_by('-id')
    olist=[]
    for s in orders:
        spdic=s.__dict__
        spdic['part_id']=s.part_id
        spdic['user_id']=s.user_id
        spdic['shop_id']=s.shop_id
        pmodels=part_model_tb.objects.filter(part_id=s.part_id).values('model_id__model_name')
        plist=[]
        for p in pmodels:
            plist.append(p['model_id__model_name'])
        st=','
        mod=st.join(plist)
        spdic['models']=mod
        olist.append(spdic)
    if(orders.count()>0):
        if 'order_page' in request.session:
            page=request.session['order_page']
            del request.session['order_page']
        else:
            page=request.GET.get('page',1)
        all_orders=orderPages(olist,page)
        return render(request,'view_order.html',{'data':all_orders})
    else:
        return render(request,'view_order.html',{'msg':'No Order'})
    
def orderPages(orders,page):
    paginator=Paginator(orders,3)
    try:
        all_orders=paginator.page(page)
    except PageNotAnInteger:
        all_orders=paginator.page(1)
    except EmptyPage:
        all_orders=paginator.page(paginator.num_pages)
    return all_orders

@login_required
def orderDetails(request,oid):
    order=order_tb.objects.filter(id=oid)
    part_model=part_model_tb.objects.filter(part_id=order[0].part_id)
    return render(request,'order_details.html',{'data':order,'part_model':part_model})

@login_required
def approveOrder(request,oid):
    order=order_tb.objects.filter(id=oid)
    order.update(status="approved")
    notification=notification_tb(user_id=order[0].user_id,seller_id=order[0].shop_id,table='order_tb',order_id=order[0],
                                 date=datetime.date.today(),time=time.asctime(time.localtime(time.time())))
    notification.save()
    messages.add_message(request,messages.INFO,"Approved")
    return redirect('orderDetails',oid=oid)

@login_required
def rejectOrder(request,oid):
    order=order_tb.objects.filter(id=oid)
    order.update(status="rejected")
    count=order[0].count
    
    spare_part=spare_part_tb.objects.filter(id=order[0].part_id_id)
    left=int(spare_part[0].stock)
    part_stock=left+count
    spare_part.update(stock=part_stock)
    notification=notification_tb(user_id=order[0].user_id,seller_id=order[0].shop_id,table='order_tb',order_id=order[0],
                                 date=datetime.date.today(),time=time.asctime(time.localtime(time.time())))
    notification.save()
    messages.add_message(request,messages.INFO,"Rejected")
    return redirect('orderDetails',oid=oid)

@login_required
def paymentDetails(request,oid):
    payment=payment_tb.objects.filter(order_id=oid)
    return render(request,'payment_details.html',{'data':payment})

@login_required
def addTrackingDetails(request,oid,page):
    return render(request,'add_tracking_details.html',{'order_id':oid,'page':page})

@login_required
def addTrackingDetailsAction(request):
    order_id=request.POST['order_id']
    decheck=request.POST.get('decheck')
    request.session['order_page']=request.POST['page']
    oid=order_tb.objects.get(id=order_id)
    t_details=request.POST['details']
    details=tracking_details_tb(tracking_details=t_details,date=datetime.date.today(),time=time.strftime("%H:%M:%S",time.localtime()),order_id=oid)
    details.save()
    if decheck:
        order=order_tb.objects.filter(id=order_id).update(status="delivered")
    messages.add_message(request,messages.INFO,"Tracking detailes added")
    return redirect('viewOrders')

@login_required
def verifyCancelling(request,oid,page):
    request.session['order_page']=page
    order=order_tb.objects.filter(id=oid)
    order.update(status="cancelling verified")
    count=int(order[0].count)
    part=order[0].part_id
    part_dic=part.__dict__
    part_id=part_dic.get("id")
    spare_part=spare_part_tb.objects.filter(id=part_id)
    left=int(spare_part[0].stock)
    part_stock=left+count
    spare_part.update(stock=part_stock)
    #status=['rejected','cancelling verified']
    #orders=order_tb.objects.filter(shop_id=request.session['spare_shop_id']).exclude(status__in=status).order_by('-id')
    messages.add_message(request,messages.INFO,"Cancelling Verified")
    return redirect('viewOrders')

@login_required
def updateProfileShop(request):
    shop=shop_tb.objects.filter(id=request.session['spare_shop_id'])
    districts=district_tb.objects.all().exclude(id=shop[0].district_id_id)
    return render(request,'update_profile_shop.html',{'data':shop,'districts':districts})

@login_required
def updateProfileShopAction(request):
    logo_img=""
    proof=""
    shop=shop_tb.objects.filter(id=request.session['spare_shop_id'])
    if 'logo' in request.FILES:
        logo_img=request.FILES['logo']
    else:
        logo_img=shop[0].logo

    if 'proof' in request.FILES:
        proof=request.FILES['proof']
    else:
        proof=shop[0].proof
    sname=request.POST['shopname']
    phone=request.POST['phone']
    email=request.POST['email']
    address=request.POST['address']
    place=request.POST['place']
    username=request.POST['username']
    password=request.POST['password']
    did=district_tb.objects.get(id=request.POST['district'])

    shop_auth=User.objects.get(username=shop[0].username)
##    shops=shop_tb.objects.filter(username=username).exclude(id=request.session['spare_shop_id'])
##    workshop=workshop_tb.objects.filter(username=username)
##    user=user_tb.objects.filter(username=username)
##    admin=admin_tb.objects.filter(username=username)
##    if((workshop.count()>0) or (shops.count()>0) or (user.count()>0) or (admin.count()>0)):
##        messages.add_message(request,messages.INFO,"Username Already Exists")
##        return redirect('updateProfileShop')
##    else:
    shop_obj=shop_tb.objects.get(id=request.session['spare_shop_id'])
    shop_obj.logo=logo_img
    shop_obj.shop_name=sname
    shop_obj.phone=phone
    shop_obj.email=email
    shop_obj.address=address
    shop_obj.district_id=did
    shop_obj.place=place
    shop_obj.proof=proof
    shop_obj.username=username
    shop_obj.password=password
    shop_obj.save()
    shop_auth.username=username
    shop_auth.set_password(password)
    shop_auth.save()
    shop_auth=auth.authenticate(username=username,password=password)
    auth.login(request,shop_auth)
    request.session['spare_shop_id']=shop[0].id
        #shop.update(logo=logo_img,shop_name=sname,phone=phone,email=email,address=address,country_id=cid,state_id=sid,district_id=did,place=place,proof=proof,
                #username=username,password=password)
    messages.add_message(request,messages.INFO,"Updated Successfully")
    return redirect('updateProfileShop')

@login_required
def viewSparePartReview(request,pid):
    reviews=rating_tb.objects.filter(part_id=pid)
    if(reviews.count()>0):
        page=request.GET.get('page',1)
        paginator=Paginator(reviews,1)
        try:
            all_reviews=paginator.page(page)
        except PageNotAnInteger:
            all_reviews=paginator.page(1)
        except EmptyPage:
            all_reviews=paginator.page(paginator.num_pages)
        return render(request,'view_review_shop.html',{'reviews':all_reviews})
    else:
        return render(request,'view_review_shop.html',{'msg':'No reviews'})

@login_required
def viewPrebookings(request):
    prebook=prebook_tb.objects.filter(shop_id=request.session['spare_shop_id']).exclude(status="rejected").order_by('-id')
    olist=[]
    for s in prebook:
        spdic=s.__dict__
        spdic['part_id']=s.part_id
        spdic['user_id']=s.user_id
        spdic['shop_id']=s.shop_id
        pmodels=part_model_tb.objects.filter(part_id=s.part_id).values('model_id__model_name')
        plist=[]
        for p in pmodels:
            plist.append(p['model_id__model_name'])
        st=','
        mod=st.join(plist)
        spdic['models']=mod
        olist.append(spdic)
    if(prebook.count()>0):
        if 'prebook_page' in request.session:
            page=request.session['prebook_page']
            del request.session['prebook_page']
        else:
            page=request.GET.get('page',1)
        all_prebook=prebookingPages(olist,page)
        return render(request,'view_prebookings.html',{'data':all_prebook})
    else:
        return render(request,'view_prebookings.html',{'msg':'No Prebookings'})

def prebookingPages(prebook,page):
    paginator=Paginator(prebook,2)
    try:
        all_prebook=paginator.page(page)
    except PageNotAnInteger:
        all_prebook=paginator.page(1)
    except EmptyPage:
        all_prebook=paginator.page(paginator.num_pages)
    return all_prebook

@login_required
def approvePrebook(request,pid,page):
    request.session['prebook_page']=page
    prebook=prebook_tb.objects.filter(id=pid)
    prebook.update(status="approved")
    notification=notification_tb(user_id=prebook[0].user_id,seller_id=prebook[0].shop_id,table='prebook_tb',prebook_id=prebook[0],
                                 date=datetime.date.today(),time=time.asctime(time.localtime(time.time())))
    notification.save()
    messages.add_message(request,messages.INFO,"Approved")
    return redirect('viewPrebookings')

@login_required
def rejectPrebook(request,pid,page):
    request.session['prebook_page']=page
    prebook=prebook_tb.objects.filter(id=pid)
    if(prebook[0].status == "approved"):
        part=spare_part_tb.objects.filter(id=prebook[0].part_id_id)
        new_stock=int(prebook[0].count)+int(part[0].stock)
        part.update(stock=new_stock)
        messages.add_message(request,messages.INFO,"Approved Stock Is Added To Main Stock")
    prebook.update(status="rejected")

    notification=notification_tb(user_id=prebook[0].user_id,seller_id=prebook[0].shop_id,table='prebook_tb',prebook_id=prebook[0],
                                 date=datetime.date.today(),time=time.asctime(time.localtime(time.time())))
    notification.save()
    messages.add_message(request,messages.INFO,"Rejected")
    return redirect('viewPrebookings')

@login_required
def searchSparePartByShop(request):
    part_name=request.GET.get('part_name')
    part=spare_part_tb.objects.filter(shop_id=request.session['spare_shop_id'],part_name__contains=part_name)
    splist=get_part_list(part)
    if(part.count()>0):
        page=request.GET.get('page',1)
        all_parts=sparePartPages(splist,page)
        return render(request,'view_spare_part.html',{'data':all_parts,'part_name':part_name})
    else:
        return render(request,'view_spare_part.html',{'msg':'No parts'})

def returnToShopHome(request):
    return render(request,'shop_home.html')


        
    
    
    


    
    
    
    
    
        
