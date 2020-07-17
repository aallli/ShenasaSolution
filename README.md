# ShenasaSolution

1- apt-get update && apt-get -y upgrade
2- apt-get install python3 && apt-get install python3-pip && apt-get install libpq-dev
3- pip install virtualenv
4- Create virtual environment: virtualenv venv
5- Clone source: git clone https://github.com/aallli/ShenasaSolution.git
6- Activate virtualenv: source venv/bin/activate
7- pip install -r requirements.txt
8- Install postgresql:

    apt-get install postgresql postgresql-contrib
    usermod -aG sudo postgres

9- Switch over to the postgres account on your server by typing:
    
    sudo -i -u postgres

10- Create database named sadesa: sudo -u postgres createdb

    sudo -u postgres createdb shenasa

11- Set postgres password: 
    
    sudo -u postgres psql postgres
    \password postgres
    \q
    exit 

12- Caution: Allow remote access to postgres:
    
    Add to /etc/postgresql/9.5/main/postgresql.conf : #listen_addresses = '*'
    Add to /etc/postgresql/9.5/main/pg_hba.conf : host all all 0.0.0.0/0 trust
    systemctl restart postgresql

13- python manage.py migrate
14- test if gunicorn can serve application: gunicorn --bind 0.0.0.0:8000 ShenasaSolution.wsgi
15- groupadd --system www-data
16- useradd --system --gid www-data --shell /bin/bash --home-dir /home/admin1/shenasa/ShenasaSolution shenasa
17- usermod -aG sudo shenasa
18- chown -R shenasa:www-data /home/admin1/shenasa/ShenasaSolution
19- chmod -R g+w /home/admin1/shenasa/ShenasaSolution

Configure Gunicorn:
20- nano /etc/systemd/system/gunicorn-shenasa.service
21- add:
    
    [Unit]
    Description=gunicorn daemon
    After=network.target
    
    [Service]
    User=shenasa
    Group=www-data
    WorkingDirectory=/home/admin1/shenasa/ShenasaSolution
    EnvironmentFile=/etc/gunicorn-shenasa.env
    ExecStart=/home/admin1/shenasa/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/admin1/shenasa/ShenasaSolution/ShenasaSolution.sock ShenasaSolution.wsgi:application
    
    [Install]
    WantedBy=multi-user.target
        
22- nano /etc/gunicorn-shenasa.env
23- Add followings:
    
    DEBUG=0
    DEPLOY=1
    DATABASES_PASSWORD='[database password]'
    ALLOWED_HOSTS='[server ip]'
    ADMIN_TEL='[admin tel]'
    ADMIN_EMAIL='[admin email]'
    LIST_PER_PAGE=[list per page in admin pages]
    CHAT_SERVER_URL = ='[Chat server url]'
    CHAT_SERVER_TOKEN = '[System token]'
    CHAT_SUPPORT_GROUP = '[Chat support group name]'
    CHAT_SUPPORT_REFRESH_INTERVAL = [Chat support refresh interval]
    
24- systemctl start gunicorn-shenasa
25- systemctl enable gunicorn-shenasa
26- Check if 'ShenasaSolution.sock' file exists: ls /home/admin1/shenasa/ShenasaSolution
27- Create /etc/nginx/conf.d/proxy_params
28- Add followings:

    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

29- If gunicorn.service file is changed, run:

    systemctl daemon-reload
    systemctl restart gunicorn-shenasa

30- Install gettext:

    apt-get update
    apt-get upgrade
    apt-get install
    apt-get install gettext

31- Compile messages for i18N:
    
    source env/bin/activate
    django-admin compilemessages (if translation is needed)

32- Collect static files: (Create static and uploads directory if needed)
 
    python manage.py collectstatic

Configure Nginx:
33- create keys and keep them in /root/certs/shenasa/:
    
    openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out /root/certs/shenasa/shenasa.crt -keyout /root/certs/shenasa/shenasa.key

34- Restrict the key’s permissions so that only root can access it:
    
    chmod 400 /root/certs/shenasa/shenasa.key

35- Install nginx:

    apt update
    apt install nginx

36- Run nginx:

    systemctl daemon-reload
    systemctl start nginx
    systemctl enable nginx
    
37- Configure nginx:

    nano /etc/nginx/conf.d/shenasa.conf

38- Add:
    
    server {
        listen       80;
        server_name  shenasa.irib.ir;
    
        error_page 404 /404.html;
        location /404.html {
            root /home/admin1/shenasa/ShenasaSolution/static/errors;
            internal;
        }
    
        location /static/ {
            if ($request_method = 'GET') {
                add_header 'Access-Control-Allow-Origin' 'http://shenasa.irib.ir:8000';
                add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
                add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
                add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';
            }
    
            root /home/admin1/shenasa/ShenasaSolution;
        }
    
        location   / {
            return 301 http://shenasa.irib.ir:8000;
        }
    }
    
    server {
        listen 8000;
        server_name  shenasa.irib.ir;
    
        location = /favicon.ico { access_log off; log_not_found off; }
    
        error_page 502 /502.html;
        location /502.html {
            root /home/admin1/shenasa/ShenasaSolution/static/errors;
            internal;
        }
    
        error_page 503 504 507 508 /50x.html;
        location /50x.html {
            root /home/admin1/shenasa/ShenasaSolution/static/errors;
            internal;
        }
    
        location /static/ {
            root /home/admin1/shenasa/ShenasaSolution;
        }
    
        location /media/ {
            root /home/admin1/shenasa/ShenasaSolution;
        }
    
        location / {
            include proxy_params;
            proxy_pass http://unix:/home/admin1/shenasa/ShenasaSolution/ShenasaSolution.sock;
        }
    }

39- Test your Nginx configuration for syntax errors by typing: 

    /usr/sbin/nginx -t

40- Restart nginx:

    /usr/sbin/nginx -s stop
    /usr/sbin/nginx