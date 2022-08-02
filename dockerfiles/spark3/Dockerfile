FROM registry.gitlab.com/abyres/releases/fedora:36

RUN set -ex && \
    dnf copr enable izhar/data-engineering -y && \
    dnf install -y apache-hadoop apache-spark3 apache-spark3-python && \
    mkdir -p /opt/apache/spark3/work-dir && \
    dnf clean all

RUN /opt/apache/spark3-python/bin/pip install ipykernel && \
    /opt/apache/spark3-python/bin/pip install /opt/apache/spark3/python/ 

RUN set -ex && \
    touch /opt/apache/spark3/RELEASE && \
    rm /bin/sh && \
    ln -sv /bin/bash /bin/sh && \
    echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su && \
    chgrp root /etc/passwd && chmod ug+rw /etc/passwd && \
    cp /opt/apache/spark3/kubernetes/dockerfiles/spark/entrypoint.sh /opt/ 

RUN /usr/sbin/groupadd -r sparkuser --gid 1000 && \
     /usr/sbin/useradd -r -g sparkuser --uid 1000 \
     -m -d /home/sparkuser \
     -s /sbin/nologin sparkuser

ADD noop.py /opt/noop.py
ENV SPARK_HOME=/opt/apache/spark3 \
    SPARK_CONF_DIR=/etc/spark3/ \
    HADOOP_HOME=/opt/apache/hadoop/ \
    JAVA_HOME=/usr/lib/jvm/jre-1.8.0/ \
    PATH="/opt/apache/spark3/bin:/opt/apache/hadoop/bin:${PATH}" \
    PYSPARK_PYTHON=/opt/apache/spark3-python/bin/python \
    SPARK_DIST_CLASSPATH="/opt/apache/hadoop//etc/hadoop:/opt/apache/hadoop//share/hadoop/common/lib/*:/opt/apache/hadoop//share/hadoop/common/*:/opt/apache/hadoop//share/hadoop/hdfs:/opt/apache/hadoop//share/hadoop/hdfs/lib/*:/opt/apache/hadoop//share/hadoop/hdfs/*:/opt/apache/hadoop//share/hadoop/mapreduce/lib/*:/opt/apache/hadoop//share/hadoop/mapreduce/*:/opt/apache/hadoop//share/hadoop/yarn:/opt/apache/hadoop//share/hadoop/yarn/lib/*:/opt/apache/hadoop//share/hadoop/yarn/*:/opt/apache/hadoop/share/hadoop/tools/lib/*"

USER root
RUN chown -R sparkuser:sparkuser /opt/apache/spark3/jars/
USER sparkuser
RUN /opt/apache/spark3/bin/spark-submit \
    --packages graphframes:graphframes:0.8.2-spark3.2-s_2.12,org.apache.iceberg:iceberg-spark-runtime-3.2_2.12:0.14.0 \
    /opt/noop.py && \
    cp /home/sparkuser/.ivy2/jars/* /opt/apache/spark3/jars/ && \
    rm -rf /home/sparkuser/.ivy2/jars/

USER root
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-hadoop-cloud_2.12/3.2.0/spark-hadoop-cloud_2.12-3.2.0.jar /opt/apache/spark3/jars/
RUN chown -R root:root /opt/apache/spark3/jars/ && chmod a+r -R /opt/apache/spark3/jars/
RUN /opt/apache/spark3-python/bin/pip install spark-dataloader==0.1.3
USER sparkuser

WORKDIR /opt/apache/spark3/work-dir

ENTRYPOINT [ "/opt/entrypoint.sh" ]
