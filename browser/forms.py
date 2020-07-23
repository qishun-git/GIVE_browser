from django import forms
import json


class DataTrackForm(forms.Form):
    #read track list from static/tracks.json file
    with open('static/data.json') as f:
        tracks_dict = json.load(f)

    DEMO_CHOICES = []
    for k, v in tracks_dict.items():
        DEMO_CHOICES.append((k, v.get('file_name')))
    data_track_field = forms.MultipleChoiceField(choices=DEMO_CHOICES, widget=forms.CheckboxSelectMultiple)
