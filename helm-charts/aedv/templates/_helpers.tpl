{{/*
Expand the name of the chart.
*/}}
{{- define "aedv.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 50 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "aedv.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 50 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "aedv.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "aedv.labels" -}}
helm.sh/chart: {{ include "aedv.chart" . }}
{{ include "aedv.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "aedv.selectorLabels" -}}
app.kubernetes.io/name: {{ include "aedv.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "aedv.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "aedv.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}


{{/* 
Superset configuration
*/}}
{{- define "superset-config" -}}
from celery.schedules import crontab
from flask_caching.backends.rediscache import RedisCache
from selenium import webdriver

import os

FEATURE_FLAGS = {
    'THUMBNAILS': True,
    'THUMBNAILS_SQLA_LISTENERS': True
}

SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY')
if os.environ.get('SUPERSET_PREVIOUS_SECRET_KEY'):
    PREVIOUS_SECRET_KEY = os.environ.get('SUPERSET_PREVIOUS_SECRET_KEY')

SQLALCHEMY_DATABASE_URI={{ quote .Values.superset.db_uri }}
DATA_DIR = "/var/lib/apache-superset"
class CeleryConfig:  # pylint: disable=too-few-public-methods
    {{ if .Values.superset.broker_url -}}
    BROKER_URL = {{ quote .Values.superset.broker_url }}
    {{- else -}}
    BROKER_URL = "redis://{{ include "aedv.fullname" . }}-redis:{{ .Values.redis_service.port }}/0"
    {{- end }}
    CELERY_IMPORTS = ("superset.sql_lab", "superset.tasks",
                      "superset.tasks.thumbnails")
    {{ if .Values.superset.celery_result_backend -}}
    CELERY_RESULT_BACKEND = {{ quote .Values.superset.celery_result_backend }}
    {{- else -}}
    CELERY_RESULT_BACKEND = "redis://{{ include "aedv.fullname" . }}-redis:{{ .Values.redis_service.port }}/3"
    {{- end }}
    CELERYD_LOG_LEVEL = {{ quote .Values.superset.celeryd_debug_level }}
    CELERYD_PREFETCH_MULTIPLIER = 10
    CELERY_ACKS_LATE = True
    CELERY_ANNOTATIONS = {
        "sql_lab.get_sql_results": {"rate_limit": "100/s"},
        "email_reports.send": {
            "rate_limit": "1/s",
            "time_limit": 120,
            "soft_time_limit": 150,
            "ignore_result": True,
        },
    }
    CELERYBEAT_SCHEDULE = {
        "email_reports.schedule_hourly": {
            "task": "email_reports.schedule_hourly",
            "schedule": crontab(minute=1, hour="*"),
        },
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=0, hour=0),
        },
    }

CELERY_CONFIG = CeleryConfig

RESULTS_BACKEND = RedisCache(
    host="{{ include "aedv.fullname" . }}-redis", 
    port={{ .Values.redis_service.port }}, key_prefix='superset_results')

THUMBNAIL_CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,
    'CACHE_KEY_PREFIX': 'superset_thumbnail',
    {{ if .Values.superset.cache_redis_url -}}
    'CACHE_REDIS_URL': {{ quote .Values.superset.cache_redis_url }},
    {{- else -}}
    'CACHE_REDIS_URL': "redis://{{ include "aedv.fullname" . }}-redis:{{ .Values.redis_service.port }}/1",
    {{- end }}
}

{{ if .Values.smtp.enabled }}
# smtp server configuration
EMAIL_NOTIFICATIONS = True  # all the emails are sent using dryrun
SMTP_HOST = {{ .Values.smtp.host | quote }}
{{ if .Values.smtp.use_tls }}
SMTP_STARTTLS = True
{{ else }}
SMTP_STARTTLS = False
{{ end }}
{{ if .Values.smtp.use_ssl }}
SMTP_SSL = True
{{ else }}
SMTP_SSL = False
{{ end }}
SMTP_USER = {{ .Values.smtp.username | quote }}
SMTP_PORT = {{ .Values.smtp.port }}
SMTP_PASSWORD = {{ .Values.smtp.password | quote }}
SMTP_MAIL_FROM = {{ .Values.smtp.from | quote }}
{{ end }}

PREFERRED_DATABASES = [
    "PostgreSQL",
    "Presto",
    "MySQL",
]

WEBDRIVER_BASEURL = "http{{ if .Values.ingress.tls }}s{{ end }}://{{ .Values.ingress.host }}/"
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_OPTION_ARGS = [
    "--headless",
]

webdrv_opts = webdriver.ChromeOptions()
webdrv_opts.add_argument("--headless")
webdrv_opts.add_argument("--no-sandbox")
webdrv_opts.add_argument("--window-size=800,600")
webdrv_opts.add_argument("--disable-dev-shm-usage")
webdrv_opts.add_argument("--ignore-certificate-errors")

WEBDRIVER_CONFIGURATION = {
   "executable_path": "/usr/bin/chromedriver",
   "service_log_path": "/var/log/apache-superset/chromedriver",
   "options": webdrv_opts
}

UPLOAD_FOLDER = '/var/lib/apache-superset/uploads'
UPLOAD_FOLDER = '/var/lib/apache-superset/'
{{- end }}


{{/* 
Redis configuration
*/}}
{{- define "redis-config" -}}
bind * -::*
protected-mode yes
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
pidfile /var/run/redis_6379.pid
loglevel notice
logfile /var/log/redis/redis.log
databases 16
always-show-logo no
set-proc-title yes
proc-title-template "{title} {listen-addr} {server-mode}"
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
rdb-del-sync-files no
dir /var/lib/redis
replica-serve-stale-data yes
replica-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-diskless-load disabled
repl-disable-tcp-nodelay no
replica-priority 100
acllog-max-len 128
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no
lazyfree-lazy-user-del no
lazyfree-lazy-user-flush no
oom-score-adj no
oom-score-adj-values 0 200 800
disable-thp yes
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
stream-node-max-bytes 4096
stream-node-max-entries 100
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
dynamic-hz yes
aof-rewrite-incremental-fsync yes
rdb-save-incremental-fsync yes
jemalloc-bg-thread yes
{{ end }}

{{/* 
Redis sentinel configuration
*/}}
{{- define "redis-sentinel-config" -}}
port 26379
daemonize no
pidfile /var/run/redis-sentinel.pid
logfile /var/log/redis/sentinel.log
dir /tmp
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 30000
acllog-max-len 128
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 180000
sentinel deny-scripts-reconfig yes
SENTINEL resolve-hostnames no
SENTINEL announce-hostnames no
{{ end }}


{{/* 
SSL key
*/}}
{{- define "server.key" -}}
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDMsSZ28Mj4sSrp
q+2Nq2qbqeYeGtbZwxkUkhL6HJWkCeohI5zMjLRc+QxLkAoQpI5ret+x1KkEyPxU
GCLZTa4Vc4STxMlLisPdT1kSfnlG9AnuipdDOalM5yjYNha5vV2la2df7ExKqNIT
PdS7lQC/yyQk9WQT3BgF2PDXq/DQSqtZBepGNyp5Iseh6ZVEu/4qPLQikb/+nkId
xP7c/wyMeTy139qizfBUvn837mkC9Ze1bp+7UpjkHikS2IEgSIhK2mSvZQpMjATz
HFEUveKgk0WlOOohtIkQg2i2ULDsHs8AxS2kvoWKOuVMl1UZ31TZkGK0jYt9BwEc
k/gr0CCdAgMBAAECggEAX0n0uxgaptNrQ7665uGuzmqIaulZraRKT6400WRvMR9A
dE7s1riF2mZCGAck+FxyxIw+CL4UNNsPxGI8Duc/rFLLnDLW9qjRx3wB3j8sXCCN
YxP3mN8F9nwCIq0DZVJHfxOB20DYv0TaDwUQvIaAA8kguWfXP/uM32P/spcjkwLq
ZUe96NpQmUagJWRQGZ1X4/yDpIIXSEL0inyIv1b1fDD/YVrA1+N+xW/ZQq14zu38
NAmkxbnMnQoep/1/NlDPB9frV04ucPgZtzG89c19KnDPZTbr9udGaJltobnq/XZQ
CtXATMYBkYfcVudwc/GPzvCwQ+r64zl7JuTMdkYqzQKBgQDv9BycK2fbJ/97ZKaa
ZDFkEagFKS+QffGoR52BP6Lwwq/n7XKgxtstyncAZ9Hvos4HNqt0qm0rzeUDhBGc
zvhP32hzM3AzSqy+dKlkVn+POgaRRs/uc6yh7zJ8/5dgWnz9cxdf+CWmKfNCDzmN
u4JrWwvj/O0PLkniGTTP5wHLcwKBgQDaYWCqPa5HeY4nOgKvLKbzZfef3scsL2wo
8vwoY4GtJu42jBx8iWuXuuIIyiF2cZwHqdntFlQoqxB+ukQZpM/LMom4xIz4YH4Y
BbUerFmjfjIRFJNHzdsVhlyKUYp+2ap/vYJYcIpac0X8WGmKOG1gkxivpfhh8QIx
Qqgjkbh/rwKBgGFfm5iYWK3rvlZxktZGYHCuZZOqkf29ziou3bDMhS/UoZOpnQG3
kMw1RDNq7huj4p20xsEyQ9kp1YymtIsAxm2LSJSvRBHcdNtY9kCchWk27+FWbhzi
3iRcsA1fnytfrScg5FRym7yhe3DMQtvMQvGT4fBj/ENT0nGpLvBLW0QXAoGBAKsD
eumWZ/Z9EH9ThGqd8xfEkEhX8218rZzbu+/9DL4GMKHy0xQLoYAuz3fGorHYgjHW
J1ztEXbPj5lOUKosULV1nDhfY23WUqiJP68HlSLdXmPV0wh2As02bR28gVKZLlXe
mEadyxrODs5whiXBzpXEW56hwIMic28UHgvMv8jtAoGBAIa1M74g3WFMbjKmwu7C
Njt6Kg0XbsV1/+ROypmL3+Np9J//gIU4pkmahVqAwZa765qnKyjrhaWPCoT/RDcq
AM+g2IJWplBiKBKBeZQJfRcSX+1P9JK8YeV+xh1j/8WZx1dK/GFEPuVyGvxt+4Qr
VVpsPCxsj29Z21WESAiNLdlp
-----END PRIVATE KEY-----
{{ end }}


{{/* 
SSL key
*/}}
{{- define "server.crt" -}}
-----BEGIN CERTIFICATE-----
MIIEWTCCA0GgAwIBAgIUJdsaWDaU0t6k66Jnb6brTVGbIukwDQYJKoZIhvcNAQEL
BQAwgbsxCzAJBgNVBAYTAi0tMRIwEAYDVQQIDAlTb21lU3RhdGUxETAPBgNVBAcM
CFNvbWVDaXR5MRkwFwYDVQQKDBBTb21lT3JnYW5pemF0aW9uMR8wHQYDVQQLDBZT
b21lT3JnYW5pemF0aW9uYWxVbml0MR4wHAYDVQQDDBVsb2NhbGhvc3QubG9jYWxk
b21haW4xKTAnBgkqhkiG9w0BCQEWGnJvb3RAbG9jYWxob3N0LmxvY2FsZG9tYWlu
MB4XDTIxMDUzMTEzMDcxM1oXDTIyMDUzMTEzMDcxM1owgbsxCzAJBgNVBAYTAi0t
MRIwEAYDVQQIDAlTb21lU3RhdGUxETAPBgNVBAcMCFNvbWVDaXR5MRkwFwYDVQQK
DBBTb21lT3JnYW5pemF0aW9uMR8wHQYDVQQLDBZTb21lT3JnYW5pemF0aW9uYWxV
bml0MR4wHAYDVQQDDBVsb2NhbGhvc3QubG9jYWxkb21haW4xKTAnBgkqhkiG9w0B
CQEWGnJvb3RAbG9jYWxob3N0LmxvY2FsZG9tYWluMIIBIjANBgkqhkiG9w0BAQEF
AAOCAQ8AMIIBCgKCAQEAzLEmdvDI+LEq6avtjatqm6nmHhrW2cMZFJIS+hyVpAnq
ISOczIy0XPkMS5AKEKSOa3rfsdSpBMj8VBgi2U2uFXOEk8TJS4rD3U9ZEn55RvQJ
7oqXQzmpTOco2DYWub1dpWtnX+xMSqjSEz3Uu5UAv8skJPVkE9wYBdjw16vw0Eqr
WQXqRjcqeSLHoemVRLv+Kjy0IpG//p5CHcT+3P8MjHk8td/aos3wVL5/N+5pAvWX
tW6fu1KY5B4pEtiBIEiIStpkr2UKTIwE8xxRFL3ioJNFpTjqIbSJEINotlCw7B7P
AMUtpL6FijrlTJdVGd9U2ZBitI2LfQcBHJP4K9AgnQIDAQABo1MwUTAdBgNVHQ4E
FgQUla41RKZFObKVhbcvh+97VNFwNtgwHwYDVR0jBBgwFoAUla41RKZFObKVhbcv
h+97VNFwNtgwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEApb4V
ojS8xDbttWNRdcVlPtAmC1dpMdoBm1Cf6L1EjPX5oWHgkC1/s6D4YOCfxWd7emWv
A6Vfb3mZSUMwnnnHf13x9zNef0B+oj5ldA2tPgvCZUBW5YqLBXEqrP3/l3SdjKHY
GuuQoPcJ8hNKpsYwWUsX6zkOVhT+54g0cnPXfJDNe49DO7YzujagqHVwogsV0Sla
zWBoGGy9LqrObwukR1Mf3GcS2f4YV2olfh/qCi9+BtKaOmX1leEeO6j13XtOjPxI
xTNkltPf2k7IctD26L62a8RdFLDFZkwzI2qhcIplfD5xv/Yey7a9uIDkv/63Z7SL
iaxMmqkCjaZg7gCncQ==
-----END CERTIFICATE-----
{{ end }}
