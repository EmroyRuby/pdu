from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse


def get_title(request):
    title_data = {
        'title': 'django is connected',
    }
    return JsonResponse(title_data)
