{{- define "spark-defaults" -}}
spark.master                     spark://{{ include "spark3.fullname" . }}-master:7077
spark.eventLog.enabled           true
spark.eventLog.dir               /var/log/spark3/event_log/
spark.history.fs.logDirectory    /var/log/spark3/event_log/
spark.sql.warehouse.dir          /var/lib/spark3/warehouse/
spark.hadoop.fs.s3a.endpoint     {{ .Values.spark.s3a_endpoint }}
spark.hadoop.fs.s3a.access.key   {{ .Values.spark.s3a_access_key }}
spark.hadoop.fs.s3a.secret.key   {{ .Values.spark.s3a_secret_key }}
spark.hadoop.fs.s3a.path.style.access  true
spark.hadoop.fs.s3a.impl         org.apache.hadoop.fs.s3a.S3AFileSystem
spark.hadoop.fs.s3a.aws.credentials.provider org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider
spark.sql.extensions             io.delta.sql.DeltaSparkSessionExtension
spark.sql.catalog.spark_catalog  org.apache.spark.sql.delta.catalog.DeltaCatalog
spark.kubernetes.container.image {{ .Values.image.repository }}:{{ .Values.image.tag }}
spark.kubernetes.container.image.pullPolicy {{ .Values.image.pullPolicy }}
spark.blockManager.port {{ .Values.spark.blockmanager_port | default "2044" }}
{{- end }}
