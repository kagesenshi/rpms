{{- define "spark-defaults" -}}
spark.master                     spark://{{ include "spark3.fullname" . }}-master:7077
spark.eventLog.enabled           true
spark.eventLog.dir               /var/log/spark3/event_log/
spark.history.fs.logDirectory    /var/log/spark3/event_log/
spark.sql.warehouse.dir          /var/lib/spark3/warehouse/
spark.kubernetes.container.image {{ .Values.image.repository }}:{{ .Values.image.tag }}
spark.kubernetes.container.image.pullPolicy {{ .Values.image.pullPolicy }}
spark.blockManager.port {{ .Values.spark.blockmanager_port | default "2044" }}
{{- end }}
