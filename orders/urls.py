from django.urls import path
from .views import PlaceOrderView, ReceivePaymentView, OrderCompleteView

app_name = "orders"

urlpatterns = [
    path("place_order/", PlaceOrderView.as_view(), name="place_order"),
    path("receive_payment/", ReceivePaymentView.as_view(), name="receive_payment"),
    path("order_complete/", OrderCompleteView.as_view(), name="order_complete"),
]
