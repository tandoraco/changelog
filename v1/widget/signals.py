from frontend.constants import WIDGET_CSS_EDIT_WARNING


def remove_css_code_edit_warning(sender, instance, *args, **kwargs):
    if instance.css:
        instance.css = instance.css.replace(WIDGET_CSS_EDIT_WARNING, '')
