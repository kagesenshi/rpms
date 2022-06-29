# install minio

REPO="abyres"
REPO_URL="https://releases.abyres.net/helm"

alias mc='mc --insecure'
function wait_for() {
    kubectl wait --for=condition=ready pod --timeout=300s -l app.kubernetes.io/name=$1
}

helm repo add ${REPO} ${REPO_URL}

set -e

helm install registry ${REPO}/registry \
    --set ingress.host=registry.k3s.lan \
    --set registry.user=user \
    --set registry.password=password

helm install minio ${REPO}/minio \
    --set ingress.host=minio.k3s.lan \
    --set ingress.console_host=minio-console.k3s.lan \
    --set minio.root_user=minio \
    --set minio.root_password=miniopassword \
    --set minio.instance_storage=1Gi

helm install citus ${REPO}/citus 

helm install gitserver ${REPO}/gitserver \
    --set ingress.host=git.k3s.lan \
    --set git.gitweb_password="password"

wait_for gitserver
wait_for citus
wait_for minio
wait_for registry

mc alias set minio https://minio.k3s.lan minio miniopassword
mc mb minio/spark/event_log
mc mb minio/spark/warehouse

kubectl exec -t citus -- createdb_with_user.sh \
    -d metastore -u metastore -p metastore

helm install hivemetastore ${REPO}/hivemetastore \
    --set hive.metastore_db_url=jdbc:postgresql://citus/metastore \
    --set hive.metastore_db_driver=org.postgresql.Driver \
    --set hive.metastore_db_user=metastore \
    --set hive.metastore_db_password=metastore \
    --set hive.metastore_db_type=postgres \
    --set hive.metastore_warehouse_dir=s3a://spark/tablespace/ \
    --set s3a.endpoint=http://minio:9000 \
    --set s3a.access_key=minio \
    --set s3a.secret_key=miniopassword

wait_for hivemetastore

helm install spark3 ${REPO}/spark3 \
    --set spark.hive_metastore_uri=thrift://hivemetastore:9083 \
    --set spark.deploy_thrift=true \
    --set ingress.thrift_host=sparksql.k3s.lan \
    --set s3a.endpoint=http://minio:9000 \
    --set s3a.access_key=minio \
    --set s3a.secret_key=miniopassword 

wait_for spark3

helm install jupyter ${REPO}/jupyterhub \
    --set ingress.host=jupyter.k3s.lan \
    --set spark.secret_name=spark3-config

kubectl exec -t citus -- createdb_with_user.sh \
    -d aedv -u aedv -p aedv

helm install aedv ${REPO}/aedv \
    --set ingress.host=superset.k3s.lan \
    --set superset.secret_key=helloworld \
    --set superset.db_uri=postgresql+psycopg2://aedv:aedv@citus/aedv

wait_for aedv

kubectl exec -t gitserver -- newrepo myproject

kubectl exec -t citus -- createdb_with_user.sh \
    -d aedwf -u aedwf -p aedwf

helm install aedwf ${REPO}/aedwf \
    --set ingress.host=airflow.k3s.lan \
    --set airflow.fernet_key="qwpdaZfaRLxXLZ5uWeScLJcF-eOuZtuP0h_6sDSz3yw=" \
    --set airflow.secret_key="helloworld" \
    --set airflow.default_timezone="Asia/Kuala_Lumpur" \
    --set airflow.dag_git_repository="http://gitserver/repo/myproject.git" \
    --set airflow.dag_git_username="git" \
    --set airflow.dag_git_password="password" \
    --set airflow.db_uri="postgresql+psycopg2://aedwf:aedwf@citus/aedwf" \
    --set spark.secret_name=spark3-config \
    --set airflow.secret_name=aedwf-config 

wait_for aedwf
