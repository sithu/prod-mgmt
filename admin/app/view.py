from flask_admin.contrib.sqla import ModelView

class MyModelView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
