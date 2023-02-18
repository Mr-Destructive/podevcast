from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from podcasts.models import Episode, Pod, Podcast
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


class PodcastDetail(DetailView):
    model = Podcast
    template_name = 'podcast/detail.html'

    def get_context_data(self, **kwargs):
        obj = super().get_context_data(**kwargs)
        obj['episodes'] = Episode.objects.filter(podcast_name_id=obj['podcast'].id).order_by('date')
        return obj
