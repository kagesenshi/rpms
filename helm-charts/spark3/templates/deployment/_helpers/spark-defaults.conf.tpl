{{- define "spark-defaults" -}}
spark.master                     k8s://https://kubernetes
spark.history.provider           org.apache.hadoop.fs.s3a.S3AFileSystem
spark.history.fs.logDirectory    s3a://{{ .Values.spark.bucket | default "spark" }}/event_log/
spark.eventLog.enabled           true
spark.eventLog.dir               s3a://{{ .Values.spark.bucket | default "spark" }}/event_log/
spark.dynamicAllocation.enable   true
spark.dynamicAllocation.shuffleTracking.enabled true
spark.dynamicAllocation.minExecutors    0
spark.executor.instances         {{ .Values.spark.executor_instances }}

spark.hadoop.fs.s3a.endpoint     {{ .Values.s3a.endpoint }}
spark.hadoop.fs.s3a.access.key   {{ .Values.s3a.access_key }}
spark.hadoop.fs.s3a.secret.key   {{ .Values.s3a.secret_key }}
spark.hadoop.fs.s3a.path.style.access  true
spark.hadoop.fs.s3a.impl         org.apache.hadoop.fs.s3a.S3AFileSystem
spark.hadoop.fs.s3a.committer.name    magic
spark.hadoop.fs.s3a.committer.magic.enabled    true
spark.hadoop.fs.s3a.aws.credentials.provider    org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider
spark.hadoop.mapreduce.outputcommitter.factory.scheme.s3a org.apache.hadoop.fs.s3a.commit.S3ACommitterFactory

spark.kubernetes.driver.volumes.emptyDir.{{ include "spark3.fullname" . }}-datadir.mount.path    /opt/apache/spark3/work-dir
spark.kubernetes.executor.volumes.emptyDir.{{ include "spark3.fullname" . }}-datadir.mount.path    /opt/apache/spark3/work-dir


spark.sql.catalogImplementation  hive
spark.sql.warehouse.dir          s3a://{{ .Values.spark.bucket | default "spark" }}/tablespace/
spark.sql.extensions             io.delta.sql.DeltaSparkSessionExtension
spark.sql.catalog.spark_catalog  org.apache.spark.sql.delta.catalog.DeltaCatalog
spark.sql.sources.commitProtocolClass org.apache.spark.internal.io.cloud.PathOutputCommitProtocol
spark.sql.parquet.output.committer.class     org.apache.spark.internal.io.cloud.BindingParquetOutputCommitter


spark.kubernetes.container.image {{ .Values.image.repository }}:{{ .Values.image.tag }}
spark.kubernetes.container.image.pullPolicy {{ .Values.image.pullPolicy }}
spark.blockManager.port {{ .Values.spark.blockmanager_port | default "2044" }}
spark.executor.cores {{ .Values.spark.executor_cores }}
spark.executor.memory {{ .Values.spark.executor_memory }}


spark.kubernetes.executor.podNamePrefix	{{ include "spark3.fullname" . }}
spark.kubernetes.memoryOverheadFactor   {{ .Values.spark.memory_overhead_factor }}

{{- end }}
