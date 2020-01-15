from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from order.models import Order,Container,Customer
from django.template.loader import get_template
from django.utils import timezone
import re

# Create your views here.

def home(request):
    orders=Order.objects.all()
    order_count=len(orders)
    containers=Container.objects.all()
    container_count=len(containers)
    customer_count=Customer.objects.count()
    response={}
    response['orders']=orders
    response['order_count']=len(orders)
    response['containers']=containers
    response['container_count']=len(containers)
    response['customer_count']=customer_count
    return render(request,'order/index.html',response)

def calendar(request):
    return render(request,'order/calender.html')

def submit_order(request):
    new_order=Order()
    last_order=Order.objects.last()
    today_date=timezone.now().date()
    if not last_order:
    	new_order.count_of_today=1
    elif last_order.order_date==today_date:
        new_order.count_of_today=last_order.count_of_today+1
    else:
        new_order.count_of_today=1
    new_order.order_number=today_date.strftime('%Y%m%d')+'%04d'%new_order.count_of_today
    new_order.customer_code=request.POST['customer_code']
    new_order.order_date=request.POST['order_date']
    new_order.assign_date=request.POST['assign_date']
    new_order.survey_locations=request.POST['survey_locations']
    new_order.depot_code=request.POST['depot_code']
    new_order.depot_name=request.POST['depot_name']
    new_order.unit_type=request.POST['unit_type']
    new_order.qty=request.POST['qty']
    new_order.release_number=request.POST['release_number']
    new_order.survey_code=request.POST['survey_code']
    new_order.remark=request.POST['remark']
    new_order.save()
    for i in range(int(request.POST['row_count'])):
        new_order.container_set.create(container_number=request.POST['container_number_%s'%(i+1)],content=request.POST['container_content_%s'%(i+1)])
    new_order.container_count=new_order.container_set.count()
    new_order.save()
    return HttpResponseRedirect('/')

def edit_order(request,order_number):
    response={}
    order=Order.objects.get(order_number=order_number)
    if request.POST.get('delete','false')=='true':
        order.delete()
        response['result']='succeed'
    else:
        order.customer_code=request.POST['customer_code']
        order.order_date=request.POST['order_date']
        order.assign_date=request.POST['assign_date']
        order.survey_locations=request.POST['survey_locations']
        order.depot_code=request.POST['depot_code']
        order.depot_name=request.POST['depot_name']
        order.unit_type=request.POST['unit_type']
        order.qty=request.POST['qty']
        order.release_number=request.POST['release_number']
        order.survey_code=request.POST['survey_code']
        order.remark=request.POST['remark']
        order.save()
        response['result']='succeed'
    return JsonResponse(response)

def submit_container(request):
    order_number=request.POST['order_number']
    container_number=request.POST['container_number']
    container_content=request.POST['container_content']
    order=Order.objects.get(order_number=order_number)
    order.container_set.create(container_number=container_number,content=container_content)
    order.container_count+=1
    order.save()
    return HttpResponseRedirect('/')

def order_container(request,order_number):
    order=Order.objects.get(order_number=order_number)
    containers=order.container_set.all()
    response={}
    for container in containers:
        response[container.container_number]={'customer_code':container.order.customer_code,'content':container.content}
    return JsonResponse(response)
