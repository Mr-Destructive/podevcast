from django.shortcuts import render
from django.views.generic import CreateView
from podcasts.models import Pod
from podcasts.forms import PodForm


class PodCreate(CreateView):
    model = Pod
    form_class = PodForm
    template_name = 'pod/create.html'

    def form_valid(self, form):
        return super().form_valid(form)
