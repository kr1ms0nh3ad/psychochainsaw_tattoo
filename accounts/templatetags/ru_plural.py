from django import template
register = template.Library()

@register.filter
def ru_plural(value, arg):
    # arg = "год,года,лет"
    args = arg.split(',')
    number = abs(int(value))
    if number % 10 == 1 and number % 100 != 11:
        return args[0]
    elif number % 10 >= 2 and number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return args[1]
    else:
        return args[2]
