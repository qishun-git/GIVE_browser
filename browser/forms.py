from django import forms
from .models import Track, Coordinates
from django.db.models import Q

class DataTrackForm(forms.Form):
    def __init__(self,*args,**kwargs):
        try:
            ip = kwargs.pop('creater')
        except:
            ip = "0.0.0.0"
        super(DataTrackForm,self).__init__(*args,**kwargs)
        self.fields['track_list'].queryset = Track.objects.filter(Q(creater=ip) | Q(public=True))

    track_list = forms.ModelMultipleChoiceField(queryset=Track.objects.all(), widget=forms.CheckboxSelectMultiple)