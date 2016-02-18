import datetime
import json
from app import app, db
from app.models.Machine import Machine
from app.models.Order import Order
from app.models.User import User
from app.models.product import Product


class Plan():
    def __init__(self):
        self.date = datetime.datetime.now()
        self.rough_plan = {}

    def plan(self):
        remaining_orders = Order.query.filter(Order.status == 'PLANNED').all()
        machines = Machine.query.all()
        employees = User.query.all()  # filter(User.status != 'in' or User.status != 'on_vacation' or User.status != 'on_holiday' or User.status == None)
        for order in remaining_orders:
            print Product.query.filter(Product.id == order.product_id)
        for employee in employees:
            print employee
        for machine in machines:
            print machine
        print len(remaining_orders)

        total_shift_time = 8 * len(machines)
        total_employees = len(employees)
        order_count = len(remaining_orders)

        print "Total Shift Time", total_shift_time
        print " Total Employees", total_employees
        print "Number of orders", order_count

        while (len(total_shift_time) > 0 and total_employees > 0 and order_count > 0):
            order = remaining_orders[0];
            product = Product.query.filter(Product.id == order.product_id)
            
