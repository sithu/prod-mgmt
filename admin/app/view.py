import os
import os.path as op

from app import app, db
from flask_admin.contrib.sqla import ModelView
from model import Color, Machine, Product, Order, Shift, ProductionEntry
from flask_admin.form import rules
from flask_admin.model.form import InlineFormAdmin
from flask_admin import form
from jinja2 import Markup
from flask import url_for
from sqlalchemy.event import listens_for
from datetime import datetime
from util import display_time, color_boxes_html
from wtforms import validators, RadioField, TextField
from flask_wtf import Form
from wtforms_components import ColorField

# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass

@listens_for(Machine, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.photo_url))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.photo_url)))
        except OSError:
            pass


class ShiftModelView(ModelView):
    column_display_pk = True
    form_columns = (Shift.shift_name, Shift.start_hour, Shift.end_hour)


class ColorInlineModelForm(InlineFormAdmin):
    form_columns = ('name', 'color_code')


class ColorModelView(ModelView):
    #inline_models = (ColorInlineModelForm(Color),)
    column_display_pk = True
    column_hide_backrefs = False
    column_searchable_list = (Color.name, Color.color_code)
    #form_excluded_columns = (Color.name)
    #inline_models = (Color,)
    # Use same rule set for edit page
    #form_edit_rules = form_create_rules
    # form_extra_fields = {
    #     'extra': ColorField()
    # }
    form_overrides = {
        'color_code': ColorField,
    }

    form_columns = (Color.name, Color.color_code)
    
    #create_template = 'rule_create.html'
    #edit_template = 'rule_edit.html'
    column_list = [Color.id, Color.name, Color.color_code, 'color']

    def _color_box(view, context, model, name):
        html = '<div class="box" style="background: %s;"></div>' % model.color_code
        return Markup(html)
    
    column_formatters = {
        'color': _color_box
    }

class MachineModelView(ModelView):
    column_display_pk = True
    column_exclude_list = ['created_at']
    # Rename columns
    column_labels = dict(order_to_machine='Order')
    #column_filters = ('id','name','status','updated_at')
    column_list = [Machine.id, Machine.name, Machine.status, 'order_to_machine']
    column_searchable_list = (Machine.id, Machine.name, Machine.status)
    #column_select_related_list = (Machine.id, Machine.name, Machine.status)
    #form_edit_rules = form_create_rules
    #form_excluded_columns = (Color.name)
    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.photo)))

    column_formatters = {
        'photo': _list_thumbnail
    }
    form_columns = ('name','status', 'power_in_kilowatt')
    

class ProductModelView(ModelView):
    column_display_pk = True
    column_exclude_list = ['created_at', 'updated_at']
    # Rename 'title' columns to 'Post Title' in list view
    column_list = (
        Product.id, Product.name, Product.photo, 'colors', Product.weight, 
        Product.time_to_build, Product.num_employee_required, 'machine',
        Product.raw_material_weight_per_bag, Product.multi_colors_ratio
    )
    # List column renaming
    column_labels = dict(selling_price='Price', num_employee_required='Employee Required', machine='Default Machine')
    
    def _colors(view, context, model, name):
        html = color_boxes_html(model.colors)
        return Markup(html)

    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % 
                url_for('static', filename=form.thumbgen_filename(model.photo))
            )

    column_formatters = {
        'photo': _list_thumbnail,
        'colors': _colors
    }

    form_columns = (
        'name',
        'photo',
        'colors',
        'multi_colors_ratio',
        'machine',
        'weight',
        'time_to_build',
        'selling_price',
        'num_employee_required',
        'raw_material_weight_per_bag',
    )

    form_ajax_refs = {
        'colors': {
            'fields': (Color.name,)
        },
        'machine': {
            'fields': (Machine.id, Machine.name,)
        }
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'photo': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }
    # Create form fields adjustment.


