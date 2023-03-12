from datetime import datetime
import simplejson as json


def generate_order_number(pk):
    current_time = datetime.now().strftime("%d%m%Y%H%M%S%f")
    order_number = current_time + str(pk)
    return order_number


def order_total_for_each_restaurant(order, restaurant_id):
    subtotal = 0
    tax = 0
    tax_data = {}
    order_data = json.loads(order.total_data).get(str(restaurant_id))
    for key, val in order_data.items():
        subtotal += float(key)
        val = val.replace("'", '"')
        tax_data.update(json.loads(val))
        # {'GST': {'17.00': '6.80'}, 'VAT': {'5.00': '2.00'}}
        for t_type in tax_data:
            for t_per in tax_data[t_type]:
                tax += float(tax_data[t_type][t_per])
        grand_total = float(subtotal) + float(tax)
        context = {
            "subtotal": subtotal,
            "grand_total": grand_total,
            "tax_data": tax_data,
        }
        return context
