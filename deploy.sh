#! /bin/sh

BASE_PATH="$(cd "$(dirname "$0")" && pwd -P)"
BACKUP_DB_PATH="$1"
VENV_PATH="$2"
NOW=$(date +%s)

# backup database
cp "$BASE_PATH/db.sqlite3" "$BACKUP_DB_PATH/db-$NOW.sqlite3"

# activate virtual environment
source $VENV_PATH/bin/activate

# get last version from git
git -C $BASE_PATH pull

# install javascript dependencies
npm install --prefix "$BASE_PATH/training/static/"

# python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --clear --no-input

# change folder permission
chown apache: -R $BASE_PATH

# restart service
systemctl restart httpd
