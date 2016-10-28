from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render


def home(request):
    cts = ContentType.objects.all()
    return render(request, "home.html", {'cts': cts})
