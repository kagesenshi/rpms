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
SQLALCHEMY_DATABASE_URI={{ quote .Values.superset.db_uri }}
DATA_DIR = "/var/lib/apache-superset"
class CeleryConfig:  # pylint: disable=too-few-public-methods
    BROKER_URL = {{ quote .Values.superset.broker_url }}
    CELERY_IMPORTS = ("superset.sql_lab", "superset.tasks",
                      "superset.tasks.thumbnails")
    CELERY_RESULT_BACKEND = {{ quote .Values.superset.celery_result_backend }}
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
        }
    }

CELERY_CONFIG = CeleryConfig

THUMBNAIL_CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,
    'CACHE_KEY_PREFIX': 'superset_thumbnail',
    'CACHE_REDIS_URL': {{ quote .Values.superset.cache_redis_url }},
}

WEBDRIVER_BASEURL = {{ quote .Values.superset.base_url }}
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_OPTION_ARGS = [
    "--headless",
]

webdrv_opts = webdriver.ChromeOptions()
webdrv_opts.add_argument("--headless")
webdrv_opts.add_argument("--no-sandbox")
webdrv_opts.add_argument("--window-size=800,600")
webdrv_opts.add_argument("--disable-dev-shm-usage")

WEBDRIVER_CONFIGURATION = {
   "executable_path": "/usr/bin/chromedriver",
   "service_log_path": "/var/log/apache-superset/chromedriver",
   "options": webdrv_opts
}
{{- end }}
