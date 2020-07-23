import subprocess

class ManageGiveData():
    group_set = set(['genes', 'GWAS', 'LD', 'linkage', 'phastCons100Way', 'RADAR'])

    
    def add(self, file_type, track_name, group_name, short_label, file_name):
        if file_type == 'geneAnnot':
            subprocess.call(['static/add_geneAnnot.sh', track_name, group_name, short_label, file_name])
        elif file_type == 'bed':
            subprocess.call(['static/add_bed.sh', track_name, group_name, short_label, file_name])
        elif file_type == 'bigwig':
            subprocess.call(['static/add_bigwig.sh', track_name, group_name, short_label, file_name])
        elif file_type == 'interaction':
            subprocess.call(['static/add_interaction.sh', track_name, group_name, short_label, file_name])
        else:
            print("Unsupported file type!")


    def delete(self, group_name, track_name):
        if group_name in self.group_set:
            subprocess.call(['static/delete_file.sh', group_name, track_name])
        else:
            print("No such group!")

