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

sleep 1s

sleep 1s

sleep 1s

sleep 1s

