#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

FROM centos:stream8

RUN set -ex && \
    dnf install dnf-plugins-core epel-release -y && \
    dnf copr enable izhar/data-engineering -y && \
    dnf install -y iputils glibc-langpack-en net-tools nmap bind-utils hostname && \
    dnf install -y bash tini nss pam && \
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
    cp /usr/lib/java/mariadb-java-client.jar /opt/apache/hive/lib/ 

WORKDIR /opt/apache/hive/work-dir
ADD entrypoint.sh /opt/entrypoint.sh
RUN chmod a+x /opt/entrypoint.sh

ENTRYPOINT [ "/opt/entrypoint.sh" ]
