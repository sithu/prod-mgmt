from app import db
from model import Product, Order, ProductionEntry, OrderHistory, ProductionEntryHistory

def init_logger():
    import logging
    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG
    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)


def test_job(a, b):
    print(str(a) + ' ' + str(b))
    #app.logger.info('Scheduler Running:' + str(a) + ' ' + str(b))

def archive_orders_job():
    print "@@@@@@@@@ archive orders job @@@@@@@@@@"
    orders = db.session.query(Order).filter(Order.status == 'COMPLETED').all()
    print "num completed orders = %d" % len(orders)
    if len(orders) < 1:
        return

    try:
        count = 0
        for o in orders:
            print "completed = %d, product = %s" % (o.completed, o.photo)
            oh = OrderHistory()
            oh.id = int(o.id)
            oh.name = str(o.name)
            oh.quantity = int(o.quantity)
            oh.product_id = int(o.product_id)
            oh.product_name = str(o.product.name)
            oh.raw_material_quantity = int(o.raw_material_quantity)
            oh.estimated_time_to_complete = int(o.estimated_time_to_complete)
            oh.machine_id = int(o.assigned_machine_id)
            oh.machine_name = o.assigned_machine.name
            oh.photo = str(o.photo)
            oh.production_start_at = o.production_start_at
            oh.production_end_at = o.production_end_at
            oh.note = str(o.note)

            db.session.add(oh)
            count += 1

            for e in o.production_entry_orders:
                print "production entry good = %d vs bad = %d" % (e.num_good, e.num_bad)
                assemblers = [ m.name for m in e.members ]
                assembler_names = ','.join(assemblers)

                eh = ProductionEntryHistory()
                eh.id = e.id
                eh.date = e.date
                eh.shift_name = e.shift.name
                eh.order_id = oh.id
                eh.lead = e.lead.name
                eh.assemblers = str(assembler_names)
                eh.num_hourly_good = str(e.num_hourly_good)
                eh.num_hourly_bad = str(e.num_hourly_bad)
                eh.num_good = e.num_good
                eh.num_bad = e.num_bad
                eh.machine_id = e.machine_id
                eh.photo = oh.photo

                db.session.add(eh)
                db.session.delete(e)
            
            db.session.delete(o)
        
        if count > 0:
            db.session.commit()
            print "successfully committed."
    except Exception as ex:
        print "@@@@@@@@@@@@@@@ Something went wrong @@@@@@@@@@@@"
        print ex

