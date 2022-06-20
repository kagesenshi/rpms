{{- define "spark3.volumes" }}
- name: {{ include "spark3.fullname" . }}-config
  secret:
    secretName: {{ include "spark3.fullname" . }}-config
- name: {{ include "spark3.fullname" . }}-datadir
  emptyDir: {}
{{- end }}

{{- define "spark3.volume-mounts" }}
- name: {{ include "spark3.fullname" . }}-config
  mountPath: "/etc/spark3/"
- name: {{ include "spark3.fullname" . }}-datadir
  mountPath: "/opt/apache/spark3/work-dir"

{{- end }}

{{- define "spark3.env" -}}
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

{{- end }}

{{- define "spark3.client-env" }}
{{- end }}
