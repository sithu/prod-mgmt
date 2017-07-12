import os
import os.path as op

from app import app, db
from flask_admin.contrib.sqla import ModelView
from model import Color, Machine, Product, Order, Shift, ProductionEntry, User, Role, Team, TeamRequest
from flask_admin.model.form import InlineFormAdmin
from flask_admin.form import thumbgen_filename, ImageUploadField, rules, DateTimeField, Select2Field
from jinja2 import Markup
from flask import url_for, redirect, render_template, request, abort, flash
from sqlalchemy.event import listens_for
from datetime import datetime, timedelta
from util import display_time, color_boxes_html, image_icon_html, href_link_html
from wtforms import Form, SelectMultipleField, RadioField, validators, TextField
from wtforms_components import ColorField, DateField
from wtforms.validators import Required
from flask_security import login_required, current_user
from sqlalchemy.sql.expression import true
from sqlalchemy import and_
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.actions import action
from flask_admin.babel import gettext, ngettext
from flask_admin.model.typefmt import BASE_FORMATTERS, list_formatter


# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass

# TODO - handle for other models with photo
# https://github.com/flask-admin/flask-admin/blob/master/examples/forms/app.py#L67
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

####################### Formatters ############################
def date_format(view, value):
    return value.strftime('%d.%m.%Y %H:%M:%S')

def timestamp_formatter(view, context, model, name):
    field = getattr(model, name, None)
    if field and field.strftime("%Y-%m-%d %I:%M:%S"):
        d = datetime.now() - field
        return display_time(int(d.total_seconds())) + " ago"
    else:
        return ''

# MY_DEFAULT_FORMATTERS = dict(BASE_FORMATTERS)
# MY_DEFAULT_FORMATTERS.update({
#     date: date_format
# })


####################### Login Required View ###################
class RoleBasedModelView(ModelView):
    column_display_pk = True
    page_size = 20
    can_view_details = True
    # column_type_formatters = MY_DEFAULT_FORMATTERS

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
    details_modal = True

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
    details_modal = True
    edit_modal = True
    column_list = ['photo', User.id, User.name, User.gender, User.is_in, 'shift', 'roles', User.active, User.email]
    
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
                                      thumbnail_size=(75, 75, True))
    }
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)
    column_sortable_list = [ 'id', 'name', 'email', 'active', 'is_in', 'gender']
    column_filters = ('id', 'name','gender', 'is_in', 'active', 'email', 'shift.name', 'roles.name')
    
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
    details_modal = True
    edit_modal = True
    form_columns = (Shift.name, Shift.start, Shift.end, Shift.total_hours)
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)
    column_list = [Shift.id, Shift.name, Shift.start, Shift.end, Shift.total_hours]

class ColorModelView(RoleBasedModelView):
    details_modal = True
    edit_modal = True
    #inline_models = (ColorInlineModelForm(Color),)
    column_hide_backrefs = False
    column_searchable_list = (Color.id, Color.name, Color.color_code)
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
    column_filters = ('id', 'name')
    

class MachineModelView(RoleBasedModelView):
    details_modal = True
    edit_modal = True
    column_exclude_list = ['created_at']
    column_list = [Machine.id, Machine.name, Machine.status, 'machine_to_lead_ratio', Machine.average_num_workers, 'orders']
    column_searchable_list = (Machine.id, Machine.name, Machine.status)
    column_labels = dict(
        average_num_workers='Scheduled Assemblers', machine_to_lead_ratio='Lead to Machine Ratio'
    )

    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=thumbgen_filename(model.photo)))

    def _all_orders(view, context, model, name):
        non_completed_orders = db.session.query(Order).filter(and_(Order.assigned_machine_id == model.id, Order.status != 'COMPLETED')).all()
        html = ''
        is_first = True
        for o in non_completed_orders:
            if is_first:
                is_first = False
                html += image_icon_html(o, o.product.num_employee_required)
            else:
                html += image_icon_html(o)

        return Markup(html)

    def _planned_workers(view, context, model, name):
        html = '<i class="glyphicon glyphicon-user">x%s</i>' % str(model.average_num_workers)
        return Markup(html)


    column_formatters = {
        'photo': _list_thumbnail,
        'orders': _all_orders,
        'average_num_workers': _planned_workers
    }

    form_extra_fields = {
        'photo': ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(75, 75, True))
    }
    form_columns = ('name','status', 'power_in_kilowatt', 'photo', 'average_num_workers', 'machine_to_lead_ratio')
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)
    column_filters = ('id', 'name', 'status', 'machine_to_lead_ratio')


