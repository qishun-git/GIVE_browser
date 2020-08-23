from background_task import background
from django.conf     import settings
from .runbash        import ManageGiveData
from .models         import Track
import os
import datetime
from django.utils import timezone


DELETE_INTERVAL_DAYS = 1

@background(schedule=1)
def delete_task():
    print('Start deleting -------------------------------------------')
    tracks = Track.objects.filter(public=False)
    if tracks:
        print("There are " + str(len(tracks)) + " tracks")
        editor = ManageGiveData()
        for track in tracks:
            t = track.modified_time
            if t < timezone.now()-datetime.timedelta(days=DELETE_INTERVAL_DAYS):
                print("deleting:" + track.ip_track_name)
                editor.delete(track.group, track.track_name)
                try:
                    f = settings.FILES_DIR+'/' + track.file_name
                    os.remove(f)
                except:
                    print('No such file:' + track.file_name)
                track.delete()
                print('deleted!')
    else:
        print("Currently no track to delete.")