from django import template
register = template.Library()
@register.filter
def tr(i,n=3):
    r,m=divmod((i-1),n)
    if not m:
        return True
    else:
        return False
