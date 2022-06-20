{{- define "spark-env" -}}
umask 002
export JAVA_HOME=/usr/lib/jvm/jre-1.8.0/
export PYSPARK_PYTHON=/opt/apache/spark3-python/bin/python
export SPARK_HOME=/opt/apache/spark3/
export SPARK_WORKER_DIR=/opt/apache/spark3/work-dir/worker

{{- end }}
