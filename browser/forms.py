from django import forms
from .models import Track, Coordinates

class DataTrackForm(forms.Form):
    track_list = forms.ModelMultipleChoiceField(queryset=Track.objects.all(), widget=forms.CheckboxSelectMultiple)