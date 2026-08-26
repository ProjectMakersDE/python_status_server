# System Status API

Kleine, authentifizierte Status-API fuer Docker-Container, MongoDB und
Systemressourcen. Das Container-Image basiert auf Python 3.13 und startet mit
Gunicorn statt dem Flask-Entwicklungsserver.

## Endpunkte

| Endpoint | Authentifizierung | Zweck |
| --- | --- | --- |
| `GET /healthz` | nein | Prozess-/Container-Healthcheck; keine internen Details |
| `GET /status/docker` | HTTP Basic Auth | Namen und Laufzustaende der Docker-Container |
| `GET /status/mongodb` | HTTP Basic Auth | MongoDB-Verbindungstest |
| `GET /status/system` | HTTP Basic Auth | CPU-, Speicher- und Plattennutzung |

Die API darf nicht unverschluesselt im Internet erreichbar sein. Der
Compose-Standard bindet sie deshalb nur an `127.0.0.1`. Fuer Zugriff von
ausserhalb ist ein HTTPS-Reverse-Proxy mit zusaetzlicher Zugriffskontrolle
vorgesehen. `STATUS_SERVER_BIND_ADDRESS=0.0.0.0` ist nur in diesem Fall
angebracht.

## Konfiguration

Die beiden Zugangsdaten sind Pflicht. Der Dienst beendet sich beim Start, wenn
eine davon fehlt, damit keine unklar konfigurierte API online geht.

```env
STATUS_SERVER_USERNAME=status-reader
STATUS_SERVER_PASSWORD=use-a-long-random-secret
STATUS_SERVER_PORT=5000

# Optional: bei Docker Compose standardmaessig 127.0.0.1
STATUS_SERVER_BIND_ADDRESS=127.0.0.1

MONGO_USERNAME=mongoUser
MONGO_PASSWORD=mongoPassword
MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_RULES=?authSource=admin

# Optionales Gunicorn-Tuning
GUNICORN_WORKERS=2
GUNICORN_THREADS=4
GUNICORN_TIMEOUT=30
```

`MONGO_USERNAME` und `MONGO_PASSWORD` muessen entweder beide gesetzt sein oder
beide fehlen. Sonderzeichen in ihnen werden sicher URL-kodiert. Fehlerantworten
enthalten keine Zugangsdaten, Verbindungszeichenfolgen oder internen
Fehlerdetails.

## Start

Die Produktions-Compose-Datei verwendet das veroeffentlichte Image:

```bash
docker compose up -d
```

Fuer eine lokale Image-Pruefung:

```bash
docker build --pull -t projectmakers/pythonstatusserver:local .
```

Das Mounten von `/var/run/docker.sock` ist erforderlich, damit der
Docker-Endpunkt funktioniert. Es gewaehrt dem Dienst jedoch weitreichenden
Host-Zugriff. Deshalb soll dieser Dienst ausschliesslich mit einem dedizierten,
stark geschuetzten Docker-Zugang betrieben werden; ein Socket-Proxy mit nur
Lesezugriff auf Container-Metadaten ist die langfristig bessere Architektur.

## Wartung und Verifikation

Abhaengigkeiten sind exakt versioniert. Dependabot prueft Python- und
Docker-Abhaengigkeiten woechentlich. Die GitHub-Actions-Pipeline installiert
die Abhaengigkeiten, fuehrt `pip-audit`, die Unit-Tests und einen frischen
Docker-Build aus.

Lokal kann die Pruefung so wiederholt werden:

```bash
python -m pip install -r requirements.txt pip-audit
STATUS_SERVER_USERNAME=test-user STATUS_SERVER_PASSWORD=test-password \
  python -m unittest discover -s tests -v
pip-audit --requirement requirements.txt
```
