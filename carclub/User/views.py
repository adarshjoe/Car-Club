from django.shortcuts import render,redirect
from User.models import *
from Spare_Parts_Shop.models import *
from Admin.models import *
from Workshop.models import *
import datetime
import random
import time
import math
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def userSignup(request):
    districts=district_tb.objects.all()
    return render(request,'user_signup.html',{'districts':districts})

def userSignupAction(request):
    pro_img=""
    if(len(request.FILES)>0):
        pro_img=request.FILES['pro_img']
    else:
        pro_img="no pic"
    did=district_tb.objects.get(id=request.POST['district'])
    user=user_tb(path=pro_img,name=request.POST['name'],gender=request.POST['gender'],address=request.POST['address'],dob=request.POST['dob'],
                     district_id=did,place=request.POST['place'],phone=request.POST['phone'],email=request.POST['email'],
                     username=request.POST['username'],password=request.POST['password'])
    user.save()
    user=User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
    user.save()
    messages.add_message(request,messages.INFO,"Signup Successful")
    return redirect('userSignup')


def viewSparePartsUser(request):
    splist=[]
    spare_part=spare_part_tb.objects.all().order_by('-id')
    for s in spare_part:
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
        
    if(spare_part.count()>0):
        page=request.GET.get('page',1)
        parts=getPartsPages(splist,page)
        return render(request,'get_spare_parts.html',{'parts':parts})
    else:
        return render(request,'get_spare_parts.html',{'msg':'No Spare Parts'})

def getPartsPages(spare_part,page):
    paginator=Paginator(spare_part,5)
    try:
        parts=paginator.page(page)
    except PageNotAnInteger:
        parts=paginator.page(1)
    except EmptyPage:
        parts=paginator.page(paginator.num_pages)
    return parts


def compareProduct(request):
    p1=request.GET.get('part1')
    p2=request.GET.get('part2')
    part1=spare_part_tb.objects.filter(id=p1)
    part1_model=part_model_tb.objects.filter(part_id=p1)
    part2=spare_part_tb.objects.filter(id=p2)
    part2_model=part_model_tb.objects.filter(part_id=p2)
    return render(request,'compare_product.html',{'part1':part1,'part1_model':part1_model,'part2':part2,'part2_model':part2_model})

@login_required
def addToCart(request,pid):
    part=spare_part_tb.objects.filter(id=pid)
    part_model=part_model_tb.objects.filter(part_id=pid)
    return render(request,'add_cart.html',{'data':part,'part_model':part_model})

@login_required
def addToCartAction(request):
    pid=spare_part_tb.objects.get(id=request.POST['pid'])
    uid=user_tb.objects.get(id=request.session['user_id'])
    sid=shop_tb.objects.get(id=request.POST['sid'])
    count=int(request.POST['count'])
    part=spare_part_tb.objects.filter(id=request.POST['pid'])
    if(count>int(part[0].stock)):
        messages.add_message(request,messages.INFO,"Not enough stock")
        return redirect('addToCart',pid=request.POST['pid'])
    else:
        cart=cart_tb(part_id=pid,phone=request.POST['phone'],address=request.POST['address'],count=request.POST['count'],total_price=request.POST['cost'],
                 user_id=uid,shop_id=sid)
        cart.save()
        messages.add_message(request,messages.INFO,"Added Successfully")
        return redirect('addToCart',pid=request.POST['pid'])
    
@login_required
def viewCart(request):
    cart=cart_tb.objects.filter(user_id=request.session['user_id'])
    return render(request,'view_cart.html',{'data':cart})

@login_required
def deleteFromCart(request,cid):
    cart_obj=cart_tb.objects.filter(id=cid).delete()
    #cart=cart_tb.objects.filter(user_id=request.session['user_id'])
    return redirect('viewCart')

@login_required
def selectOrder(request,cid):
    cart_obj=cart_tb.objects.filter(id=cid)
    part_model=part_model_tb.objects.filter(part_id=cart_obj[0].part_id)
    all_cart=cart_tb.objects.filter(user_id=request.session['user_id'])
    return render(request,'view_cart.html',{'data':all_cart,'cart':cart_obj,'part_model':part_model})

