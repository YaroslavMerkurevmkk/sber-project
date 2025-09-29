# Sber project

## Installation
Use Python3.11 or later

### Create venv
```bash
python3.11 -m venv venv
```

### Activate venv and install requirements
```bash
source venv/bin/activate
pip install -U pip && pip install -r requirements.txt
```

### Configuration
Create directory `config` and file `config/config.json`
```json
{
  "token": "Giga Chat token",
  "debug": true,
  "secret_key": "",
  "allowed_hosts": [],
  "db_backend": "sqlite3",
  "db_host": "localhost",
  "db_name": "config/db.sqlite3",
  "db_port": 3306,
  "db_user": "sber_admin",
  "db_password": "parol",
  "data_dir": "data"
}
```

### Configure Django
```bash
python src/manage.py migrate
python src/manage.py createsuperuser
python src/manage.py collectstatic
unicorn web.asgi:application --reload --port 8000
```

### Start on linux
```bash
./bin/run.sh
```

### Start on Windows
Run `bin\run.bat` file *or*
```bash
bin\run_con.bat
```

### Documentation
 - [Commands](docs/commands.md)
 - [Models](docs/models.md)


## Deployment

**Example for Debian 12**

### Clone and install
Clone repository and [install](#installation)

### Setting MySQL server
```sql
CREATE DATABASE <db name>;
CREATE USER '<username>'@'<scope>' IDENTIFIED BY '<user password>';
GRANT ALL PRIVILEGES ON <db name>.* TO '<username>'@'<scope>';
FLUSH PRIVILEGES; 
```

### Setting Systemd Unit
```
[Unit]
Description=AI agent for sber project
After=network.target

[Service]
User=<username>
Group=<username>
WorkingDirectory=<path to project>/src
ExecStart=<path to project>/venv/bin/python3.11 uvicorn web.asgi:application --reload --port 8888

[Install]
WantedBy=multi-user.target
```

Start and enable unit (as root)
```bash
systemctl start sber
systemctl enable sber
```

### Setting Nginx
```
server {
    listen 443 ssl;
    server_name <your domain>;

    ssl_certificate /etc/letsencrypt/live/<your domain>/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/<your domain>/privkey.pem; # managed by Certbot

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'HIGH:!aNULL:!MD5';

    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

    }

    location /admin/ {
        allow <trusted address>;
        deny all;
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias <path to project>/staticfiles/;
        autoindex off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
}
```

Restart service
```bash
systemctl restart nginx
```