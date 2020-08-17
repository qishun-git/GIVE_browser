from django.http                        import HttpResponse, HttpResponseRedirect
from django.shortcuts                   import get_object_or_404, render
from django.urls                        import reverse
from django.views.decorators.csrf       import csrf_exempt
from django.conf                        import settings
from .forms                             import DataTrackForm
from .runbash                           import ManageGiveData
from .models                            import Track, Coordinates

import json
import re
import os
import glob



def home(request):
    return render(request,'browser/home.html',{'title':'Home'})


def browser(request):
    def getIP(request):
        from ipware import get_client_ip
        ip, _ = get_client_ip(request)
        if ip is None:
            # Unable to get the client's IP address
            return "0.0.0.0"
        else:
            return ip
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
            track_string = '|'.join(tracks)
            give_url = '../panel?selectedtracks=' + track_string

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
    num_of_subs = request.GET.get('num_of_subs', 1)
    coordinates = "\"chr10:30000000-50000000\""
    tracks = []
    if selectedtracks:
        # customized tracks
        track_ids_string = selectedtracks.split('|')
        track_ids = [s for s in track_ids_string]
        
        for i in range(len(track_ids)):
            t_id = track_ids[i]
            t = data.get(pk=t_id)
            track = '\"'+t.track_name+'\",' if i < len(track_ids)-1 else '\"'+t.track_name+'\"'
            tracks.append(track)
            # get GWAS coordinates
            if t.group == "GWAS":
                cors_list = Coordinates.objects.filter(track=t)
                if cors_list and len(cors_list) > 0:
                    cors = cors_list[0]
                    ch = cors.chromosome
                    start = cors.start
                    end = cors.end
                    cor_string = '\"' + ch + ':' + start + '-' + end + '\"'
                    coordinates = cor_string


    context = {
        'title': 'Visualization-Panel', 
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
            ip_track_name = track.get('track_name', '')
            try: 
                creater, track_name = ip_track_name.split('-')
                creater = creater.replace('_', '.')
                public = False
            except:
                public = True
                creater = "0.0.0.0"
                track_name = ip_track_name
            group = track.get('group', '')
            label = track.get('label', '')
            file_name = track.get('file_name', '')
            new_track = Track(
                ip_track_name=ip_track_name,
                file_type=file_type,
                track_name=track_name,
                group=group,
                label=label,
                file_name=file_name,
                creater=creater,
                public=public
                )
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


def delete_files():
    files = glob.glob(settings.FILES_DIR+'/*')
    for f in files:
        if f.endswith('cytoBandIdeo.txt'):
            continue
        os.remove(f)


def delete(request):
    tracks = Track.objects.filter(public=False)
    if tracks:
        editor = ManageGiveData()
        for track in tracks:
            editor.delete(track.group, track.track_name)
            f = settings.FILES_DIR+'/' + track.file_name
            os.remove(f)
        Track.objects.filter(public=False).delete()
        

    return HttpResponse("<h1>DELETED!<h1>")


def reset(request):
    editor = ManageGiveData()
    editor.reset()

    Track.objects.filter(public=False).delete()

    files = glob.glob(settings.FILES_DIR+'/*')
    file_set = set(["cytoBandIdeo.txt", "genePred_symbol.txt", "radar.bw", "hg38.phastCons100way.bw"])
    for f in files:
        flag = False
        for do_not_delete in file_set:
            if f.endswith(do_not_delete):
                flag = True
                break
        if flag:
            continue
        os.remove(f)

    return HttpResponse("<h1>RESETED!<h1>")