@login_required
def addOrder(request):
    cart=cart_tb.objects.filter(id=request.POST['cart_id'])
    count=int(request.POST['count'])
    
    spare_part=spare_part_tb.objects.filter(id=cart[0].part_id_id)
    stock=int(spare_part[0].stock)
    left=stock-count
    all_cart=cart_tb.objects.filter(user_id=request.session['user_id'])
    if(left<0):
        messages.add_message(request,messages.INFO,"Not enough stock")
        return redirect('selectOrder',cid=request.POST['cart_id'])
    else:
        order=order_tb(part_id=cart[0].part_id,phone=cart[0].phone,address=cart[0].address,count=count,total_price=request.POST['cost'],user_id=cart[0].user_id,
                       date=datetime.date.today(),time=time.strftime("%H:%M:%S",time.localtime()),status='pending',shop_id=cart[0].shop_id)
        order.save()
        spare_part=spare_part_tb.objects.filter(id=cart[0].part_id_id).update(stock=left)
        c_obj=cart_tb.objects.filter(id=request.POST['cart_id']).delete()
        all_cart=cart_tb.objects.filter(user_id=request.session['user_id'])
        messages.add_message(request,messages.INFO,"Order Placed")
        return redirect('viewCart')
##        if(all_cart.count()>0):
##            return render(request,'view_cart.html',{'data':all_cart,'message':'Order Placed'})
##        else:
##            return render(request,'view_cart.html',{'msg':'Empty Cart','message':'Order Placed'})

@login_required
def cancelConfirm(request):
    cart=cart_tb.objects.filter(user_id=request.session['user_id'])
    return render(request,'view_cart.html',{'data':cart})

@login_required
def orderStatus(request):
    status=['cancelled','cancelling verified']
    orders=order_tb.objects.filter(user_id=request.session['user_id']).exclude(status__in=status).order_by('-id')
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
        if 'page' in request.session:
            page=request.session['page']
            del request.session['page']
        else:
            page=request.GET.get('page',1)
        #if 'page_number' in request.session:
           #page=request.session['page_number']
        paginator=Paginator(olist,2)
        try:
            all_orders=paginator.page(page)
        except PageNotAnInteger:
            all_orders=paginator.page(1)
        except EmptyPage:
            all_orders=paginator.page(paginator.num_pages)
        return render(request,'order_status.html',{'data':all_orders})
    else:
        return render(request,'order_status.html',{'msg':'No orders'})

@login_required
def payForOrder(request,oid,page):
    order=order_tb.objects.filter(id=oid)
    return render(request,'pay_for_order.html',{'data':order,'page':page})

@login_required
def payForOrderAction(request):
    uid=user_tb.objects.get(id=request.session['user_id'])
    account=bank_tb.objects.filter(credit_card_number=request.POST['c_c_n'],cvv=request.POST['cvv'],name=request.POST['name'])
    amount=float(request.POST['amount'])
    order=order_tb.objects.filter(id=request.POST['order_id'])
    if(account.count()>0):
        oid=order_tb.objects.get(id=request.POST['order_id'])
        sid=order[0].shop_id
        balance=float(account[0].balance)
        new_balance=balance-amount
        if(new_balance<2000):
            messages.add_message(request,messages.INFO,"Payment Failed : Check Your Balance")
            return redirect('payForOrder',oid=request.POST['order_id'],page=request.POST['orderpage'])
        else:
            request.session['page']=request.POST['orderpage']
            key=random.randint(100000,999999)
            payment=payment_tb(order_id=oid,amount=request.POST['amount'],transaction_key=key,date=datetime.date.today(),user_id=uid,shop_id=sid)
            payment.save()
            account.update(balance=new_balance)
            order.update(status="paid")
            notification=notification_tb.objects.filter(order_id=oid).update(status='read')
            messages.add_message(request,messages.INFO,"Payment Successful")
            return redirect('orderStatus')
    else:
        messages.add_message(request,messages.INFO,"invalid data")
        return redirect('payForOrder',oid=request.POST['order_id'],page=request.POST['orderpage'])
        

