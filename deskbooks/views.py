from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from .models import BorderPoint


class BordersListView(ListView):
    """Display list of border points"""
    model = BorderPoint
    template_name = 'deskbooks/bpoints.html'
    paginate_by = 20

    def get_queryset(self):
        return BorderPoint.objects.all().order_by('region')
