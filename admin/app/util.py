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


def image_icon_html(model):
    if not model.photo:
        return ''

    html = '<a href="%s"><img src="%s" width="50" height="50"></a>' % (
        url_for('order.edit_view', id=model.id, url=url_for('order.index_view')),    
        url_for('static', filename=thumbgen_filename(model.photo))
    )
    
    return html