@login_required
def viewTrackingDetails(request,oid):
    t_details=tracking_details_tb.objects.filter(order_id=oid).order_by('-id')
    if(t_details.count()>0):
        return render(request,'view_tracking_details.html',{'data':t_details[0]})
    else:
        return render(request,'view_tracking_details.html',{'msg':'No Updates'})

@login_required
def cancelOrder(request,oid,page):
    request.session['page']=page
    order=order_tb.objects.filter(id=oid).update(status="cancelled")
    messages.add_message(request,messages.INFO,"Cancelling Successful")
    return redirect('orderStatus')

def part_list(parts):
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

def getSpareParts(request):
    vid=request.GET.get('vehicle')
    bid=request.GET.get('brand')
    mid=request.GET.get('model')
    cid=request.GET.get('category')
    part=request.GET.get('part_name')


    if((vid != '') and (bid == '') and (mid == '') and (cid == '') and (part == '')):
        
        spare_part=spare_part_tb.objects.filter(vehicle_id=vid)
        
    elif((vid != '') and (bid != '') and (mid == '') and (part == '') and (cid == '')):
        
        spare_part=spare_part_tb.objects.filter(vehicle_id=vid,brand_id=bid)
        
    elif((vid != '') and (bid != '') and (mid != '') and(part == '') and (cid == '')):
        
        spare_part=spare_part_tb.objects.filter(vehicle_id=vid,brand_id=bid,id__in=part_model_tb.objects.filter(model_id=mid).values('part_id'))

    elif((vid != '') and (bid != '') and (mid != '') and(cid != '') and (part == '')):

        spare_part=spare_part_tb.objects.filter(vehicle_id=vid,brand_id=bid,category_id=cid,id__in=part_model_tb.objects.filter(model_id=mid).values('part_id'))

    elif((part != '') and (vid == '') and (bid == '') and (mid == '') and (cid == '')):
        
        spare_part=spare_part_tb.objects.filter(part_name__contains=part)

    elif((part != '') and (vid != '') and (bid == '') and (mid == '') and (cid == '')):

        spare_part=spare_part_tb.objects.filter(vehicle_id=vid,part_name__contains=part)

    elif((part != '') and (vid != '') and (bid != '') and (mid == '') and (cid == '')):

        spare_part=spare_part_tb.objects.filter(vehicle_id=vid,brand_id=bid,part_name__contains=part)

    elif((cid  == '') and (part != '') and (vid != '') and (bid != '') and (mid != '')):
        
        spare_part=spare_part_tb.objects.filter(vehicle_id=vid,brand_id=bid,part_name__contains=part,id__in=part_model_tb.objects.filter(model_id=mid).values('part_id'))
        
    else:
        
        spare_part=spare_part_tb.objects.filter(vehicle_id=vid,brand_id=bid,category_id=cid,part_name__contains=part,id__in=part_model_tb.objects.filter(model_id=mid).values('part_id'))
    splist=part_list(spare_part)
    if(spare_part.count()>0):
        page=request.GET.get('page',1)
        parts=getPartsPages(splist,page)
        return render(request,'get_spare_parts.html',{'parts':parts,'vehicle':vid,'brand':bid,'model':mid,'category':cid,'part':part})
    else:
        return render(request,'get_spare_parts.html',{'msg':'No Spare Parts'})

def searchSparePart(request):
    p_name=request.GET.get('part_name')
    spare_part=spare_part_tb.objects.filter(part_name__contains=p_name)
    splist=part_list(spare_part)
    if(spare_part.count()>0):
        page=request.GET.get('page',1)
        parts=getPartsPages(splist,page)
        return render(request,'get_spare_parts.html',{'parts':parts,'part':p_name})
    else:
        return render(request,'get_spare_parts.html',{'msg':'No Spare parts'})
   

#def giveRatingAndReview(request):
    #order=order_tb.objects.filter(user_id=request.session['user_id'],status='delivered')
    #if(order.count()>0):
        #return render(request,'give_rating_review.html',{'data':order})
    #else:
        #return render(request,'give_rating_review.html',{'msg':'You have no successful orders'})
@login_required
def rateAndReview(request,oid):
    order=order_tb.objects.filter(id=oid)
    return render(request,'rate_and_review.html',{'part_id':order[0].part_id_id,'oid':oid})