class ProductModelView(RoleBasedModelView):
    details_modal = True
    edit_modal = False
    column_exclude_list = ['created_at', 'updated_at']
    # Rename 'title' columns to 'Post Title' in list view
    column_list = (
        Product.id, Product.name, Product.photo, 'colors', 'weight', 
        Product.time_to_build, Product.num_employee_required, 'machine',
        Product.raw_material_weight_per_bag, Product.multi_colors_ratio
    )
    # List column renaming
    column_labels = dict(
        selling_price='Price', num_employee_required='Employee Required', 
        machine='Default Machine', weight='Weight (g)',
        time_to_build='Time To Build (sec)', 
        raw_material_weight_per_bag='Raw Material Unit Weight (g)'
    )
    
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
                                      thumbnail_size=(75, 75, True))
    }
    # Create form fields adjustment.
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)
    column_filters = ('id', 'name', 'weight', 'time_to_build', 'num_employee_required', 'machine.name', 'raw_material_weight_per_bag')


class OrderModelView(RoleBasedModelView):
    details_modal = True
    edit_modal = True
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
        'assigned_machine': QueryAjaxModelLoader('assigned_machine', db.session, Machine,
        filters=["status!='NOT_IN_USE'"],
        fields=['id', 'name'], page_size=10)
    }

    def _colors(view, context, model, name):
        html = color_boxes_html(model.product_colors)
        return Markup(html)

    def _time_to_complete(view, context, model, name):
        return display_time(model.estimated_time_to_complete)

    def _production_entries(view, context, model, name):
        html = ''
        for entry in model.production_entry_orders:
            html += href_link_html(entry.id, 'productionentry')
        
        return Markup(html)


    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=thumbgen_filename(model.photo)))

    column_formatters = {
        'Product Photo': _list_thumbnail,
        'Time To Complete': _time_to_complete,
        'Colors': _colors,
        'production_start_at': timestamp_formatter,
        'production_end_at': timestamp_formatter,
        'production_entry_orders': _production_entries
    }

    # List table columns
    column_list = (
        Order.id, Order.name, 'product', 'Product Photo', 'Colors', Order.status,
        Order.quantity, 'completed', 'Time To Complete',
        'production_entry_orders',
        Order.raw_material_quantity,
        Order.assigned_machine_id,
        Order.production_start_at, Order.production_end_at
    )

    column_sortable_list = [ 'id', 'name', 'product', 'status', 
        'quantity', 'completed', 'estimated_time_to_complete',
        'assigned_machine_id',
        'raw_material_quantity', 'production_start_at', 'production_end_at'
    ]
    
    column_searchable_list = (Order.id, Order.name, Order.status)
    column_filters = (
        'id', 'name', 'status', 'quantity', 'estimated_time_to_complete', 'raw_material_quantity',
        'assigned_machine_id'
    )
    
    # List column renaming
    column_labels = dict(
        production_entry_orders='Production Entries', 
        estimated_time_to_complete='Estimated Time', 
        production_start_at='Production Start',
        production_end_at='Production End',
        assigned_machine_id='Machine Id'
    )
    
    # Sort the data by id in descending order.
    column_default_sort = ('id', True)


class UserLeadAjaxModelLoader(QueryAjaxModelLoader):
    # Overrides Team lead name loader
    def get_list(self, term, offset=0, limit=10):
        return (
            db.session.query(User).filter(and_(User.active == true(), User.roles.any(name='lead'))).all()
        )

class UserAssemblerAjaxModelLoader(QueryAjaxModelLoader):
    # Overrides Team assember name loader
    def get_list(self, term, offset=0, limit=10):
        return (
            db.session.query(User).filter(and_(User.active == true(), User.roles.any(name='assembler'))).all()
        )


