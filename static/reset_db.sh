#!/bin/bash
docker exec -it give /bin/bash -c "bash remove_data.sh -u root -p Admin2015 -r hg38 -a CONFIRM"
sleep 1s
docker exec -it give /bin/bash -c "bash add_trackGroup.sh  -u root -p Admin2015 -r hg38 -g \"genes\" -l \"Known Gene\" -o 1 -s 0"
sleep 1s
docker exec -it give /bin/bash -c "bash add_trackGroup.sh  -u root -p Admin2015 -r hg38 -g \"GWAS\" -l \"GWAS data\" -o 2 -s 0"
sleep 1s
docker exec -it give /bin/bash -c "bash add_trackGroup.sh  -u root -p Admin2015 -r hg38 -g \"LD\" -l \"LD data\" -o 2 -s 0"
sleep 1s
docker exec -it give /bin/bash -c "bash add_trackGroup.sh  -u root -p Admin2015 -r hg38 -g \"RADAR\" -l \"RADAR data\" -o 4 -s 0"
sleep 1s
docker exec -it give /bin/bash -c "bash add_trackGroup.sh  -u root -p Admin2015 -r hg38 -g \"phastCons100way\" -l \"phastCons data\" -o 4 -s 0"
sleep 1s
docker exec -it give /bin/bash -c "bash add_geneAnnot.sh  -u root -p Admin2015 -r hg38 -t \"KnownGene\" -g \"genes\" -l \"UCSC known genes annotation\" -s \"UCSC Genes\" -o 1 -v full  -f /mnt/my_data/genePred_symbol.txt"
sleep 1s
docker exec -it give /bin/bash -c "bash add_track_bigWig.sh -u root -p Admin2015 -r hg38 -t \"RADAR\" -g \"RADAR\" -l \"RADAR\" -s \"RADAR\" -o 3 -v full -a true -f /mnt/my_data/radar.bw"
sleep 1s
docker exec -it give /bin/bash -c "bash add_track_bigWig.sh -u root -p Admin2015 -r hg38 -t \"phastCons\" -g \"phastCons100way\" -l \"phastCons\" -s \"phastCons\" -o 3 -v full -a true -f /mnt/my_data/hg38.phastCons100way.bw"