@login_required
def rateAndReviewAction(request):
    pid=spare_part_tb.objects.get(id=request.POST['part_id'])
    uid=user_tb.objects.get(id=request.session['user_id'])
    rating_obj=rating_tb(part_id=pid,rating=request.POST['rating'],review=request.POST['review'],user_id=uid,date=datetime.date.today())
    rating_obj.save()
    part=spare_part_tb.objects.filter(id=request.POST['part_id'])
    messages.add_message(request,messages.INFO,"Added Successfully")
    return redirect('rateAndReview',oid=request.POST['oid'])

def viewReview(request,pid):
    reviews=rating_tb.objects.filter(part_id=pid).order_by('-id')
    if(reviews.count()>0):
        page=request.GET.get('page',1)
        part_reviews=getReviewPages(reviews,page)
        return render(request,'view_review.html',{'reviews':part_reviews})
    else:
        return render(request,'view_review.html',{'msg':'No reviews'})

def getReviewPages(reviews,page):
    paginator=Paginator(reviews,4)
    try:
        part_reviews=paginator.page(page)
    except PageNotAnInteger:
        part_reviews=paginator.page(1)
    except EmptyPage:
        part_reviews=paginator.page(paginator.num_pages)
    return part_reviews

@login_required
def viewPaymentDetails(request,oid):
    payment=payment_tb.objects.filter(order_id=oid)
    return render(request,'view_payment_details.html',{'data':payment})

@login_required
def writeComplaint(request):
    return render(request,'write_complaint.html')

@login_required
def writeComplaintAction(request):
    uid=user_tb.objects.get(id=request.session['user_id'])
    complaint=complaint_tb(user_id=uid,subject=request.POST['subject'],complaint=request.POST['complaint'],date=datetime.date.today())
    complaint.save()
    messages.add_message(request,messages.INFO,"Submitted successfully")
    return redirect('writeComplaint')

@login_required
def updateProfile(request):
    user=user_tb.objects.filter(id=request.session['user_id'])
    districts=district_tb.objects.all().exclude(id=user[0].district_id_id)
    return render(request,'update_profile_user.html',{'data':user,'districts':districts})

@login_required
def updateProfileAction(request):
    pro_img=""
    user=user_tb.objects.filter(id=request.session['user_id'])
    if(len(request.FILES)>0):
        pro_img=request.FILES['pro_img']
    else:
        pro_img=user[0].path
    name=request.POST['name']
    gender=request.POST['gender']
    address=request.POST['address']
    dob=request.POST['dob']
    place=request.POST['place']
    phone=request.POST['phone']
    email=request.POST['email']
    username=request.POST['username']
    password=request.POST['password']
    did=district_tb.objects.get(id=request.POST['district'])

    user_auth=User.objects.get(username=user[0].username)
    user_obj=user_tb.objects.get(id=request.session['user_id'])
    user_obj.path=pro_img
    user_obj.name=name
    user_obj.gender=gender
    user_obj.address=address
    user_obj.dob=dob
    user_obj.district_id=did
    user_obj.place=place
    user_obj.phone=phone
    user_obj.email=email
    user_obj.username=username
    user_obj.password=password
    user_obj.save()
    user_auth.username=username
    user_auth.set_password(password)
    user_auth.save()
    user_auth=auth.authenticate(username=username,password=password)
    auth.login(request,user_auth)
    request.session['user_id']=user[0].id
    messages.add_message(request,messages.INFO,"Updated sucessully")
    return redirect('updateProfile')

def nearbyWorkshop(request):
    districts=district_tb.objects.all()
    return render(request,'nearby_workshops.html',{'districts':districts})

def getNearbyWorkshop(request):
    did=request.GET.get('district')
    place=request.GET.get('place')
    if((did != '') and (place == '')):
        shop=workshop_tb.objects.filter(district_id=did)
    elif((did != '') and (place != '')):
        shop=workshop_tb.objects.filter(district_id=did,place__contains=place)
    
    
    if(shop.count()>0):
        page=request.GET.get('page',1)
        paginator=Paginator(shop,4)
        try:
            all_shop=paginator.page(page)
        except PageNotAnInteger:
            all_shop=paginator.page(1)
        except EmptyPage:
            all_shop=paginator.page(paginator.num_pages)
        return render(request,'get_nearby_workshops.html',{'data':all_shop,'district':did,'place':place})
    else:
        return render(request,'get_nearby_workshops.html',{'msg':'No Workshops'})

