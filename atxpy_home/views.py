from django.http import Http404
from django.views.generic import DetailView

from hero_content.models import Hero


class IndexView(DetailView):
    model = Hero
    queryset = Hero.objects.all().select_related()
    template_name = "index.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            return queryset.all()[0]
        except IndexError:
            raise Http404("Unable to load hero content")
