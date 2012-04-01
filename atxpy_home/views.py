from datetime import datetime
from django.views.generic import DetailView

from hero_content.models import Hero
from posts.models import Post

class IndexView(DetailView):
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
        context["posts"] = Post.objects.order_by("-pub_date")[:5]
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
