from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import DataTrackForm
from .runbash import ManageGiveData
import json
from .models import Track, Coordinates
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request,'browser/home.html',{'title':'Home'})

# # track mapping
# with open('static/data.json') as f:
#         data = json.load(f)
# # create a track list
# tracks_dict = {}
# for k, v in data.items():
#     tracks_dict[k] = v.get('track_name')


def browser(request):
    data = Track.objects.all()
    if request.method == 'POST':
        # get user seleted tracks by POST
        form = DataTrackForm(request.POST)
        tracks = request.POST.getlist('track_list')
        if not tracks or len(tracks) <= 0:
            give_url = '../panel'
        else:
            # add file to GIVE container
            editor = ManageGiveData()
            for track_id in tracks:
                # get metadata for each track
                track = data.get(track_id=track_id)
                file_type = track.file_type
                track_name = track.track_name
                group = track.group
                label = track.label
                file_name = track.file_name
                editor.add(file_type, track_name, group, label, file_name)
            
            # add track to Give panel by GET method
            track_string = '-'.join(tracks)
            give_url = '../panel?selectedtracks=' + track_string
            # print(give_url)
    else:
        # initialize track selection form
        form = DataTrackForm()    
        give_url = '../panel'
    
    context = {
        'title':'Browser', 
        'give_url':give_url,
        'form': form,
    }
    return render(request,'browser/browser.html', context) 


def panel(request):
    data = Track.objects.all()
    selectedtracks = request.GET.copy().get('selectedtracks')
    if selectedtracks:
        # customized tracks
        track_ids_string = selectedtracks.split('-')
        track_ids = [s for s in track_ids_string]
        tracks = ['\"'+data.get(track_id=i).track_name+'\",' for i in track_ids[:-1]]
        tracks.append('\"'+data.get(track_id=track_ids[-1]).track_name+'\"')
    else:
        # default tracks
        tracks = []
    context = {
        'title':'GIVE-Panel', 
        'tracks': tracks
    }
    return render(request, 'browser/give_panel.html', context)


@csrf_exempt
def addViz(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        
        track_list = json_data.get('track_list')
        for track in track_list:
            file_type = track.get('file_type')
            track_name = track.get('track_name')
            group = track.get('group')
            label = track.get('label')
            file_name = track.get('file_name')
            new_track = Track(file_type=file_type,track_name=track_name,group=group,label=label,file_name=file_name)
            new_track.save()
            cor_dict = track.get('coordinates')
            for k,v in cor_dict.items():
                chromosome = k
                for pair in v:
                    start = pair[0]
                    end = pair[1]
                    new_cor = Coordinates(chromosome=chromosome,start=start,end=end,track=new_track)
                    new_cor.save()
    return HttpResponse(status=204)







    

