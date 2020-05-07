#!/bin/sh

# super need this and it's very easy to forget so just instant quit if it 
# isn't present
if [ -z "${SECRET_KEY}" ]; then
    echo "No SECRET_KEY environment variable set, quitting";
    exit;
fi;

# check if prod flag is set in settings.pu
if ! python3 -c 'import ralf_explorer_site.settings as set; quit(-1) if not set.PRODUCTION else quit(0)'; then
    echo "PRODUCTION not set to True in settings.py, quitting";
    exit;
fi;

# run deploy check command to show any issues
python3 manage.py check --deploy

# move static files to directory specified in settings.py
python3 manage.py collectstatic

# remove any existing database
rm db.sqlite3

# generate initial database
python3 manage.py makemigrations
python3 manage.py migrate

# generate sqlite database from json file
python3 manage.py shell -c "import json_dump_to_db as j2d; j2d.add_entries();"