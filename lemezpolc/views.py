from django.shortcuts import render
from django.db.models.functions import Lower

from lemezpolc.filters import ReleaseFilter
from lemezpolc.models import Release


def release_list(request):
    release_filter = ReleaseFilter(request.GET, queryset=Release.objects.order_by(Lower('artist')))
    return render(request, 'lemezpolc/index.html', {'filter': release_filter})
