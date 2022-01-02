from .models import Activity


def common(request):
    context = {}

    if not request.user.is_anonymous:
        context = {
            'activities': Activity.objects.filter(user=request.user).exclude(watched_flag=True)
        }

    return context