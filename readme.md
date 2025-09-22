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
  "secret_key": "",
  "allowed_hosts": [],
  "db_backend": "sqlite3",
  "db_host": "localhost",
  "db_name": "config/db.sqlite3",
  "db_port": 3306,
  "db_user": "sber_admin",
  "db_password": "parol"
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

### Documentation
 - [Commands](docs/commands.md)
 - [Models](docs/models.md)