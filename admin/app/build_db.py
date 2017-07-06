import datetime
from app import app, db
from app.model import Color, Machine, Product, Shift, Order, ProductionEntry, Role, User
from colour import Color as HtmlColor
from flask_security.utils import encrypt_password

def build_sample_db(user_datastore):
    db.drop_all()
    db.create_all()
    print "####### Creating test data ########"
    create_colors()
    create_machines()
    create_shift()
    create_product()
    create_order()
    create_production_entry()
    db.session.commit()
    create_role_and_user(user_datastore)


def create_colors():
    print "Creating Color..."
    color_names = [
        'Smoke White', 'Salmon', 'Green', 'Teal'
    ]
    color_codes = [
        '#F5F5F5', '#FA8072', '#008000', '#008080'
    ]

    for i in range(len(color_names)):
        color = Color()
        color.color_code = HtmlColor(color_codes[i])
        color.name = color_names[i]
        db.session.add(color)


def create_machines():
    print "Creating Machine..."
    names = [ 'Machine A', 'Machine B', 'Machine C', 'Machine D' ]
    kw = [ 1000, 1500, 2000, 2500 ]

    for i in range(len(names)):
        m = Machine()
        m.name = names[i]
        m.status = 'OFF'
        m.power_in_kilowatt = kw[i]
        db.session.add(m)


def create_shift():
    print "creating Shifts..."
    shifts = [ ('Morning', 8, 16), ('Evening', 16, 24), ('Night', 24, 8)]
    for t in shifts:
        s = Shift()
        s.shift_name = t[0]
        s.start_hour = t[1]
        s.end_hour = t[2]
        db.session.add(s)


def create_product():
    print "creating Products..."
    products = [
        ('Chair', 'chair.jpg', '50%-50%', 100, 15, 1000, 3, 1000, 1, 1),
        ('Round Table', 'round_table.jpg', '50%-50%', 200, 25, 2000, 2, 1000, 2, 2)    
    ]
    for p in products:
        product = Product()
        product.name = p[0]
        product.photo = p[1]
        product.multi_colors_ratio = p[2]
        product.weight = p[3]
        product.time_to_build = p[4]
        product.selling_price = p[5]
        product.num_employee_required = p[6]
        product.raw_material_weight_per_bag = p[7]
        machine = Machine.query.get(p[8])
        product.machine_id = machine.id
        color = Color.query.get(p[9])
        product.colors = [color]
        db.session.add(product)


def create_order():
    print "creating order..."
    orders = [
        ('Chair x 1000 Orders', 1, 1000),
        ('Round Table x 2000 Orders', 2, 2000)        
    ]
    for o in orders:
        order = Order()
        order.name = o[0]
        order.product_id = o[1]
        order.quantity = o[2]
        db.session.add(order)


def create_production_entry():
    print "creating production entry..."
    entries = [
        (1, 1, 'Ko Maung'),
        (1, 2, 'Ko Soe')      
    ]
    for e in entries:
        pEntry = ProductionEntry()
        pEntry.shift_id = e[0]
        pEntry.order_id = e[1]
        pEntry.team_lead_name = e[2]
        db.session.add(pEntry)
        

def create_role_and_user(user_datastore):
    with app.app_context():
        print "creating role..."
        admin_role = Role(name='admin')
        create_and_edit_role = Role(name='create_and_edit')
        edit_role = Role(name='edit')
        read_role = Role(name='read')
        db.session.add(admin_role)
        db.session.add(create_and_edit_role)
        db.session.add(edit_role)
        db.session.add(read_role)
        
        print "creating user..."
        admin_user = user_datastore.create_user(
            name='Admin',
            email='admin@gmail.com',
            password=encrypt_password('admin'),
            roles=[admin_role]
        )

        user_datastore.create_user(
            name='Create Edit',
            email='create_edit@gmail.com',
            password=encrypt_password('createedit'),
            roles=[create_and_edit_role]
        )

        user_datastore.create_user(
            name='Edit',
            email='edit@gmail.com',
            password=encrypt_password('edit'),
            roles=[edit_role]
        )

        first_names = [
            'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
            'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
            'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
        ]
        last_names = [
            'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
            'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
            'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
        ]

        for i in range(len(first_names)):
            tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
            user_datastore.create_user(
                name=first_names[i] + " " + last_names[i],
                email=tmp_email,
                password=encrypt_password('user'),
                roles=[read_role,]
            )

        db.session.commit()
    return

