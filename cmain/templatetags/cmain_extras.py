
from django import template

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    arg_list = [arg.strip() for arg in group_name.split(',')]
    return user.groups.filter(name__in=arg_list).exists()