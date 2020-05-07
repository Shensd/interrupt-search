#!/bin/sh

# This deploy file is rather specific to the environment I have this deployed
# in, so think of this more as a template if you are looking to deploy your
# own prod instance of this project

# stop apache server
systemctl stop apache2

# generate a new random key file 
dd if=/dev/random bs=512 count=128 | base64 -w 0 > /etc/secret.key
chown root:www-data /etc/secret.key

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
printf "Converting json dump to db..."
python3 manage.py shell -c "import json_dump_to_db as j2d; j2d.add_entries();"
printf "done\n"

# start apache server up again
systemctl start apache2

# print status
systemctl status apache2