#!/bin/sh

if [ -z "${SECRET_KEY}" ]; then
    echo "No SECRET_KEY environment variable set, quitting";
    exit;
fi;

# run deploy check command to show any issues
python3 manage.py check --deploy

# move static files to directory specified in settings.py
python3 manage.py collectstatic

# generate sqlite database from json file
python3 manage.py shell -c "import json_dump_to_db as j2d; j2d.add_entries();"