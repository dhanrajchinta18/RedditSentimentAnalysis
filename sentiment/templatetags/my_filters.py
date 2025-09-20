from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """Checks if a string ends with the given argument."""
    try:
        return str(value).lower().endswith(str(arg).lower())
    except Exception:
        return False
