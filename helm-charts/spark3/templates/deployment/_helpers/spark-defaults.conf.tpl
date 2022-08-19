{{- define "spark-defaults" -}}
spark.master                     {{ .Values.spark.master | default "k8s://https://kubernetes.default" }}
spark.kubernetes.namespace       {{ .Values.spark.k8s_namespace | default "default" }}
spark.history.provider           org.apache.hadoop.fs.s3a.S3AFileSystem
spark.history.fs.logDirectory    s3a://{{ .Values.spark.bucket | default "spark" }}/event_log/
spark.eventLog.enabled           true
spark.eventLog.dir               s3a://{{ .Values.spark.bucket | default "spark" }}/event_log/
spark.dynamicAllocation.enable   true
spark.dynamicAllocation.shuffleTracking.enabled true
spark.dynamicAllocation.minExecutors    0
spark.executor.instances         {{ .Values.spark.executor_instances }}

spark.hadoop.fs.defaultFS        s3a://{{ .Values.spark.bucket | default "spark" }}/
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
spark.kubernetes.allocation.batch.delay	15s


spark.sql.catalogImplementation  hive
spark.sql.warehouse.dir          s3a://{{ .Values.spark.bucket | default "spark" }}/tablespace/

spark.sql.sources.commitProtocolClass org.apache.spark.internal.io.cloud.PathOutputCommitProtocol
spark.sql.parquet.output.committer.class     org.apache.spark.internal.io.cloud.BindingParquetOutputCommitter


spark.kubernetes.container.image {{ .Values.image.repository }}:{{ .Values.image.tag }}
spark.kubernetes.container.image.pullPolicy {{ .Values.image.pullPolicy }}
spark.blockManager.port {{ .Values.spark.blockmanager_port | default "2044" }}
spark.executor.cores {{ .Values.spark.executor_cores }}
spark.executor.memory {{ .Values.spark.executor_memory }}


spark.kubernetes.executor.podNamePrefix	${env:K8S_POD_NAME}
spark.kubernetes.driver.pod.name	${env:K8S_POD_NAME}
spark.kubernetes.memoryOverheadFactor   {{ .Values.spark.memory_overhead_factor }}

spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
spark.sql.catalog.spark_catalog=org.apache.iceberg.spark.SparkSessionCatalog
spark.sql.catalog.spark_catalog.type=hive

spark.driver.extraJavaOptions {{ .Values.spark.driver_java_options }}
spark.executor.extraJavaOptions {{ .Values.spark.executor_java_options }}

spark.sql.parquet.int96RebaseModeInWrite {{ .Values.spark.int96_rebase | default "CORRECTED" }}
{{- end }}
