import os
import os.path as op

from flask_admin.contrib.sqla import ModelView
from model import Color, Machine, Product
from flask_admin.form import rules
from flask_admin.model.form import InlineFormAdmin
from flask_admin import form
from jinja2 import Markup
from sqlalchemy.event import listens_for

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
    form_columns = (Machine.name, Machine.status, Machine.power_in_kilowatt)

class ProductModelView(ModelView):
    column_display_pk = True
    # column_hide_backrefs = False
    def _list_thumbnail(view, context, model, name):
        if not model.photo_url:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.photo_url)))

    column_formatters = {
        'path': _list_thumbnail
    }

    form_columns = (
        'name',
        'color_id',
        'color',
        'weight',
        'time_to_build',
        'selling_price',
        'num_employee_required',
        'default_machine_id',
        'mold_id',
        'photo_url'
    )

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'photo_url': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }
    # Create form fields adjustment.
   


