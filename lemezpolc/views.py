from django.shortcuts import render

from lemezpolc.models import Release


def index(request):
    releases = Release.objects.order_by('artist')[:30]
    return render(request, 'lemezpolc/index.html', {'releases': releases})
