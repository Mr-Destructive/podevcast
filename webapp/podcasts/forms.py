from django import forms
from podcasts.models import Pod

class PodForm(forms.ModelForm):
    class Meta:
        model = Pod
        fields = ['rss_link']
