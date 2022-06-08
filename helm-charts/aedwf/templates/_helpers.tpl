{{/*
Expand the name of the chart.
*/}}
{{- define "aedwf.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "aedwf.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
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
{{- define "aedwf.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "aedwf.labels" -}}
helm.sh/chart: {{ include "aedwf.chart" . }}
{{ include "aedwf.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "aedwf.selectorLabels" -}}
app.kubernetes.io/name: {{ include "aedwf.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "aedwf.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "aedwf.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}


{{/* 
  Airflow configuration
*/}}
{{- define "airflow-config" -}}
[core]
dags_folder = /airflow/dags/
default_timezone = {{ .Values.airflow.default_timezone }}
executor = CeleryExecutor
sql_alchemy_conn = {{ .Values.airflow.db_uri }}
sql_engine_encoding = utf-8
sql_alchemy_pool_enabled = True
sql_alchemy_pool_size = {{ .Values.airflow.db_pool_size | default "5" }}
sql_alchemy_max_overflow = {{ .Values.airflow.db_pool_max_overflow | default "10" }}
sql_alchemy_pool_recycle = {{ .Values.airflow.db_pool_recycle | default "1800" }}
sql_alchemy_pool_pre_ping = True
sql_alchemy_schema =
parallelism = {{ .Values.airflow.task_parallelism | default "32" }}
max_active_tasks_per_dag = {{ .Values.airflow.max_active_tasks_per_dag | default "16" }}
dags_are_paused_at_creation = {{ .Values.airflow.dags_paused_at_creation | default "True" }}
max_active_runs_per_dag = {{ .Values.airflow.max_active_runs_per_dag | default "16" }}
load_examples = False
load_default_connections = False
plugins_folder = /airflow/plugins/
execute_tasks_new_python_interpreter = True
donot_pickle = False
dag_file_processor_timeout = 50
task_runner = StandardTaskRunner
default_impersonation = apache-airflow
security = 
unit_test_mode = False
enable_xcom_pickling = False
killed_task_cleanup_time = 150

[logging]
base_log_folder = /var/log/apache-airflow/
{{ if .Values.airflow.remote_logging_enabled }}
remote_logging = True
remote_log_conn_id = {{ .Values.airflow.remote_log_conn_id | default "" }}
remote_base_log_folder = {{ .Values.airflow.remote_log_folder | default "" }}
{{ else }}
remote_logging = False
{{ end }}
encrypt_s3_logs = False
logging_level = INFO
fab_logging_level = WARNING
colored_console_log = True
dag_processor_manager_log_location = /var/log/apache-airflow/dag_processor_manager/dag_processor_manager.log
worker_log_server_port = 8793

[metrics]
statsd_on = False
statsd_host = localhost
statsd_port = 8125
statsd_prefix = airflow

[lineage]
backend = 

[atlas]
sasl_enabled = False
host =
port = 21000
username =
password =

[celery]
celery_app_name = airflow.executors.celery_executor
worker_concurrency = 8
worker_umask = 0o077
broker_url = redis://redis:6379/0
result_backend = redis://redis:6379/1
flower_host = 0.0.0.0
flower_url_prefix =
flower_port = 5555
flower_basic_auth =
sync_parallelism = 0
celery_config_options = airflow.config_templates.default_celery.DEFAULT_CELERY_CONFIG
ssl_active = False
ssl_key =
ssl_cert =
ssl_cacert =
pool = prefork
operation_timeout = 1.0
task_track_started = True
task_adoption_timeout = 600
task_publish_max_retries = 3
worker_precheck = False

[scheduler]
child_process_log_directory = /var/log/apache-airflow/scheduler

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
Webserver Config 
*/}}
{{- define "airflow-webserver-config" }}
"""Default configuration for the Airflow webserver"""
import os

from airflow.www.fab_security.manager import AUTH_DB
basedir = os.path.abspath(os.path.dirname(__file__))
WTF_CSRF_ENABLED = True
AUTH_TYPE = AUTH_DB

{{ end }}