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

def getIP(request):
    from ipware import get_client_ip
    ip, _ = get_client_ip(request)
    if ip is None:
        # Unable to get the client's IP address
        return "0.0.0.0"
    else:
        return ip

def browser(request):
    ip = getIP(request)
    data = Track.objects.all()
    if request.method == 'POST':
        # get user seleted tracks by POST
        form = DataTrackForm(request.POST, creater=ip)
        tracks = request.POST.getlist('track_list')
        if not tracks or len(tracks) <= 0:
            give_url = '../panel'
        else:
            # add file to GIVE container
            editor = ManageGiveData()
            for track_id in tracks:
                # get metadata for each track
                track = data.get(pk=track_id)
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
        form = DataTrackForm(creater=ip)    
        give_url = '../panel'
    
    context = {
        'title':'Browser', 
        'give_url':give_url,
        'form': form,
    }
    return render(request,'browser/browser.html', context) 


def panel(request):
    data = Track.objects.all()
    selectedtracks = request.GET.get('selectedtracks')
    num_of_subs = request.GET.get('num_of_subs', 2)
    coordinates = ["\"chr10:30000059-30010059\",", "\"chr10:30000059-30010059\""]
    tracks = []
    if selectedtracks:
        # customized tracks
        track_ids_string = selectedtracks.split('-')
        track_ids = [s for s in track_ids_string]
        
        for i in range(len(track_ids)):
            t_id = track_ids[i]
            t = data.get(pk=t_id)
            track = '\"'+t.track_name+'\",' if i < len(track_ids)-1 else '\"'+t.track_name+'\"'
            tracks.append(track)
            cors_list = Coordinates.objects.filter(track=t)

            if cors_list and len(cors_list) > 0:
                cors = cors_list[0]
                ch = cors.chromosome
                start = cors.start
                end = cors.end
                cor_string = '\"' + ch + ':' + start + '-' + end + '\"'
                print("here:"+t.group)
                if t.group == "GWAS":
                    coordinates[0] = cor_string + ','
                else:
                    coordinates[1] = cor_string


    context = {
        'title': 'GIVE-Panel', 
        'subs': num_of_subs,
        'coors': coordinates,
        'tracks': tracks
    }
    return render(request, 'browser/give_panel.html', context)


@csrf_exempt
def addViz(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        
        track_list = json_data.get('track_list')
        for track in track_list:
            file_type = track.get('file_type', '')
            ip_track_name = track.get('track_name', '0_0_0_0.name')
            creater, track_name = ip_track_name.split('.')
            creater = '.'.join(creater.split('_'))
            group = track.get('group', '')
            label = track.get('label', '')
            file_name = track.get('file_name', '')
            new_track = Track(ip_track_name=ip_track_name,file_type=file_type,track_name=track_name,group=group,label=label,file_name=file_name,creater=creater)
            new_track.save()
            cor_dict = track.get('coordinates', {})
            for k,v in cor_dict.items():
                chromosome = k
                for pair in v:
                    start = pair[0]
                    end = pair[1]
                    new_cor = Coordinates(chromosome=chromosome,start=start,end=end,track=new_track)
                    new_cor.save()
    return HttpResponse(status=204)