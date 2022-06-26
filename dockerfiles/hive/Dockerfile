FROM registry.gitlab.com/abyres/releases/centos8:8-1

RUN set -ex && \
    dnf copr enable izhar/data-engineering -y && \
    dnf install -y apache-hadoop apache-hive && \
    dnf clean all

RUN /usr/sbin/groupadd -r hiveuser --gid 1000 && \
     /usr/sbin/useradd -r -g hiveuser --uid 1000 \
     -s /sbin/nologin hiveuser

RUN set -ex && \
    dnf install mariadb-java-client.noarch postgresql-jdbc -y && \
    dnf clean all

ENV HIVE_CONF_DIR=/etc/hive
ENV HADOOP_HOME=/opt/apache/hadoop/
ENV JAVA_HOME=/usr/lib/jvm/jre-1.8.0/

RUN rm /opt/apache/hive/lib/guava-*.jar && \
    cp /opt/apache/hadoop/share/hadoop/hdfs/lib/guava-*.jar /opt/apache/hive/lib/ && \
    cp /usr/share/java/postgresql-jdbc.jar /opt/apache/hive/lib/ && \
    cp /usr/lib/java/mariadb-java-client.jar /opt/apache/hive/lib/ && \
    cp /opt/apache/hadoop/share/hadoop/tools/lib/*aws*.jar /opt/apache/hive/lib/ 

WORKDIR /opt/apache/hive/work-dir
ADD entrypoint.sh /opt/entrypoint.sh
RUN chmod a+x /opt/entrypoint.sh

ENTRYPOINT [ "/opt/entrypoint.sh" ]
