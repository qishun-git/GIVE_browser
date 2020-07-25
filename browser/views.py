from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import DataTrackForm, CoordinateForm
from .runbash import ManageGiveData
import json


def home(request):
    return render(request,'browser/home.html',{'title':'Home'})

# track mapping
with open('static/data.json') as f:
        data = json.load(f)
# create a track list
tracks_dict = {}
for k, v in data.items():
    tracks_dict[k] = v.get('track_name')


def browser(request):
    coorform = CoordinateForm(request.GET)
    if request.method == 'POST':
        # get user seleted tracks by POST
        form = DataTrackForm(request.POST)
        tracks = request.POST.getlist('data_tracks')
        if len(tracks) <= 0:
            give_url = '../panel'
        else:
            # add file to GIVE container
            eidtor = ManageGiveData()
            for track_id in tracks:
                # get metadata for each track
                track = data.get(track_id)
                file_type = track.get('file_type')
                track_name = track.get('track_name')
                group = track.get('group')
                label = track.get('label')
                file_name = track.get('file_name')
                eidtor.add(file_type, track_name, group, label, file_name)
            
            # add track to Give panel by GET method
            track_string = '-'.join(tracks)
            give_url = '../panel?selectedtracks=' + track_string
    else:
        # initialize track selection form
        form = DataTrackForm()    
        give_url = '../panel'
    
    context = {
        'title':'Browser', 
        'give_url':give_url,
        'form': form,
        'coorform': coorform
    }
    return render(request,'browser/browser.html', context) 

def about(request):
    return render(request,'browser/about.html', {'title':'About'})

def contact(request):
    return render(request,'browser/contact.html', {'title':'Contact'})



def panel(request):
    selectedtracks = request.GET.copy().get('selectedtracks')
    if selectedtracks:
        # customized tracks
        track_ids_string = selectedtracks.split('-')
        track_ids = [s for s in track_ids_string]
        tracks = ['\"'+tracks_dict[i]+'\",' for i in track_ids[:-1]]
        tracks.append('\"'+tracks_dict[track_ids[-1]]+'\"')
    else:
        # default tracks
        tracks = []
    context = {
        'title':'GIVE-Panel', 
        'tracks': tracks
    }
    return render(request, 'browser/give_panel.html', context)


def panelarea(request):
    selectedtracks = request.GET.copy().get('selectedtracks')
    if selectedtracks:
        # customized tracks
        track_ids_string = selectedtracks.split('-')
        track_ids = [s for s in track_ids_string]
        tracks = ['\"'+tracks_dict[i]+'\",' for i in track_ids[:-1]]
        tracks.append('\"'+tracks_dict[track_ids[-1]]+'\"')
    else:
        # default tracks
        tracks = []
    context = {
        'title':'GIVE-Panel', 
        'tracks': tracks
    }
    return render(request, 'browser/give_area.html', context)


    

