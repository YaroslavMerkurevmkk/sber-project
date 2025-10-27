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
  "db_backend": "mysql",
  "db_host": "localhost",
  "db_name": "sber-db",
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

### Start on Windows
Run `bin\run.bat` file *or*
```bash
bin\run_con.bat
```

### Usage Example
```python
import pprint
import time

import requests


def main(question: str, api_url: str, token: str) -> None:
    data = {
        "token": token,
        "reg_number": int(time.time()),
        "open_access": True,
        "fz_53": False,
        "organisation": "ООО Тест",
        "filling_date": int(time.time()),
        "fast_track": False,
        "first_name": "Иван",
        "middle_name": "Иванович",
        "last_name": "Иванов",
        "birth_date": int(time.mktime(time.strptime("1990-01-01", "%Y-%m-%d"))),
        "address": "г. Москва, ул. Пушкина, д. 1",
        "email": "ivan.ivanov@example.com",
        "phone_number": "+74951234567",
        "question": question,
        "region": "Москва"
    }

    resp = requests.post(api_url, json=data)
    print(resp.status_code)

    if resp.ok:
        pprint.pp(resp.json())
    else:
        print(resp.text)


if __name__ == "__main__":
    main("Some question", "http://127.0.0.1:8000/api/", "your token")
```