class OrderModelView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

    def __init__(self, session, name=None, category=None, endpoint=None, url=None, static_folder=None, menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        super(OrderModelView, self).__init__(Order, session, name, category, endpoint, url, static_folder, menu_class_name, menu_icon_type, menu_icon_value)

    # Create form fields
    form_columns = (
        'name',
        'product',
        'quantity',
        'assigned_machine',
        'note'
    )

    form_ajax_refs = {
        'product': {
            'fields': (Product.name,)
        },
        'assigned_machine': {
            'fields': (Machine.id, Machine.name,)
        }
    }

    def _colors(view, context, model, name):
        html = color_boxes_html(model.product_colors)
        return Markup(html)

    def _time_to_complete(view, context, model, name):
        return display_time(model.estimated_time_to_complete)

    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.photo)))

    column_formatters = {
        'Product Photo': _list_thumbnail,
        'Time To Complete': _time_to_complete,
        'Colors': _colors
    }

    # List table columns
    column_list = (
        Order.id, Order.name, 'product', 'Product Photo', 'Colors', Order.status,
        Order.quantity, 'completed', 'Time To Complete',
        Order.raw_material_quantity,
        Order.assigned_machine_id,
        Order.production_start_at, Order.production_end_at,
        Order.note
    )

    column_sortable_list = [ 'id', 'name', 'product', 'status', 
        'quantity', 'completed', 'estimated_time_to_complete',
        'assigned_machine_id',
        'raw_material_quantity', 'production_start_at', 'production_end_at'
    ]
    column_searchable_list = (Order.id, Order.name)
    column_filters = ('status',)


class ProductionEntryModelView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

    # List table columns
    column_list = (
        'id', 'shift', 'date', 'machine_id', 'order', 'Product Photo', 'Colors', 'status',
        'team_lead_name', 'remaining', 'num_good', 'num_bad'
    )

    column_sortable_list = [ 
        'id', 'shift', 'date', 'order', 'team_lead_name', 
         'num_good', 'num_bad'
    ]

    column_filters = ('shift.shift_name', 'date', 'order.assigned_machine_id', 'order.status', 'order.remaining')

    # Create form fields
    def order_status_filter():
        return db.session.query(Order).filter(Order.status != 'COMPLETED')

    form_args = dict(
        order = dict(label='For Order', query_factory=order_status_filter)
    )

    form_columns = (
        'shift',
        'order',
        'date',
        ProductionEntry.team_lead_name,
        ProductionEntry.num_hourly_good,
        ProductionEntry.num_hourly_bad
    )    

    def _colors(view, context, model, name):
        html = color_boxes_html(model.product_colors)
        return Markup(html)

    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % 
                url_for('static', filename=form.thumbgen_filename(model.photo))
            )

    column_formatters = {
        'Product Photo': _list_thumbnail,
        'Colors': _colors
    }
    
    def on_model_change(self, form, model, is_created=False):
        if is_created:
            print "======== creating ======="
        else:
            print "======== updating ======="
            if model.num_hourly_good or model.num_hourly_bad:
                print "progress"
                model.order.status = 'IN_PROGRESS'
                model.order.production_start_at = datetime.now()


class ProductionEntryWorkerModelView(ModelView):
    column_display_pk = True
    column_hide_backrefs = True

    def get_query(self):
        return self.session.query(self.model).filter(self.model.active == True)
    
    # List table columns
    list_columns = (
        'id', 'shift', 'date', 'machine_id', 'order', 'Product Photo', 'Colors', 'status',
        'team_lead_name', 'remaining', 'num_good', 'num_bad'
    )

    column_sortable_list = [ 
        'id', 'shift', 'date', 'order', 'team_lead_name', 
         'num_good', 'num_bad'
    ]

    column_filters = ('shift.shift_name', 'date', 'order.assigned_machine_id', 'order.status', 'order.remaining')

    # Create form fields
    form_columns = (
        'shift',
        'order',
        'date',
        ProductionEntry.team_lead_name,
        ProductionEntry.num_hourly_good,
        ProductionEntry.num_hourly_bad
    )    

    def _colors(view, context, model, name):
        html = color_boxes_html(model.product_colors)
        return Markup(html)

    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % 
                url_for('static', filename=form.thumbgen_filename(model.photo))
            )

    column_formatters = {
        'Product Photo': _list_thumbnail,
        'Colors': _colors
    }
    
    def on_model_change(self, form, model, is_created=False):
        if is_created:
            print "======== creating ======="
        else:
            print "======== updating ======="
            if model.num_hourly_good or model.num_hourly_bad:
                print "progress"
                model.order.status = 'IN_PROGRESS'
                model.order.production_start_at = datetime.now()

