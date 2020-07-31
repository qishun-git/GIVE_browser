from django import forms
from .models import Track

class DataTrackForm(forms.Form):
    track_list = forms.ModelMultipleChoiceField(queryset=Track.objects.all(), widget=forms.CheckboxSelectMultiple)