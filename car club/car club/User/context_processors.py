from django.shortcuts import render,redirect
from Workshop.models import *
from Spare_Parts_Shop.models import *
from User.models import *
from Admin.models import *
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required

def userdata(request):
    if 'workshop_id' in request.session:
        workshop = workshop_tb.objects.filter(id=request.session['workshop_id']).first()
        return {'userdata': workshop}
    elif 'spare_shop_id' in request.session:
        spareshop = shop_tb.objects.filter(id=request.session['spare_shop_id']).first()
        return {'userdata': spareshop}
    elif 'user_id' in request.session:
        user = user_tb.objects.filter(id=request.session['user_id']).first()
        return {'userdata': user}
    elif 'admin_id' in request.session:
        admin = admin_tb.objects.filter(id=request.session['admin_id']).first()
        return {'userdata': admin}
    else:
        return {}