from django.db import models
from django.utils import timezone

# Create your models here.
class Track(models.Model):
    # file_type = models.TextChoices('geneAnnot','bed','bigwig')
    ip_track_name = models.CharField(max_length=60, primary_key=True)
    file_type = models.CharField(max_length=50)
    track_name = models.CharField(max_length=50)
    # group = models.TextChoices('genes','GWAS','LD','RADAR','phastCons100way')
    group = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    creater = models.GenericIPAddressField(default="0.0.0.0")
    public = models.BooleanField(default=True)
    modified_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.track_name

class Coordinates(models.Model):
    coordinates_id = models.AutoField(primary_key=True)
    chromosome = models.CharField(max_length=50)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    def __str__(self):
        name = self.track.ip_track_name + " : " + self.chromosome + " : " + self.start + "-" + self.end
        return name

