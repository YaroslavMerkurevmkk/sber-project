# Sber project

**All commands in description tested on linux (Fedora)**

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

### Setting MySQL server
```sql
CREATE DATABASE <db name>;
CREATE USER '<username>'@'<scope>' IDENTIFIED BY '<user password>';
GRANT ALL PRIVILEGES ON <db name>.* TO '<username>'@'<scope>';
FLUSH PRIVILEGES; 
```

### Configuration
Create directory `config` and file `config/config.json`
```json
{
  "token": "Giga Chat token",
  "debug": true,
  "secret_key": "",
  "allowed_hosts": [],
  "csrf_trusted_origins": [],
  "db_backend": "sqlite3",
  "db_host": "localhost",
  "db_name": "config/db.sqlite3",
  "db_port": 3306,
  "db_user": "sber_admin",
  "db_password": "parol",
  "data_dir": "data"
}
```

`data_dir` - Directory with .md files for tools

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