def viewServices(request,wid):
    services=service_tb.objects.filter(shop_id=wid)
    if(services.count()>0):
        page=request.GET.get('page',1)
        paginator=Paginator(services,4)
        try:
            all_services=paginator.page(page)
        except PageNotAnInteger:
            all_services=paginator.page(1)
        except EmptyPage:
            all_services=paginator.page(paginator.num_pages)
        return render(request,'view_services.html',{'data':all_services})
    else:
        return render(request,'view_services.html',{'msg':'No services'})

def viewWorkshopReviews(request,wid):
    reviews=workshop_review_tb.objects.filter(shop_id=wid).order_by('-id')
    if(reviews.count()>0):
        page=request.GET.get('page',1)
        all_reviews=reviewPages(reviews,page)
        return render(request,'view_workshop_reviews.html',{'workshop_id':wid,'reviews':all_reviews})
    else:
        return render(request,'view_workshop_reviews.html',{'workshop_id':wid,'msg':'No Reviews'})

def reviewPages(reviews,page):
    paginator=Paginator(reviews,3)
    try:
        all_reviews=paginator.page(page)
    except PageNotAnInteger:
        all_reviews=paginator.page(1)
    except EmptyPage:
        all_reviews=paginator.page(paginator.num_pages)
    return all_reviews

@login_required
def addReviewForWorkshop(request):
    sid=workshop_tb.objects.get(id=request.POST['shop_id'])
    uid=user_tb.objects.get(id=request.session['user_id'])
    review=workshop_review_tb(shop_id=sid,rating=request.POST['rating'],review=request.POST['review'],user_id=uid,date=datetime.date.today())
    review.save()
    reviews=workshop_review_tb.objects.filter(shop_id=sid).order_by('-id')
    workshop_id=request.POST['shop_id']
    page=request.GET.get('page',1)
    all_reviews=reviewPages(reviews,page)
    messages.add_message(request,messages.INFO,"Review Added Successfully")
    return redirect('viewWorkshopReviews',wid=workshop_id)


def partDetails(request,pid):
    part=spare_part_tb.objects.filter(id=pid)
    models=part_model_tb.objects.filter(part_id=pid)
    return render(request,'part_details.html',{'data':part,'models':models})

@login_required
def prebook(request,pid):
    part=spare_part_tb.objects.filter(id=pid)
    part_model=part_model_tb.objects.filter(part_id=pid)
    return render(request,'prebook.html',{'data':part,'part_model':part_model})

@login_required
def prebookAction(request):
    pid=spare_part_tb.objects.get(id=request.POST['pid'])
    sid=shop_tb.objects.get(id=request.POST['sid'])
    uid=user_tb.objects.get(id=request.session['user_id'])
    prebook=prebook_tb(part_id=pid,user_id=uid,shop_id=sid,count=request.POST['count'],date=datetime.date.today(),time=time.strftime("%H:%M:%S",time.localtime()))
    prebook.save()
    part=spare_part_tb.objects.filter(id=request.POST['pid'])
    messages.add_message(request,messages.INFO,"Request Sent")
    return redirect('prebook',pid=request.POST['pid'])

@login_required
def prebookingStatus(request):
    status=['ordered','cancelled']
    prebook=prebook_tb.objects.filter(user_id=request.session['user_id']).exclude(status__in=status).order_by('-id')
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
    #if(prebook.count()>0):
    page=request.GET.get('page',1)
        #if 'page_number' in request.session:
           #page=request.session['page_number']
    paginator=Paginator(olist,4)
    try:
        all_prebook=paginator.page(page)
    except PageNotAnInteger:
        all_prebook=paginator.page(1)
    except EmptyPage:
        all_prebook=paginator.page(paginator.num_pages)
    return render(request,'prebooking_status.html',{'data':all_prebook})
    #else:
    #return render(request,'prebooking_status.html',{'msg':'No prebookings'})