class ProductionEntryModelView(RoleBasedModelView):
    details_modal = True
    #column_labels = dict(user='Lead', users='Members')
    # List table columns
    column_list = (
        'id', 'shift', 'date', 'machine_id', 'order', 'Product Photo', 'Colors', 'status',
        'lead', 'members', 'remaining', 'num_good', 'num_bad'
    )

    column_sortable_list = [ 
        'id', 'shift', 'date', 'order',
         'num_good', 'num_bad'
    ]

    column_filters = ('shift.name', 'date', 'lead.name', 'order.assigned_machine_id', 'order.status', 'order.remaining', 'members.name', 'num_good', 'num_bad')
    # Sort entry by id descending order.
    column_default_sort = ('id', True)

    # Create form fields
    def order_status_filter():
        return db.session.query(Order).filter(Order.status != 'COMPLETED')

    form_args = dict(
        order = dict(label='For Order', query_factory=order_status_filter)
    )
    form_create_rules = ('shift', 'order', 'date', 'lead', 'members')
    column_labels = dict(num_hourly_good='Num Hourly Good - Example: 10,20,30',num_hourly_bad='Num Hourly Bad - Example: 0,1,2')
    form_columns = (
        'shift',
        'order',
        'date',
        'lead',
        'members',
        ProductionEntry.num_hourly_good,
        ProductionEntry.num_hourly_bad
    )    
    form_ajax_refs = {
        'lead': UserLeadAjaxModelLoader(
            "lead", db.session, User, fields=['name']
        ),
        'members': UserAssemblerAjaxModelLoader(
            "members", db.session, User, fields=['name']
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
                model.order.status = 'IN_PROGRESS'
                if not model.order.production_start_at:
                    model.order.production_start_at = datetime.now()


class TeamRequestModelView(RoleBasedModelView):
    column_exclude_list = ['updated_at', 'day_off']
    column_default_sort = ('id', True)
    form_columns = ('start_date', 'end_date', 'day_off')
    column_labels = dict(id='Team Request Id')
    form_extra_fields = {
        'day_off': SelectMultipleField('Day Off',
            choices=[ 
                ('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), 
                ('3', 'Thursday'), ('4', 'Friday'), 
                ('5', 'Saturday'), ('6', 'Sunday')
            ],
            default = [ '6' ]
        )
    }

    def is_accessible(self):
        result = super(RoleBasedModelView, self).is_accessible()
        self.can_edit = False
        self.can_view_details = False
        return result

    def on_model_change(self, form, model, is_created=False):
        today = datetime.now().date()
        start = form.start_date.data
        end = form.end_date.data
        
        if start <= today:
            raise validators.ValidationError("'Start Date' must be a future date!")
        if end < start:
            raise validators.ValidationError("'Start Date' must be before 'End Date'")
        if (end - start).days > 90:
            raise validators.ValidationError("You cannot schedule for more than 90 days")
            
        if len(form.day_off.data) > 0:
            model.day_off = ','.join(form.day_off.data)
        else:
            model.day_off = ''


class TeamModelView(RoleBasedModelView):
    details_modal = True
    edit_modal = True
    column_default_sort = ('date', False)
    column_sortable_list = [ 'id', 'date', 'machine' ]
    column_list = ['id', 'date', 'week_day', 'shift', 'machine', 'lead', 'members', 'standbys' ]
    column_searchable_list = ('id', 'date')
    column_labels = dict(id='Team Id',week_day='Day')
    column_filters = ('date', 'shift.name','machine.name', 'lead.name', 'members.name')
    
    form_columns = ('date', 'shift', 'machine', 'lead', 'members', 'standbys')
    
    form_ajax_refs = {
        'lead': UserLeadAjaxModelLoader(
            "lead", db.session, User, fields=['name']
        ),
        'members': UserAssemblerAjaxModelLoader(
            "members", db.session, User, fields=['name']
        ),
        'standbys': UserAssemblerAjaxModelLoader(
            "standbys", db.session, User, fields=['name']
        )
    }

    def _standbys_count(view, context, model, name):
        if len(model.standbys) < 1:
            return ''

        html = '<i class="glyphicon glyphicon-user">x%s</i>' % str(len(model.standbys))
        return Markup(html)


    column_formatters = {
        'standbys': _standbys_count
    }
    