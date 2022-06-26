{{- define "spark-defaults" -}}
spark.master                     k8s://https://kubernetes
spark.history.provider           org.apache.hadoop.fs.s3a.S3AFileSystem
spark.eventLog.enabled           true
spark.eventLog.dir               s3a://{{ .Values.spark.bucket | default "spark" }}/event_log/
spark.history.fs.logDirectory    s3a://{{ .Values.spark.bucket | default "spark" }}/event_log/
spark.sql.warehouse.dir          s3a://{{ .Values.spark.bucket | default "spark" }}/tablespace/
spark.hadoop.fs.s3a.endpoint     {{ .Values.s3a.endpoint }}
spark.hadoop.fs.s3a.access.key   {{ .Values.s3a.access_key }}
spark.hadoop.fs.s3a.secret.key   {{ .Values.s3a.secret_key }}
spark.hadoop.fs.s3a.path.style.access  true
spark.hadoop.fs.s3a.impl         org.apache.hadoop.fs.s3a.S3AFileSystem
spark.sql.catalogImplementation  hive
spark.hadoop.fs.s3a.aws.credentials.provider org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider
spark.sql.extensions             io.delta.sql.DeltaSparkSessionExtension
spark.sql.catalog.spark_catalog  org.apache.spark.sql.delta.catalog.DeltaCatalog
spark.kubernetes.container.image {{ .Values.image.repository }}:{{ .Values.image.tag }}
spark.kubernetes.container.image.pullPolicy {{ .Values.image.pullPolicy }}
spark.blockManager.port {{ .Values.spark.blockmanager_port | default "2044" }}
spark.executor.cores {{ .Values.spark.executor_cores }}
spark.executor.memory {{ .Values.spark.executor_memory }}
# Parameters to use new commiters
#spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version 2
spark.hadoop.fs.s3a.committer.name magic
spark.hadoop.fs.s3a.committer.magic.enabled true
spark.hadoop.mapreduce.outputcommitter.factory.scheme.s3a org.apache.hadoop.fs.s3a.commit.S3ACommitterFactory
spark.sql.sources.commitProtocolClass org.apache.spark.internal.io.cloud.PathOutputCommitProtocol
spark.sql.parquet.output.committer.class     org.apache.spark.internal.io.cloud.BindingParquetOutputCommitter

{{- end }}
