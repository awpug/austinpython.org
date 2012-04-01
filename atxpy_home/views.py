from cbv_utils.mixins import context_mixin_factory
from datetime import datetime
from django.views.generic import DetailView

from hero_content.models import Hero
from posts.models import Post
from django.conf import settings


def posts():
    return Post.objects.all()[:5]

PostsMixin = context_mixin_factory(callback=posts)


class IndexView(PostsMixin, DetailView):
    model = Hero
    queryset = Hero.objects.all()
    template_name = "index.html"

    def get_queryset(self, queryset=None):
        if queryset is None:
            queryset = self.queryset
        return queryset.filter(pub_date__lte=datetime.now)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            return queryset.all()[0]
        except IndexError:
            return _fake_hero()

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        # This should be moved to a default template var at some point...
        context["USE_COMPILED_STATIC"] = settings.USE_COMPILED_STATIC
        return context


def _fake_hero():
    """ Generate a stub hero for first-time peeps. """
    return Hero(title="No Hero Content!",
        summary="Add a hero to the database to set it up.",
        pub_date=datetime.today(),
        action_text="Action Link Here",
        action_url="#action-link",
        location="Location Here",
        datetime=datetime.now())
