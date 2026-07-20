# Personal Site - Server Configuration Reference
> Rocky Linux 9 · PostgreSQL 18 · Garage S3 · Gunicorn · nginx · certbot

---

## Directory Structure

```
/opt/personalsite/
├── app/                        # Django source code & working directory for gunicorn
└── env/                        # Python virtual environment

/var/www/personalsite/
└── static/                     # STATIC_ROOT - served by nginx

/var/lib/garage/
└── meta/                       # Garage metadata directory

/mnt/[second-drive]/garage/
└── data/                       # Garage object data (second drive)

/var/lib/pgsql/18/data/         # PostgreSQL data directory
                                # (or on second drive if moved)

/etc/personalsite/
└── env                         # Secrets EnvironmentFile

/etc/garage.toml                # Garage config

/etc/nginx/conf.d/
├── personalsite_dev.conf       # nginx development site config
└── personalsite_prod.conf      # nginx production site config

/etc/systemd/system/
├── personalsite.service        # Gunicorn service unit
└── garage.service              # Garage service unit

/var/log/personalsite/          # Gunicorn access + error logs
/run/gunicorn/                  # Gunicorn socket - tmpfs, auto-created by systemd
/etc/letsencrypt/               # SSL certificates (managed by Certbot)
```

---

## System Preparation

- Update system packages
  ```bash
  sudo dnf update -y
  ```
- Open firewall ports
  ```bash
  sudo firewall-cmd --permanent --add-service=http
  sudo firewall-cmd --permanent --add-service=https
  sudo firewall-cmd --reload
  ```
- development firewall port
  ```bash
  sudo firewall-cmd --permanent --add-rich-rule='
    rule family="ipv4"
    source address="192.168.1.0/24"
    port protocol="tcp" port="8080"
    accept'
  sudo firewall-cmd --reload
  ```
- Create application service user (no login shell)
  ```bash
  sudo useradd --system --no-create-home --shell /sbin/nologin personalsite
  ```
- Create Garage service user
  ```bash
  sudo useradd --system --no-create-home --shell /sbin/nologin garage
  ```

---

## PostgreSQL 18

- Add official repo and disable built-in module
- https://www.postgresql.org/download/linux/redhat/
  ```bash
  sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm
  sudo dnf -qy module disable postgresql
  ```
- Install PostgreSQL 18
  ```bash
  sudo dnf install -y postgresql18-server postgresql18 postgresql18-contrib
  ```
- Optional: Add binaries to PATH
  ```bash
  echo 'export PATH=/usr/pgsql-18/bin:$PATH' | sudo tee /etc/profile.d/postgresql18.sh
  source /etc/profile.d/postgresql18.sh
  ```
- Initialise database cluster
  ```bash
  sudo /usr/pgsql-18/bin/postgresql-18-setup initdb
  sudo systemctl enable --now postgresql-18
  ```
- Configure `pg_hba.conf` - add line for Django user
  ```
  # /var/lib/pgsql/18/data/pg_hba.conf
  host    personalsite    django_user     127.0.0.1/32    scram-sha-256
  ```
- Reload PostgreSQL after config change
  ```bash
  sudo systemctl reload postgresql-18
  ```
- Create database and user
  ```sql
  sudo -u postgres psql
  CREATE DATABASE personalsite;
  CREATE USER django_user WITH PASSWORD 'yourpassword';
  ALTER ROLE django_user SET client_encoding TO 'utf8';
  ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';
  ALTER ROLE django_user SET timezone TO 'UTC';
  GRANT ALL PRIVILEGES ON DATABASE personalsite TO django_user;
  \c personalsite
  GRANT ALL ON SCHEMA public TO django_user;
  \q
  ```
- Verify connection
  ```bash
  psql -U django_user -h 127.0.0.1 -d personalsite
  ```

---

## Garage S3

- https://garagehq.deuxfleurs.fr/documentation/quick-start/
- Download Garage binary 
- https://garagehq.deuxfleurs.fr/download/
  ```bash
  wget <linux/amd64 link>
  chmod +x garage && sudo mv garage /usr/local/bin/
  ```
- Create data directories and set ownership
  ```bash
  sudo mkdir -p /var/lib/garage/meta
  sudo mkdir -p /mnt/[second-drive]/garage/data
  sudo chown -R garage:garage /var/lib/garage
  sudo chown -R garage:garage /mnt/[second-drive]/garage
  ```
- Write `/etc/garage.toml`
  ```
  cat > garage.toml <<EOF
  ...file contents of garage.txt...
  EOF
  ```
