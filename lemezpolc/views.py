from django.shortcuts import render
from django.db.models.functions import Lower

from lemezpolc.models import Release


def index(request):
    releases = Release.objects.order_by(Lower('artist'))
    return render(request, 'lemezpolc/index.html', {'releases': releases})

    return render(request, 'lemezpolc/index.html', {'releases': releases})
