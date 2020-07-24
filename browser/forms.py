from django import forms
import json


class DataTrackForm(forms.Form):
    #read track list from static/tracks.json file
    with open('static/data.json') as f:
        tracks_dict = json.load(f)

    # Grab only the ids and file_names
    DATA_TRACKS = []
    for k, v in tracks_dict.items():
        DATA_TRACKS.append((k, v.get('file_name')))
    data_tracks = forms.MultipleChoiceField(choices=DATA_TRACKS, widget=forms.CheckboxSelectMultiple)
