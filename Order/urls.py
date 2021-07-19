from django.urls import path
from. import views

urlpatterns = [
    path('order/', views.order, name="order"),
    path('order-summary/', views.order_summary, name="order-summary"),
    path('add-<pk>-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('remove-<pk>-from-cart/', views.remove_cart, name="remove-from-cart"),
    path('reduce-quantity-item/<pk>/', views.reduce_quantity, name="reduce-quantity"),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-gateway/', views.payment, name='payment-gateway'),
    path('payment-gateway-success/', views.payment_success, name='payment-success'),
    path('payment-gateway-failure/', views.payment_failure, name='payment-failure')
]