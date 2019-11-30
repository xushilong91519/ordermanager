from django.shortcuts import render
from django.http import HttpResponse
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
    new_order.order_number=''.join(re.split('[\s\-\+\.:]',str(timezone.now()))[0:7])
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
    orders=Order.objects.all()
    try:
        customer=Customer.objects.get(customer_code=request.POST['customer_code'])
    except:
        customer=Customer()
        customer.customer_code=request.POST['customer_code']
        customer.order_count=0
    customer.order_count+=1
    customer.save()
    customer_count=Customer.objects.count()
    containers=Container.objects.all()
    response={}
    response['orders']=orders
    response['order_count']=len(orders)
    response['containers']=containers
    response['container_count']=len(containers)
    response['customer_count']=customer_count
    return render(request,'order/index.html',response)

def edit_order(request,order_number):
    order=Order.objects.get(order_number=order_number)
    order.customer_code=request.POST['customer_code']
    order.survey_locations=request.POST['survey_locations']
    order.depot_code=request.POST['depot_code']
    order.depot_name=request.POST['depot_name']
    order.unit_type=request.POST['unit_type']
    order.release_number=request.POST['release_number']
    order.survey_code=request.POST['survey_code']
    order.remark=request.POST['remark']
    order.save()
    return render(request,'web1/order.html',locals())

def container_detail(request,container_number):
    container=Container.objects.get(container_number=container_number)
    return HttpResponse(container.content)
