from django import template
from django.urls import reverse
import re


register = template.Library()

@register.filter
def permission_noarg(url,request):
    for permission_url in request.session['permission_list']:
        # print(url)
        # print(permission_url['url'])
        if reverse(url)==permission_url['url']:
            return True
    return False


@register.filter
def permission_arg(url,request):
    for permission_url in request.session['permission_list']:
        # print('++++',reverse(url,args=(1,)))
        # print('>>>>>',permission_url['url'])
        if re.search(f"^{permission_url['url']}$",reverse(url,args=(1,))):

            return True
    return False