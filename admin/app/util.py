from flask_admin.form import thumbgen_filename
from jinja2 import Markup
from flask import url_for

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def color_boxes_html(colors):
    html = ''
    for color in colors:
        html += '<div class="box" style="background: %s;"></div>' % color.color_code
    
    return html


def image_icon_html(model, count=None):
    if not model.photo:
        return ''
    
    num_worker = ''
    if count:
        num_worker = '<i class="glyphicon glyphicon-user">x%s</i>' % str(count)

    html = '<a href="%s"><img src="%s" width="50" height="50">%s</a>' % (
        url_for('order.edit_view', id=model.id, url=url_for('order.index_view')),    
        url_for('static', filename=thumbgen_filename(model.photo)),
        num_worker
    )
    
    return html


def href_link_html(model_id, model_name):
    if not model_id or not model_name:
        return ''

    html = '<a href="%s">%d</a>' % (
        url_for(model_name + '.edit_view', id=model_id, url=url_for(model_name + '.index_view')),
        model_id 
    )
    
    return html

def slot_lead_to_machine(leads, machines):
    resources = []
    count = 0
    lead = leads.pop()
    for m in machines:
        ratio = int(m.machine_to_lead_ratio.split('-')[0])
        if len(leads) > 0 and count >= ratio:
            lead = leads.pop()
            count = 1 # reset 0 and just pop() above (1). So, sets to 1
        else:
            count += 1

        resources.append(lead)

    return (resources, leads)