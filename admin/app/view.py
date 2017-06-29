import os
import os.path as op

from flask_admin.contrib.sqla import ModelView
from model import Color, Machine, Product, Order, Shift, ProductionEntry
from flask_admin.form import rules
from flask_admin.model.form import InlineFormAdmin
from flask_admin import form
from jinja2 import Markup
from flask import url_for
from sqlalchemy.event import listens_for
from datetime import datetime

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


class MyModelView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

class ColorInlineModelForm(InlineFormAdmin):
    form_columns = ('name', 'color_code')


class ColorModelView(ModelView):
    #inline_models = (ColorInlineModelForm(Color),)
    column_display_pk = True
    column_hide_backrefs = False
    form_columns = (Color.name, Color.color_code)
    column_searchable_list = (Color.name, Color.color_code)
    #form_excluded_columns = (Color.name)
    #inline_models = (Color,)

    # Use same rule set for edit page
    #form_edit_rules = form_create_rules

    #create_template = 'rule_create.html'
    #edit_template = 'rule_edit.html'

    
class MachineModelView(ModelView):
    column_display_pk = True
    column_exclude_list = ['created_at']
    #column_filters = ('id','name','status','updated_at')
    column_list = [Machine.id, Machine.name, Machine.status, Machine.updated_at]
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
    
    form_columns = (Machine.name, Machine.status, Machine.power_in_kilowatt, 'photo')
    form_extra_fields = {
        'photo': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }
    

class ProductModelView(ModelView):
    column_display_pk = True
    column_exclude_list = ['created_at', 'updated_at']
    # Rename 'title' columns to 'Post Title' in list view
    column_list = (
        Product.id, Product.name, Product.photo, Product.weight, 
        Product.time_to_build, Product.num_employee_required, 'machine',
        Product.raw_material_weight_per_bag, 'colors', Product.multi_colors_ratio
    )
    # List column renaming
    column_labels = dict(selling_price='Price', num_employee_required='Employee Required', machine='Default Machine')
    
    # column_hide_backrefs = False
    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.photo)))

    column_formatters = {
        'photo': _list_thumbnail
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

    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.photo)))

    column_formatters = {
        'Product Photo': _list_thumbnail
    }

    # List table columns
    column_list = (
        Order.id, Order.name, 'product', 'Product Photo', Order.status,
        Order.quantity, 'completed', 'progress', Order.estimated_time_to_complete,
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
    column_hide_backrefs = True

    # Create form fields
    form_columns = (
        'shift',
        'order',
        'date',
        ProductionEntry.team_lead_name,
        ProductionEntry.num_hourly_good,
        ProductionEntry.num_hourly_bad
    )
    
    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.photo)))

    column_formatters = {
        'Product Photo': _list_thumbnail
    }

    # List table columns
    column_list = (
        'id', 'shift', 'date', 'order', 'Product Photo', 'status',
        'team_lead_name', 'remaining', 'num_good', 'num_bad'  
    )
    
    
    def on_model_change(self, form, model, is_created=False):
        if is_created:
            print "======== creating ======="
        else:
            print "======== updating ======="
            if model.num_hourly_good or model.num_hourly_bad:
                print "progress"
                model.order.status = 'IN_PROGRESS'
                model.order.production_start_at = datetime.now()

