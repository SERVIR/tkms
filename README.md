# SERVIR Training Knowledge Management System (TKMS)

The TKMS is being implemented as a mechanism to facilitate sharing iformation about training and other capacity building events organized by members of the SERVIR Global Network.

This prototype is in the early stages of development. The UI and the underlying database structures may change significantly until the first usable release.

[![Django: 4.x](https://img.shields.io/badge/Django-4.x-blue)](https://www.djangoproject.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SERVIR: Global](https://img.shields.io/badge/SERVIR-Global-green)](https://servirglobal.net)

## Setup and Installation
The installation described here will make use of conda to ensure there are no package conflicts with
existing or future applications on the machine.  It is highly recommended using a dedicated environment
for this application to avoid any issues.

### Recommended
Conda (To manage packages within the applications own environment)

### Environment
- Create the env

```commandline
conda env create -f environment.yml
```

Add a file named data.json in the base directory.  This file will hold a json object containing
the siteID for your application, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, and ACCOUNT_DEFAULT_HTTP_PROTOCOL (likely, http
for dev, https for production).  The format will be:

```json
{
  "ALLOWED_HOSTS": ["localhost", "your_domain.com", "127.0.0.1"],
  "SECRET_KEY": "REPLACE WITH A SECRET KEY USING LETTERS, NUMBERS, AND SPECIAL CHARACTERS",
  "CSRF_TRUSTED_ORIGINS":  ["http://localhost", "http://127.0.0.1"],
  "ACCOUNT_DEFAULT_HTTP_PROTOCOL": "http"
}
```

- enter the environment

```shell
conda activate tkms
```

- Install npm packages
```
npm install --prefix "/servir_apps/tkms/training/static/"
```

- Create database tables and superuser
###### follow prompts to create super user
```commandline
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

TKMS uses Google authentication which will need to be configured in the
[Google Developer APIs Console]( https://console.developers.google.com/apis ). When you open the console you will
need to create a new project.

- Click "Select a project" (or arrow by prior project name if you already have projects) at the top left of the screen.
- In the new dialog click New Project at the top right
- Enter Project Name and click Create
- In the left panel click "OAuth consent screen" link and fill out the form with the information for your application.
- In the left panel click "Credentials" link
- At the top left click + Create Credentials and select "OAuth 2.0 Client ID"
- In the dropdown select "Web Application" and give a name.
- Add Authorized JavaScript origins (you may enable multiple)
    - examples:
        - http://localhost:8010
        - http://127.0.0.1:8010
        - https://tkms.servirglobal.net
- Add Authorized redirect URIs (you may enable multiple)
    - examples:
        - http://localhost:8010/accounts/google/login/callback/
        - http://127.0.0.1:8010/accounts/google/login/callback/
        - https://tkms.servirglobal.net/accounts/google/login/callback/
- Copy and save the Client ID and Client secret to your local machine (you will need these later)
- Click save

Authentication is now enabled through google, but we need to connect it to your application.


Add the site domain to the system in the terminal by entering the shell.  This is needed
due to the social authentication which is enabled.
```shell
python manage.py shell
```
Run the following in the open shell substituting domain for the correct domain
```python
from django.contrib.sites.models import Site
site = Site()
site.domain = '{REPLACE WITH YOUR DOMAIN}'
site.name = '{REPLACE WITH YOUR DOMAIN}'
site.save()
Site.objects.all().values()
exit()
```

Look for your domain in the printed QuerySet and the id of the object. This is your SITE_ID which needs to be 
changed in settings.py if it is not the same.

Open the admin page of your site by navigating to your url/admin and login with the superuser
account you created earlier. In the left panel click the link that says "Social Accounts".  Click the Add
button.  Select Google for the provider, give a name, paste the Client ID that you saved, and the
Client secret (secret key) into the boxes.  Leave Key empty, move the domain you added to Chosen sites and click save.
This completes the Authentication setup.

At this point you should be able to start the application.  From the root directory you can run the following command

```
python manage.py runserver
```

Of course running the application in this manner is only for development.  We recommend installing
this application on a server and serving it through nginx using gunicorn (conda install gunicorn) for production.  To do this you will need to
have both installed on your server.  There are enough resources explaining in depth how to install them,
so we will avoid duplicating this information.  We recommend adding a service to start the application
by creating a .service file located at /etc/systemd/system.  We named ours tkms.service
The service file will contain the following, please substitute the correct paths as mentioned below.

# Server installation
## Create Application Service
As mentioned above create the following file at /etc/systemd/system/ and name it tkms.service
```editorconfig
[Unit]
Description=tkms daemon
After=network.target

[Service]
User=nginx
Group=nginx
SocketUser=nginx
WorkingDirectory={REPLACE WITH PATH TO APPLICATION ROOT}/tkms
accesslog = "/var/log/tkms/tkms_gunicorn.log"
errorlog = "/var/log/tkms/tkms_gunicornerror.log"
ExecStart={REPLACE WITH FULL PATH TO gunicorn IN YOUR CONDA ENV}/bin/gunicorn --timeout 60 --workers 5 --pythonpath '{REPLACE WITH PATH TO APPLICATION ROOT},{REPLACE WITH FULL PATH TO YOUR CONDA ENV}/lib/python3.10/site-packages' --bind unix:{REPLACE WITH LOCATION YOU WANT THE SOCK}/tkms_prod.sock wsgi:application

[Install]
WantedBy=multi-user.target

```

## Create nginx site
Create a file in /etc/nginx/conf.d/ named tkms_prod.conf

```editorconfig
upstream tkms_prod {
server unix:{REPLACE WITH LOCATION YOU WANT THE SOCK}/tkms_prod.sock
           fail_timeout=0;
           }

           server {
           listen 443;
                     server_name {REPLACE WITH YOUR DOMAIN};
                     add_header Access-Control-Allow-Origin *;

                     ssl on;
                     ssl_certificate {REPLACE WITH FULL PATH TO CERT FILE};
                     ssl_certificate_key {REPLACE WITH FULL PATH TO CERT KEY};

                     # Some Settings that worked along the way
                     client_max_body_size 8000M;
                     client_body_buffer_size 8000M;
                     client_body_timeout 120;

                     proxy_read_timeout 300;
                     proxy_connect_timeout 300;
                                              proxy_send_timeout 300;
                                              fastcgi_buffers 8 16k;
                                              fastcgi_buffer_size 32k;
                                              fastcgi_connect_timeout 90s;
                                              fastcgi_send_timeout 90s;
                                              fastcgi_read_timeout 90s;


                                              location = /favicon.ico { access_log off; log_not_found off; }
                                              location /static/ {
autoindex on;
alias {REPLACE WITH FULL PATH TO APPS}/staticfiles/;
}

location / {
proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_pass http://unix:{REPLACE WITH LOCATION YOU WANT THE SOCK}/tkms_prod.sock ;
                      }


                      }

                      # Reroute any non https traffic to https
                      server {
                      listen 80;
                      server_name {REPLACE WITH YOUR DOMAIN};
                      rewrite ^(.*) https://$server_name$1 permanent;
}

```

# Create Alias commands to make starting the application simple
Create a file at /etc/profile.d/ named tkms_alias.sh and add the following:
```commandline
# Global Alias
alias d='conda deactivate'
alias so='sudo chown -R www-data /servir_apps'
alias nsr='sudo service nginx restart'
alias nss='sudo service nginx stop'


# SAMS Alias
alias tkms='cd /servir_apps/tkms'
alias acttkms='conda activate tkms'
alias uotkms='sudo chown -R ${USER} /servir_apps/tkms'
alias sotkms='sudo chown -R www-data /servir_apps/tkms'
alias tkmsstart='sudo service tkms restart; sudo service nginx restart; so'
alias tkmsstop='sudo service tkms stop'
alias tkmsrestart='tkmsstop; tkmsstart'

```
Now activate the alias file by running
```commandline
source /etc/profile.d/tkms_alias.sh
```

Now you should be able to run tkmsstart to run the production application.

---
## Contact information

This effort is being coordinated by the SERVIR Science Coordination Office and the SERVIR Hub's Capacity Building Leads.
For implementation support, contact Francisco Delgado (Geospatial IT Lead) or Billy Ashmall (Senior Software Engineer).
For concept, content and procedures, contact Betzy Hernandez (Capacity Building Lead) or Kathleen Cutting (Project Analyst)

## License and Distribution

SERVIR Training Knowledge Management System (TKMS) is distributed by SERVIR under the terms of the MIT License. See
[LICENSE](https://github.com/SERVIR/SAMS/blob/master/LICENSE) in this directory for more information.

## Privacy & Terms of Use

SERVIR Training Knowledge Management System (TKMS) abides to all of SERVIR's privacy and terms of use as described
at [https://servirglobal.net/Privacy-Terms-of-Use](https://servirglobal.net/Privacy-Terms-of-Use).
