{{- define "spark-env" -}}
#!/usr/bin/env bash

export JAVA_HOME=/usr/lib/jvm/jre-1.8.0/
export PYSPARK_PYTHON=/opt/apache/spark3-python/bin/python
export SPARK_CONF_DIR=/etc/spark3/ 
export SPARK_HOME=/opt/apache/spark3/
export HADOOP_HOME=/opt/apache/hadoop/ 
export JAVA_HOME=/usr/lib/jvm/jre-1.8.0/ 
export SPARK_DIST_CLASSPATH="$(/opt/apache/hadoop/bin/hadoop classpath):/opt/apache/hadoop/share/hadoop/tools/lib/*"
{{- end }}
