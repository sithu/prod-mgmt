from flask_admin.contrib.sqla import ModelView
from model import Color, Machine, Product
from flask_admin.form import rules
from flask_admin.model.form import InlineFormAdmin

class MyModelView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

class ColorInlineModelForm(InlineFormAdmin):
    form_columns = ('name', 'color_code')


class ColorModelView(ModelView):
    #inline_models = (ColorInlineModelForm(Color),)
    column_display_pk = True
    #column_hide_backrefs = False
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
    # column_filters = ('id','name','status','updated_at')
    column_list = [Machine.id, Machine.name, Machine.status, Machine.updated_at]
    column_searchable_list = (Machine.id, Machine.name, Machine.status)
    #column_select_related_list = (Machine.id, Machine.name, Machine.status)
    #form_edit_rules = form_create_rules
    #form_excluded_columns = (Color.name)
    form_columns = (Machine.name, Machine.status)

class ProductModelView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


