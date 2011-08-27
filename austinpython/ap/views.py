from django.views.generic import TemplateView
from austinpython.opportunities.models import Opportunity

class HomeView(TemplateView):
    """ View with overal site summary and registration. """
    template_name = "home.html"

    def get_context_data(self):
        """ Retrieve all the random pieces of data needed for the home page """
        context = dict(
            opportunities = Opportunity.objects.all()[:20],
        )
        return context

