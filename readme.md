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
    "token": "GigaChat token"
}
```

### Start on linux
```bash
./bin/run.sh
```