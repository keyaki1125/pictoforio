# from django import template
# from ..models import Activity
#
# register = template.Library()
#
#
# def context_activities(request):
#     context = {
#         'activities': Activity.objects.filter(user=request.user).exclude(watched_flag=True)
#     }
#     return context