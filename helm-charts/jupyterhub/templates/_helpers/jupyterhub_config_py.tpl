# vim: set syntax=python:
{{- define "jupyterhub.config" -}}
import os, nativeauthenticator
import socket
from kubespawner.objects import make_owner_reference
import json

c.JupyterHub.db_url = "{{ .Values.jupyterhub.db_uri }}"
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.JupyterHub.template_paths = [os.path.join(
    os.path.dirname(nativeauthenticator.__file__), '/templates/')]
c.Authenticator.admin_users = {'admin'}
c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.JupyterHub.hub_ip = socket.gethostbyname(socket.gethostname())
c.KubeSpawner.cmd = ["jupyterhub-singleuser"]

c.KubeSpawner.pod_name_template = '{{ include "jupyterhub.name" . }}-nb-{username}'
c.KubeSpawner.extra_pod_config = {
    "setHostnameAsFQDN": True,
    "subdomain": '{{ include "jupyterhub.name" . }}',
}
c.KubeSpawner.extra_labels = {
    'app.kubernetes.io/name': '{{ include "jupyterhub.name" . }}',
    'app.kubernetes.io/instance': '{{ .Release.Name }}'
}
c.KubeSpawner.dns_name_template = '{name}.{{ include "jupyterhub.fullname" . }}.{namespace}.svc.cluster.local'
c.KubeSpawner.service_account = '{{ include "jupyterhub.serviceAccountName" . }}'
c.KubeSpawner.automount_service_account_token = True
c.KubeSpawner.image_spec = "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
c.KubeSpawner.image_pull_policy = "{{ .Values.image.pullPolicy }}"
{{- with .Values.imagePullSecrets }}
c.KubeSpawner.image_pull_secrets "{{- toYaml . -}}"
{{- end }}

c.KubeSpawner.storage_access_modes = ['{{ .Values.storageAccessMode | default "ReadWriteMany" }}']
c.KubeSpawner.storage_capacity = '{{ .Values.jupyterhub.nb_storage_capacity | default "1Gi" }}'
c.KubeSpawner.fs_gid = 1000
{{- if .Values.jupyterhub.nb_storage_class }}
c.KubeSpawner.storage_class = "{{ .Values.jupyterhub.nb_storage_class }}"
{{- end }}
c.KubeSpawner.pvc_name_template = 'pvc-{{ include "jupyterhub.fullname" . }}-{username}'
c.KubeSpawner.storage_pvc_ensure = True
c.KubeSpawner.volumes = [
  {
    'name': 'vol-{{ include "jupyterhub.fullname" . }}-{username}',
    'persistentVolumeClaim': {
      'claimName': 'pvc-{{ include "jupyterhub.fullname" . }}-{username}'
    }
  }, {
    'name': '{{ include "jupyterhub.fullname" . }}-spark-config',
    'secret': {
        'secretName': '{{ .Values.spark.secret_name }}',
    }
 }, {
    'name': '{{ include "jupyterhub.fullname" . }}-airflow-config',
    'secret': {
        'secretName': '{{ .Values.airflow.secret_name }}',
    }
 }
]
c.KubeSpawner.volume_mounts = [
    {
        'mountPath': '/home/',
        'name': 'vol-{{ include "jupyterhub.fullname" . }}-{username}'
    }, {
        'name':  '{{ include "jupyterhub.fullname" . }}-spark-config',
        'mountPath': "/etc/spark3/"
    }, {
        'name': '{{ include "jupyterhub.fullname" . }}-spark-config',
        'mountPath': "/opt/apache/spark3/conf/",
    }, {
        'name': '{{ include "jupyterhub.fullname" . }}-airflow-config',
        'mountPath': "/etc/apache-airflow/",
    }
]
c.KubeSpawner.start_timeout = 300


def modify_pod(spawner, pod):
    name = os.environ.get('K8S_POD_NAME')
    uid = os.environ.get('K8S_POD_UID')
    if not name or not uid:
       return pod
    ref = make_owner_reference(name, uid)
    pod.metadata.owner_references = [ref]
    return pod

c.KubeSpawner.modify_pod_hook = modify_pod

{{- if .Values.jupyterhub.profiles }}
profiles_json = """{{- toJson .Values.jupyterhub.profiles -}}"""
c.KubeSpawner.profile_list = json.loads(profiles_json)
{{- end }}
{{- end }}