- Write `/etc/systemd/system/garage.service`
- Enable and start Garage
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable --now garage
  ```
- Apply node layout (required before Garage is usable)
  ```bash
  garage status           # note the node ID
  garage layout assign [NODE_ID] --zone dc1 --capacity 1T
  garage layout apply
  ```
- Create bucket and enable website mode
  ```bash
  garage bucket create personal-site-bucket
  garage bucket website --allow personal-site-bucket
  ```
- Create API key and grant access
  ```bash
  garage key create django-key
  garage bucket allow --read --write personal-site-bucket --key [KEY_ID]
  garage key info django-key   # shows access + secret key - save these
  ```

---

## Django Application

- Copy source to `/opt/personalsite/app/`
- Create virtual environment and install dependencies
  ```bash
  python -m venv /opt/personalsite/env
  source /opt/personalsite/env/bin/activate
  pip install -r /opt/personalsite/app/requirements.txt
  ```
- Create secrets file `/etc/personalsite/env`
  ```bash
  sudo mkdir /etc/personalsite
  sudo vim /etc/personalsite/env
  # Contents - no export keyword, no quotes unless value has spaces:
  # DJANGO_SECRET_KEY=...
  # DB_PASSWORD=...
  # GARAGE_ACCESS_KEY=...
  # GARAGE_SECRET_KEY=...
  # DJANGO_ADMIN_URL=...
  sudo chown root:root /etc/personalsite/env
  sudo chmod 600 /etc/personalsite/env
  ```
- Make static files directory
  ```bash
  sudo mkdir -p /var/www/personalsite/static
  ```
- Collect static files
  ```bash
  ./manage.py collectstatic --noinput
  ```
- Run database migrations
  ```bash
  export $(sudo cat /etc/personalsite/env | xargs)
  ./manage.py migrate
  ```
- Create Django superuser
  ```bash
  ./manage.py createsuperuser
  ```
- Set ownership of app directories
  ```bash
  sudo chown -R personalsite:personalsite /opt/personalsite
  sudo chown -R personalsite:personalsite /var/www/personalsite
  ```

---

## Gunicorn (systemd)

- Write `/etc/systemd/system/personalsite.service`
- Create log directory
  ```bash
  sudo mkdir -p /var/log/personalsite
  sudo chown personalsite:personalsite /var/log/personalsite
  ```
- Enable and start
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable --now personalsite
  sudo systemctl status personalsite
  ```
- Confirm socket exists
  ```bash
  ls -la /run/gunicorn/
  ```

---

## nginx

- Install nginx
  ```bash
  sudo dnf install nginx -y
  sudo systemctl enable --now nginx
  ```
  ```bash
  ```
- Write `/etc/nginx/conf.d/personalsite.conf`
- Validate config and reload
  ```bash
  sudo nginx -t
  sudo systemctl reload nginx
  ```
- Smoke test before SSL
  ```bash
  curl -I http://localhost
  ```

---

## SSL (Let's Encrypt)

- Confirm DNS A record points to this server's public IP
- Install Certbot
  ```bash
  sudo dnf install certbot python3-certbot-dns-cloudflare -y
  ```
- Make cloudlfare API key and store it in `/etc/letsencrypt/cloudflare.ini`
  - Token requires permissions for `Zone:DNS:Edit`
  ```
  dns_cloudflare_api_token = [API token]
  ```
- Secure permissions for the API token
  ```
  sudo chmod 600 /etc/letsencrypt/cloudflare.ini
  ```
- Get SSL cert
  ```
  sudo certbot certonly --dns-cloudflare \
    --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
    --dns-cloudflare-propagation-seconds 60 \
    -d emelavm.com -d www.emelavm.com
  ```
- nginx config is set up for certs at `/etc/letsencrypt/live/emelavm.com/
- Set up the cron job to renew SSL certs
  ```
  SLEEPTIME=$(awk 'BEGIN{srand(); print int(rand()*(3600+1))}'); echo "0 0,12 * * * root sleep $SLEEPTIME && certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
  ```

---

## Verification

- HTTPS response
  ```bash
  curl -I https://emelavm.com
  ```
- Static files served by nginx
  ```bash
  curl -I 
  ```
- Media proxy via Garage
  ```bash
  curl -I https://emelavm.com/media/embeds/[any-uploaded-file]
  ```
- Check all logs are clean
  ```bash
  sudo journalctl -u personalsite -n 50
  sudo journalctl -u garage -n 50
  sudo tail -f /var/log/nginx/error.log
  sudo tail -f /var/log/personalsite/error.log
  ```

---

## Key Service Commands (Quick Reference)

- `sudo systemctl <start|stop|status|reload|restart> <service-name>`
- Services
  - Django/Gunicorn - `personalsite`
  - Garage = `garage`
  - PostgreSQL = `postgresql-18`
  - nginx = `nginx`
- Reloading
  - use `restart` for django & garage
  - use `reload` for postresql & nginx

## Deploy Update Procedure (after code changes)

```bash
cd /opt/personalsite/app
git pull
source /opt/personalsite/env/bin/activate
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
sudo systemctl restart personalsite
sudo systemctl reload nginx
```
