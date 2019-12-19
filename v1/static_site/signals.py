from v1.static_site.constants import TEMPLATE_NAME_OR_CONTENT_REQUIRED_ERROR


def snake_case_field_name(sender, instance, *args, **kwargs):
    instance.name = instance.name.lower().replace(' ', '_')


def either_template_name_or_template_content_is_required(sender, instance, *args, **kwargs):
    if not (instance.template_file or instance.template_content):
        raise RuntimeError(TEMPLATE_NAME_OR_CONTENT_REQUIRED_ERROR)
