from wsgiref.validate import validator


def is_email_valid(address):
    # Check if the e-mail address already exists in database.
    return True  # or False

def user_email(form, field):
    if not is_email_valid(field.data):
        raise validator.ValidationError("The e-mail address {} is already taken.".format(field.data))