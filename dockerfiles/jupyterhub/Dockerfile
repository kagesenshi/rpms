FROM registry.gitlab.com/abyres/releases/spark3:3.2.0-4

USER root
RUN set -ex && \
    dnf install -y jupyterhub passwd git  && \
    dnf clean all

ADD entrypoint.sh /opt/entrypoint.sh
RUN chmod a+rx /opt/entrypoint.sh

RUN userdel sparkuser
RUN /usr/sbin/groupadd -r jupyter --gid 1000 && \
     /usr/sbin/useradd -r -g jupyter --uid 1000 \
     -m -d /home/jupyter \
     -s /bin/bash jupyter 

ADD https://dl.min.io/client/mc/release/linux-amd64/mc /usr/local/bin/mc

RUN mkdir /opt/jupyterhub/share/jupyter/kernels/pyspark/
ADD pyspark-kernel/* /opt/jupyterhub/share/jupyter/kernels/pyspark/
ADD python-kernel/* /opt/jupyterhub/share/jupyter/kernels/python3/
WORKDIR /var/lib/jupyterhub/
USER root
RUN chown -R jupyter:jupyter /var/lib/jupyterhub/ && \
    chmod a+x /usr/local/bin/mc && \
    /opt/jupyterhub/bin/jupyter labextension disable @jupyterlab/extensionmanager-extension

ENTRYPOINT ["/opt/entrypoint.sh"]
