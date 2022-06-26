{{/*
Expand the name of the chart.
*/}}
{{- define "gitserver.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "gitserver.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "gitserver.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "gitserver.labels" -}}
helm.sh/chart: {{ include "gitserver.chart" . }}
{{ include "gitserver.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "gitserver.selectorLabels" -}}
app.kubernetes.io/name: {{ include "gitserver.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "gitserver.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "gitserver.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}


{{- define "gitserver.volumes" -}}
- name: {{ include "gitserver.fullname" . }}-datadir
  persistentVolumeClaim:
    claimName: {{ include "gitserver.fullname" . }}-data
{{- end }}

{{- define "gitserver.volumeMounts" -}}
- name: {{ include "gitserver.fullname" . }}-datadir
  mountPath: /srv/git
{{- end }}

{{- define "gitserver.env" -}}
{{- if .Values.git.ssh_public_keys }}
- name: GIT_SSH_PUBKEYS
  valueFrom:
    secretKeyRef:
      name: {{ include "gitserver.fullname" . }}-secret
      key: ssh_public_keys
{{- end }}
- name: GITWEB_USER
  valueFrom:
    secretKeyRef:
      name: {{ include "gitserver.fullname" . }}-secret
      key: gitweb_user
- name: GITWEB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "gitserver.fullname" . }}-secret
      key: gitweb_password
{{- if .Values.ingress.tls }}
- name: INGRESS_HOST
  value: https://{{ .Values.ingress.host }}/repo
{{- else }}
- name: INGRESS_HOST
  value: http://{{ .Values.ingress.host }}/repo
{{- end }}
{{- end }}