@login_required
def orderPrebook(request,pid):
    prebook=prebook_tb.objects.filter(id=pid)
    part_model=part_model_tb.objects.filter(part_id=prebook[0].part_id)
    return render(request,'order_prebook.html',{'data':prebook,'part_model':part_model})

@login_required
def confirmOrderAction(request):
    stock=int(request.POST['stock'])
    count=int(request.POST['count'])
    prebook=prebook_tb.objects.filter(id=request.POST['bid'])
    part=spare_part_tb.objects.filter(id=request.POST['pid'])
    if(count>stock):
        messages.add_message(request,messages.INFO,"Not enough stock")
        return redirect('orderPrebook',pid=request.POST['bid'])
    else:
        left=stock-count
        if(left != 0):
            new_stock=int(part[0].stock)+left
            part.update(stock=new_stock)
        order=order_tb(part_id=prebook[0].part_id,phone=request.POST['phone'],address=request.POST['address'],count=count,total_price=request.POST['cost'],
                       user_id=prebook[0].user_id,date=datetime.date.today(),time=time.strftime("%H:%M:%S",time.localtime()),prebook_id=request.POST['bid'],status='pending',shop_id=prebook[0].shop_id)
        order.save()
        prebook.update(status="ordered")
        notification=notification_tb.objects.filter(prebook_id=request.POST['bid']).update(status='read')
        status=['ordered','cancelled']
        prebookings=prebook_tb.objects.filter(user_id=request.session['user_id']).exclude(status__in=status)
        messages.add_message(request,messages.INFO,"Order Placed")
        return redirect('prebookingStatus')
##        if(prebookings.count()>0):
##            return render(request,'prebooking_status.html',{'data':prebookings,'message':'Order Placed'})
##        else:
##            return render(request,'prebooking_status.html',{'msg':'No prebookings','message':'Order Placed'})

@login_required
def cancelPrebook(request,pid):
    prebook=prebook_tb.objects.filter(id=pid)
    if(prebook[0].status == "approved"):
        part=spare_part_tb.objects.filter(id=prebook[0].part_id_id)
        new_stock=int(prebook[0].count)+int(part[0].stock)
        part.update(stock=new_stock)
    prebook.update(status="cancelled")
    status=['ordered','cancelled']
    prebook=prebook_tb.objects.filter(user_id=request.session['user_id']).exclude(status__in=status)
    return redirect('prebookingStatus')
##    if(prebook.count()>0):
##        return render(request,'prebooking_status.html',{'data':prebook})
##    else:
##        return render(request,'prebooking_status.html',{'msg':'No prebookings'})

def sparePartFromCategory(request,cid):
    spare_part=spare_part_tb.objects.filter(category_id=cid).order_by('-id')
    splist=part_list(spare_part)
    if(spare_part.count()>0):
        page=request.GET.get('page',1)
        parts=getPartsPages(splist,page)
        return render(request,'get_spare_parts.html',{'parts':parts})
    else:
        return render(request,'get_spare_parts.html',{'msg':'No Spare Parts'})

@login_required
def notification(request):
    notifications=notification_tb.objects.filter(status='unread',user_id=request.session['user_id']).order_by('-id')
    reply=reply_tb.objects.filter(user_id=request.session['user_id'],status='unread').order_by('-id')
    return render(request,'notification.html',{'data':notifications,'reply':reply})

@login_required
def readNotification(request,nid):
    notification=notification_tb.objects.filter(id=nid).update(status='read')
    return redirect('notification')

@login_required
def readReply(request,rid):
    reply=reply_tb.objects.filter(id=rid).update(status='read')
    return redirect('notification')

def getPartNames(request):
    part=''
    plist=[]
    if 'term' in request.GET:
        part=spare_part_tb.objects.filter(part_name__istartswith=request.GET.get('term'))
        for p in part:
            plist.append(p.part_name)
    return JsonResponse(plist,safe=False)

def getPlace(request):
    place=''
    plist=[]
    if 'term' in request.GET:
        place=workshop_tb.objects.filter(place__istartswith=request.GET.get('term'))
        for p in place:
           plist.append(p.place) 
    return JsonResponse(plist,safe=False)




    
    
    
