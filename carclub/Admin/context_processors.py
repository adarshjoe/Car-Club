from Admin.models import *
from User.models import *
from Spare_Parts_Shop.models import *
from Workshop.models import *

def get_part(parts):
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

def getData(request):
    user=''
    spare_part_shop=''
    workshop=''
    part_shop=''
    services=''
    w_reviews=''
    admin=''
    sales=''
    shop_signups=''
    workshop_signups=''
    orders=''
    not_count=0
    
    part_for_users=spare_part_tb.objects.all().exclude(stock='0').order_by('-id')[:9]
    splist=get_part(part_for_users)
    vehicles=vehicle_tb.objects.all()
    car_category=part_category_tb.objects.filter(vehicle_id=1)
    bike_category=part_category_tb.objects.filter(vehicle_id=2)
    
    if 'user_id' in request.session:
        user=user_tb.objects.filter(id=request.session['user_id'])
        notification=notification_tb.objects.filter(user_id=request.session['user_id'],status='unread')
        reply=reply_tb.objects.filter(user_id=request.session['user_id'],status='unread')
        not_count=notification.count()+reply.count()
    if 'spare_shop_id' in request.session:
        spare_part_shop=shop_tb.objects.filter(id=request.session['spare_shop_id'])
        parts=spare_part_tb.objects.filter(shop_id=request.session['spare_shop_id']).order_by('-id')[:6]
        part_shop=get_part(parts)
        status=['rejected','cancelling verified']
        orders=order_tb.objects.filter(shop_id=request.session['spare_shop_id']).exclude(status__in=status).order_by('-id')[:6]
    if 'workshop_id' in request.session:
        workshop=workshop_tb.objects.filter(id=request.session['workshop_id'])
        services=service_tb.objects.filter(shop_id=request.session['workshop_id']).order_by('-id')[:9]
        w_reviews=workshop_review_tb.objects.filter(shop_id=request.session['workshop_id']).order_by('-id')[:2]
    if 'admin_id' in request.session:
        admin=admin_tb.objects.filter(id=request.session['admin_id'])
        sales=payment_tb.objects.all().order_by('-id')[:6]
        shop_signups=shop_tb.objects.all().order_by('-id')[:3]
        workshop_signups=workshop_tb.objects.order_by('-id')[:3]
    return {
        'vehicles':vehicles,
        'car_category':car_category,
        'bike_category':bike_category,
        'user':user,
        'spare_part_shop':spare_part_shop,
        'workshop':workshop,
        'latest_parts':part_shop,
        'services':services,
        'workshop_reviews':w_reviews,
        'admin':admin,
        'sales':sales,
        'shop_signups':shop_signups,
        'workshop_signups':workshop_signups,
        'orders':orders,
        'part':splist,
        'notification_count':not_count,
    }
