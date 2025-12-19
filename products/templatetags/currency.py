from django import template

register = template.Library()


@register.filter
def currency(value, precision=2):
    """Format a numeric value to fixed decimals. Simple fallback for missing currency tag lib."""
    try:
        return f"{float(value):,.{int(precision)}f}"
    except Exception:
        return value
