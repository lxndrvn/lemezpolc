import django_filters

from lemezpolc.models import Release


class ReleaseFilter(django_filters.FilterSet):
    artist = django_filters.CharFilter(lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Release
        fields = ['year', 'release_format']
