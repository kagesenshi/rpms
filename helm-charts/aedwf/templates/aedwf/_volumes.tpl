{{- define "aedwf.volumes" }}
- name: {{ include "aedwf.fullname" . }}-config
  secret:
    secretName: {{ include "aedwf.fullname" . }}-config
- name: {{ include "aedwf.fullname" . }}-datadir
  persistentVolumeClaim:
    claimName: {{ include "aedwf.fullname" . }}-datadir            
- name: {{ include "aedwf.fullname" . }}-logdir
  emptyDir: {}
- name: {{ include "aedwf.fullname" . }}-spark-config
  secret:
    secretName: {{ .Values.spark.secret_name }}
{{- end }}

{{- define "aedwf.volumeMounts" }}
- name: {{ include "aedwf.fullname" . }}-spark-config
  mountPath: "/etc/spark3/"
- name: {{ include "aedwf.fullname" . }}-config
  mountPath: "/etc/apache-airflow"
- name: {{ include "aedwf.fullname" . }}-datadir
  mountPath: "/var/lib/apache-airflow"
- name: {{ include "aedwf.fullname" . }}-logdir
  mountPath: "/var/log/apache-airflow"
{{- end }}


{{- define "aedwf.env" }}
- name: AIRFLOW__CORE__FERNET_KEY
  valueFrom:
    secretKeyRef:
      name: {{ include "aedwf.fullname" . }}-secrets
      key: fernet-key
- name: CELERY_WORKERS
  value: "2"
- name: SPARK_HOME
  value: /opt/apache/spark3
- name: SPARK_CONF_DIR
  value: /etc/spark3/
- name: JAVA_HOME
  value: /usr/lib/jvm/jre-1.8.0/
- name: PYSPARK_PYTHON
  value: /opt/apache/spark3-python/bin/python
- name: SPARK_WORKER_DIR
  value: /opt/apache/spark3/work-dir/worker
- name: K8S_POD_NAME
  valueFrom:
    fieldRef:
      fieldPath: metadata.name
{{- end }}
