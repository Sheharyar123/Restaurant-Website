from datetime import datetime


def generate_order_number(pk):
    current_time = datetime.now().strftime("%d%m%Y%H%M%S%f")
    order_number = current_time + str(pk)
    return order_number
