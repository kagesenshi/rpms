FROM registry.gitlab.com/abyres/releases/aedwf:2.2.5-5

USER root
RUN set -ex && \
    dnf install -y jupyterhub passwd git && \
    dnf clean all

RUN userdel airflow
RUN /usr/sbin/groupadd -r jupyter --gid 1000 && \
     /usr/sbin/useradd -r -g jupyter --uid 1000 \
     -m -d /home/jupyter \
     -s /bin/bash jupyter 

ADD https://dl.min.io/client/mc/release/linux-amd64/mc /usr/local/bin/mc

RUN mkdir /opt/jupyterhub/share/jupyter/kernels/pyspark/ && \
    mkdir /workdir/ && \
    /usr/bin/python3 -m venv /opt/venv/ && \
    /opt/venv/bin/pip install ipykernel && \
    /opt/apache/spark3-python/bin/pip install matplotlib \
       pandas-profiling[notebook,html] pydot \
       bokeh altair vega-datasets 

ADD pyspark-kernel/* /opt/jupyterhub/share/jupyter/kernels/pyspark/
ADD python-kernel/* /opt/jupyterhub/share/jupyter/kernels/python3/
ADD page_config.json /opt/jupyterhub/etc/jupyter/labconfig/page_config.json

WORKDIR /workdir/

RUN chown -R jupyter:jupyter /var/lib/jupyterhub/ && \
    chown -R jupyter:jupyter /opt/venv/ && \
    chown -R jupyter:jupyter /workdir/ && \
    chmod a+x /usr/local/bin/mc && \
    chown jupyter:jupyter /var/log/apache-airflow

ENV WORKDIR=/workdir/ \
    AIRFLOW_HOME=/etc/apache-airflow \
    PATH="/opt/venv/bin:/:${PATH}:/opt/apache-airflow/bin/"

ADD entrypoint.sh /opt/entrypoint.sh
RUN chmod a+rx /opt/entrypoint.sh

ENTRYPOINT ["/opt/entrypoint.sh"]
