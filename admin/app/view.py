import os
import os.path as op

from app import app, db
from flask_admin.contrib.sqla import ModelView
from model import Color, Machine, Product, Order, Shift, ProductionEntry, User, Role
from flask_admin.model.form import InlineFormAdmin
from flask_admin.form import thumbgen_filename, ImageUploadField
from jinja2 import Markup
from flask import url_for, redirect, render_template, request, abort, flash
from sqlalchemy.event import listens_for
from datetime import datetime
from util import display_time, color_boxes_html
from wtforms import Form
from wtforms_components import ColorField
from flask_security import login_required, current_user
from sqlalchemy.sql.expression import true
from sqlalchemy import and_
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.actions import action
from flask_admin.babel import gettext, ngettext


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

####################### Login Required View ###################
class RoleBasedModelView(ModelView):
    column_display_pk = True
    page_size = 20
    can_view_details = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            self.can_export = True
            self.can_view_details = True
        elif current_user.has_role('manager'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = False
            self.can_export = False
            elf.can_view_details = True
        elif current_user.has_role('lead'):
            self.can_create = False
            self.can_edit = True
            self.can_delete = False
            self.can_export = False
            self.can_view_details = False
        elif current_user.has_role('assembler'):
            self.can_create = False # read-only
            self.can_edit = False
            self.can_delete = False
            self.can_export = False
            self.can_view_details = False
        else:
            return False
        
        return True

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied abort(403)
                # Admin home
                flash("You don't have permission to access the page!", 'warning')
                return redirect(url_for('admin.index'))
            else:
                # login
                flash('You were successfully logged in', 'info')
                return redirect(url_for('security.login', next=request.url))

####################### Custom Model View ######################
class RoleModelView(ModelView):
    form_columns = (Role.name, Role.description)
    can_create = False
    can_edit = False
    can_delete = False
    column_display_pk = True
    page_size = 20

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        else:
            if current_user.has_role('admin'):
                self.can_create = True
            
            return True

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied abort(403)
                # Admin home
                flash("You don't have permission to access the page!", 'warning')
                return redirect(url_for('admin.index'))
            else:
                # login
                flash('You were successfully logged in', 'info')
                return redirect(url_for('security.login', next=request.url))


class UserModelView(RoleBasedModelView):
    column_list = ['photo', User.id, User.name, User.email, User.active, 'roles']
    
    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=thumbgen_filename(model.photo)))

    column_formatters = {
        'photo': _list_thumbnail
    }

    form_extra_fields = {
        'photo': ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)
    column_sortable_list = [ 'id', 'name', 'email', 'active']

    @action('enable', 'Enable', 'Are you sure you want to enable selected users?')
    def action_enable(self, ids):
        self.toggle_user_status(ids, True)

    @action('disable', 'Disable', 'Are you sure you want to disable selected users?')
    def action_disable(self, ids):
        self.toggle_user_status(ids, False)
    
    def toggle_user_status(self, ids, flag=False):
        try:
            query = User.query.filter(User.id.in_(ids))
            count = 0
            for user in query.all():
                if user.active != flag:
                    user.active = flag
                    count += 1
            
            if count > 0:
                self.session.commit()

            flash(ngettext('User was successfully disabled',
                '%(count)s users were successfully disabled',
                count,
                count=count))
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            
            flash(gettext('Failed to update user status. %(error)s',
            error=str(ex)), 'error')


class ShiftModelView(RoleBasedModelView):
    form_columns = (Shift.shift_name, Shift.start, Shift.end, Shift.total_hours)
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)
    column_list = [Shift.id, Shift.shift_name, Shift.start, Shift.end, Shift.total_hours]

class ColorModelView(RoleBasedModelView):
    #inline_models = (ColorInlineModelForm(Color),)
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

    form_columns = (Color.color_code, Color.name)
    
    #create_template = 'rule_create.html'
    #edit_template = 'rule_edit.html'
    column_list = [Color.id, Color.name, Color.color_code, 'color']

    def _color_box(view, context, model, name):
        html = '<div class="box" style="background: %s;"></div>' % model.color_code
        return Markup(html)
    
    column_formatters = {
        'color': _color_box
    }
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)

class MachineModelView(RoleBasedModelView):
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
                                                 filename=thumbgen_filename(model.photo)))

    column_formatters = {
        'photo': _list_thumbnail
    }

    form_extra_fields = {
        'photo': ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }
    form_columns = ('name','status', 'power_in_kilowatt', 'photo')
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)


class ProductModelView(RoleBasedModelView):
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
                url_for('static', filename=thumbgen_filename(model.photo))
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
        'photo': ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }
    # Create form fields adjustment.
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)


class OrderModelView(RoleBasedModelView):
    
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
                                                 filename=thumbgen_filename(model.photo)))

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
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)


class UserAjaxModelLoader(QueryAjaxModelLoader):
    # Overrides Team lead name loader
    def get_list(self, term, offset=0, limit=20):
        return (
            db.session.query(User).filter(and_(User.active == true(), User.roles.any(name='lead'))).all()
        )



class ProductionEntryModelView(RoleBasedModelView):
    # List table columns
    column_list = (
        'id', 'shift', 'date', 'machine_id', 'order', 'Product Photo', 'Colors', 'status',
        'user', 'remaining', 'num_good', 'num_bad'
    )

    column_sortable_list = [ 
        'id', 'shift', 'date', 'order', 'user', 
         'num_good', 'num_bad'
    ]

    column_filters = ('shift.shift_name', 'date', 'order.assigned_machine_id', 'order.status', 'order.remaining')
    column_labels = dict(user='Team Lead Name')
    # Sort entry by id descending order.
    column_default_sort = ('id', True)

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
        'user',
        ProductionEntry.num_hourly_good,
        ProductionEntry.num_hourly_bad
    )    
    form_ajax_refs = {
        'user': UserAjaxModelLoader(
            "user", db.session, User, fields=['name']
        )
    }

    def _colors(view, context, model, name):
        html = color_boxes_html(model.product_colors)
        return Markup(html)

    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % 
                url_for('static', filename=thumbgen_filename(model.photo))
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

