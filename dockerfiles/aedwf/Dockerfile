FROM registry.gitlab.com/abyres/releases/spark3:3.2.0-11

USER root
RUN dnf copr enable izhar/aet -y  && \
    dnf install mariadb-connector-c apache-airflow -y && \
    dnf swap apache-airflow-logos aedwf-logos -y && \
    dnf clean all

ADD entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod a+x /usr/bin/entrypoint.sh

RUN userdel sparkuser
RUN /usr/sbin/groupadd -r airflow --gid 1000 && \
     /usr/sbin/useradd -r -g airflow --uid 1000 \
     -m -d /home/airflow/ \
     -s /bin/bash airflow 

ADD sudoers /etc/sudoers.d/

WORKDIR /var/lib/apache-airflow/
USER airflow

ENV PYTHONPATH=/etc/apache-airflow \
    ACCESS_LOG=/var/log/apache-airflow/access.log \
    ERROR_LOG=/var/log/apache-airflow/errors.log \
    PATH="/opt/apache-airflow/bin/:${PATH}" \
    PYTHONUNBUFFERED=1 \
    AIRFLOW_HOME=/etc/apache-airflow/ \
    LC_ALL=en_US.utf8 \
    LANG=en_US.utf8

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
