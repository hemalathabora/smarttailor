from django.urls import path
from . import views
from .views import tailor_productivity_chart
urlpatterns = [
    path('', views.home, name='home'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('tailor-dashboard/', views.tailor_dashboard, name='tailor_dashboard'),
    path('track-order/', views.track_order, name='track_order'),
    path('reorder/<int:order_id>/', views.reorder_editable, name='reorder_editable'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),
    path('estimated-measurements/', views.estimated_measurements, name='estimated_measurements'),
    path('tailor/productivity/', tailor_productivity_chart, name='tailor_productivity'),
    path('order/<int:order_id>/edit/', views.edit_order, name='edit_order'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('order/<int:order_id>/design/', views.customer_order_detail, name='customer_order_detail'),
]

