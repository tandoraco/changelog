def snake_case_field_name(sender, instance, *args, **kwargs):
    instance.name = instance.name.lower().replace(' ', '_')
