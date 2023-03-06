from django.urls import path
from .views import (
    PlaceOrderView,
    ReceivePaymentView,
    OrderCompleteView,
    CustomerOrdersView,
    OrderDetailView,
)

app_name = "orders"

urlpatterns = [
    path("place_order/", PlaceOrderView.as_view(), name="place_order"),
    path("receive_payment/", ReceivePaymentView.as_view(), name="receive_payment"),
    path("order_complete/", OrderCompleteView.as_view(), name="order_complete"),
    path("my_orders/", CustomerOrdersView.as_view(), name="my_orders"),
    path("order/<str:order_number>/", OrderDetailView.as_view(), name="order_detail"),
]
