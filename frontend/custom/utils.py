def get_boolean_form_field_value(value):
    boolean_form_field_dict = {
        'on': True,
        'off': False
    }

    return boolean_form_field_dict.get(value, False)
