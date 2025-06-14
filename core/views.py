from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages

from smarttailor import settings
from .models import Customer, Fabric, Measurement, Order, Tailor
from datetime import datetime
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.core.files.storage import FileSystemStorage
from .predict_measurements import estimate_measurements
import random
import os
from datetime import datetime, timedelta
from collections import defaultdict
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncWeek
def home(request):
    return render(request, 'core/home.html')


def place_order(request):
    fabrics = Fabric.objects.all()
    tailors = Tailor.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        customer = Customer.objects.create(name=name, phone=phone, email=email, address=address)

        measurement = Measurement.objects.create(
            customer=customer,
            shoulder=float(request.POST['shoulder']),
            chest=float(request.POST['chest']),
            waist=float(request.POST['waist']),
            hip=float(request.POST['hip']),
            height=float(request.POST['height']),
            visual_notes=request.POST.get('visual_notes', '')
        )

        fabric = Fabric.objects.get(id=request.POST['fabric'])
        tailor = Tailor.objects.get(id=request.POST['tailor'])
        style_notes = request.POST['style_notes']
        delivery_date = request.POST['delivery_date']

        Order.objects.create(
            customer=customer,
            fabric=fabric,
            tailor=tailor,
            style_notes=style_notes,
            measurement=measurement,
            delivery_date=delivery_date
        )

        fabric.quantity_in_meters -= 2
        fabric.save()

        return render(request, 'core/order_success.html', {'customer': customer})

    return render(request, 'core/place_order.html', {'fabrics': fabrics, 'tailors': tailors})


def order_success(request):
    return render(request, 'core/order_success.html')
def track_order(request):
    orders = None
    query = ''
    if request.method == 'POST':
        query = request.POST['query']
        orders = Order.objects.filter(
            customer__email__icontains=query
        ) | Order.objects.filter(
            customer__phone__icontains=query
        )

    return render(request, 'core/track_order.html', {'orders': orders, 'query': query})

def tailor_dashboard(request):
    orders = Order.objects.all()

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("status")
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
        except Order.DoesNotExist:
            pass

        return redirect('tailor_dashboard')

    return render(request, 'core/tailor_dashboard.html', {'orders': orders})

def reorder_editable(request, order_id):
    original_order = get_object_or_404(Order, id=order_id)
    fabrics = Fabric.objects.all()
    tailors = Tailor.objects.all()

    if request.method == 'POST':
        customer = original_order.customer

        measurement = Measurement.objects.create(
            customer=customer,
            shoulder=request.POST['shoulder'],
            chest=request.POST['chest'],
            waist=request.POST['waist'],
            hip=request.POST['hip'],
            height=request.POST['height'],
            visual_notes=request.POST.get('visual_notes', '')
        )

        fabric = Fabric.objects.get(id=request.POST['fabric'])
        tailor = Tailor.objects.get(id=request.POST['tailor'])
        style_notes = request.POST['style_notes']
        delivery_date = request.POST['delivery_date']

        Order.objects.create(
            customer=customer,
            fabric=fabric,
            tailor=tailor,
            style_notes=style_notes,
            measurement=measurement,
            delivery_date=delivery_date
        )

        fabric.quantity_in_meters -= 2
        fabric.save()

        return render(request, 'core/order_success.html', {'customer': customer})

    return render(request, 'core/place_order.html', {
        'fabrics': fabrics,
        'tailors': tailors,
        'order': original_order,
        'measurement': original_order.measurement,
    })


def customer_dashboard(request):
    customer_orders = None
    query = ''

    if request.method == 'POST':
        query = request.POST['query']
        customer_orders = Order.objects.filter(
            customer__email__icontains=query
        ) | Order.objects.filter(
            customer__phone__icontains=query
        )

    return render(request, 'core/customer_dashboard.html', {
        'orders': customer_orders,
        'query': query
    })


def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template_path = 'core/invoice_template.html'
    context = {'order': order}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors generating the PDF')
    return response


def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_fabrics = Fabric.objects.count()
    total_tailors = Tailor.objects.count()
    total_customers = Customer.objects.count()
    recent_orders = Order.objects.order_by('-id')[:5]

    return render(request, 'core/admin_dashboard.html', {
        'total_orders': total_orders,
        'total_fabrics': total_fabrics,
        'total_tailors': total_tailors,
        'total_customers': total_customers,
        'recent_orders': recent_orders,
    })


def upload_photo(request):
    if request.method == 'POST' and request.FILES['photo']:
        photo = request.FILES['photo']
        fs = FileSystemStorage ()
        filename = fs.save (photo.name, photo)
        request.session['photo_filename'] = filename  # store for next view
        return redirect ('estimated_measurements')
    return render (request, 'core/upload_photo.html')


def estimated_measurements(request):
    filename = request.session.get('photo_filename')
    image_path = os.path.join(settings.MEDIA_ROOT, filename)

    estimated_data = estimate_measurements(image_path)

    if not estimated_data:
        messages.error(request, "Could not detect body landmarks. Try another photo.")
        return redirect('upload_photo')

    return render(request, 'core/estimated_measurement.html', {
        'photo_filename': filename,
        'estimated': estimated_data,
    })
def tailor_productivity_chart(request):
    tailor_id = request.GET.get('tailor')
    tailor_list = Tailor.objects.all()  # for dropdown

    if not tailor_id:
        return render(request, 'core/tailor_productivity.html', {
            'tailors': tailor_list,
            'message': 'Please select a tailor'
        })

    try:
        tailor = Tailor.objects.get(id=tailor_id)
    except Tailor.DoesNotExist:
        return render(request, 'core/tailor_productivity.html', {
            'tailors': tailor_list,
            'message': 'Invalid tailor selected'
        })

    # Filter orders for selected tailor
    orders = Order.objects.filter(tailor=tailor)

    if not orders.exists():
        return render(request, 'core/tailor_productivity.html', {
            'tailors': tailor_list,
            'selected_tailor': tailor,
            'message': 'No productivity data available.'
        })

    # Group by week number and month
    orders_per_week = defaultdict(int)
    orders_per_month = defaultdict(int)

    for order in orders:
        week = order.created_at.strftime('%Y-W%U')
        month = order.created_at.strftime('%Y-%m')
        orders_per_week[week] += 1
        orders_per_month[month] += 1

    context = {
        'tailors': tailor_list,
        'selected_tailor': tailor,
        'orders_per_week': dict (orders_per_week),
        'orders_per_month': dict (orders_per_month),
        'week_labels': list (orders_per_week.keys ()),
        'week_counts': list (orders_per_week.values ()),
        'month_labels': list (orders_per_month.keys ()),
        'month_counts': list (orders_per_month.values ()),
    }

    return render(request, 'core/tailor_productivity.html', context)

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    tailors = Tailor.objects.all()
    fabrics = Fabric.objects.all()

    if request.method == 'POST':
        order.tailor_id = request.POST.get('tailor')
        order.fabric_id = request.POST.get('fabric')
        order.style_notes = request.POST.get('style_notes')
        order.delivery_date = request.POST.get('delivery_date')
        order.status = request.POST.get('status')
        order.save()
        return redirect('order_list')  # Change this to your view name

    return render(request, 'core/edit_order.html', {
        'order': order,
        'tailors': tailors,
        'fabrics': fabrics,
        'status_choices': Order._meta.get_field('status').choices,
    })


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Cancelled'
    order.save()
    return redirect('track_order')
def customer_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST' and request.FILES.get('design_image'):
        order.design_image = request.FILES['design_image']
        order.save()
        return redirect('customer_order_detail', order_id=order.id)

    return render(request, 'core/customer_order_detail.html', {'order': order})