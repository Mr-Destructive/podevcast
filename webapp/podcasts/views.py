from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from podcasts.models import Pod, Podcast
from podcasts.forms import PodForm


class PodCreate(CreateView):
    model = Pod
    form_class = PodForm
    template_name = 'pod/create.html'

    def form_valid(self, form):
        return super().form_valid(form)


class PodScrap(UpdateView):
    model = Pod
    form_class = PodForm
    template_name = 'pod/create.html'


class PodList(ListView):
    model = Pod
    template_name = 'pod/list.html'


class PodcastList(ListView):
    model = Podcast
    template_name = 'podcast/list.html'
