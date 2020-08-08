from django.db import models

# Create your models here.
class Track(models.Model):
    # file_type = models.TextChoices('geneAnnot','bed','bigwig')
    file_type = models.CharField(max_length=50)
    track_name = models.CharField(max_length=50, primary_key=True)
    # group = models.TextChoices('genes','GWAS','LD','RADAR','phastCons100way')
    group = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    creater = models.GenericIPAddressField(default="0.0.0.0")

    def __str__(self):
        return self.file_name

class Coordinates(models.Model):
    coordinates_id = models.AutoField(primary_key=True)
    chromosome = models.CharField(max_length=50)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    def __str__(self):
        name = self.track.track_name + " : " + self.chromosome + " : " + self.start + "-" + self.end
        return name

