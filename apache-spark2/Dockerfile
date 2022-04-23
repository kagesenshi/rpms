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
    dnf install -y bash tini nss pam apache-spark2 && \
    mkdir -p /opt/apache/spark2/work-dir && \
    touch /opt/apache/spark2/RELEASE && \
    rm /bin/sh && \
    ln -sv /bin/bash /bin/sh && \
    echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su && \
    chgrp root /etc/passwd && chmod ug+rw /etc/passwd && \
    cp /opt/apache/spark2/kubernetes/dockerfiles/spark/entrypoint.sh /opt/ && \
    dnf clean all

ENV SPARK_HOME /opt/apache/spark2

WORKDIR /opt/apache/spark2/work-dir

ENTRYPOINT [ "/opt/entrypoint.sh" ]
