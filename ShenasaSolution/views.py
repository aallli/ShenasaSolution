from django.contrib import messages
from django.shortcuts import redirect
from ShenasaSolution.utlis import update_operator


def start_support(request):
    try:
        update_operator(request, status='ready')
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)
    return redirect(request.META['HTTP_REFERER'])


def stop_support(request):
    try:
        update_operator(request, status='off')
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)
    return redirect(request.META['HTTP_REFERER'])
