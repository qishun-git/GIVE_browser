#!/bin/bash
docker exec -it give /bin/bash -c "bash remove_data.sh -u root -p Admin2015 -r hg38 -g $1 -t \"$2\""