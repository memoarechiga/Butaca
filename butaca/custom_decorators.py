from django.http import HttpResponseForbidden

def promoter_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.status == 'Promotor':  # Replace 'Promoter' with the status value for promoters in your CustomUser model
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this page.")

    return _wrapped_view