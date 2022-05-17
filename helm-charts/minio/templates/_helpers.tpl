{{/*
Expand the name of the chart.
*/}}
{{- define "minio.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "minio.fullname" -}}
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
{{- define "minio.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "minio.labels" -}}
helm.sh/chart: {{ include "minio.chart" . }}
{{ include "minio.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "minio.selectorLabels" -}}
app.kubernetes.io/name: {{ include "minio.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "minio.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "minio.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/* 
SSL key
*/}}
{{- define "server.key" -}}
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDMsSZ28Mj4sSrp
q+2Nq2qbqeYeGtbZwxkUkhL6HJWkCeohI5zMjLRc+QxLkAoQpI5ret+x1KkEyPxU
GCLZTa4Vc4STxMlLisPdT1kSfnlG9AnuipdDOalM5yjYNha5vV2la2df7ExKqNIT
PdS7lQC/yyQk9WQT3BgF2PDXq/DQSqtZBepGNyp5Iseh6ZVEu/4qPLQikb/+nkId
xP7c/wyMeTy139qizfBUvn837mkC9Ze1bp+7UpjkHikS2IEgSIhK2mSvZQpMjATz
HFEUveKgk0WlOOohtIkQg2i2ULDsHs8AxS2kvoWKOuVMl1UZ31TZkGK0jYt9BwEc
k/gr0CCdAgMBAAECggEAX0n0uxgaptNrQ7665uGuzmqIaulZraRKT6400WRvMR9A
dE7s1riF2mZCGAck+FxyxIw+CL4UNNsPxGI8Duc/rFLLnDLW9qjRx3wB3j8sXCCN
YxP3mN8F9nwCIq0DZVJHfxOB20DYv0TaDwUQvIaAA8kguWfXP/uM32P/spcjkwLq
ZUe96NpQmUagJWRQGZ1X4/yDpIIXSEL0inyIv1b1fDD/YVrA1+N+xW/ZQq14zu38
NAmkxbnMnQoep/1/NlDPB9frV04ucPgZtzG89c19KnDPZTbr9udGaJltobnq/XZQ
CtXATMYBkYfcVudwc/GPzvCwQ+r64zl7JuTMdkYqzQKBgQDv9BycK2fbJ/97ZKaa
ZDFkEagFKS+QffGoR52BP6Lwwq/n7XKgxtstyncAZ9Hvos4HNqt0qm0rzeUDhBGc
zvhP32hzM3AzSqy+dKlkVn+POgaRRs/uc6yh7zJ8/5dgWnz9cxdf+CWmKfNCDzmN
u4JrWwvj/O0PLkniGTTP5wHLcwKBgQDaYWCqPa5HeY4nOgKvLKbzZfef3scsL2wo
8vwoY4GtJu42jBx8iWuXuuIIyiF2cZwHqdntFlQoqxB+ukQZpM/LMom4xIz4YH4Y
BbUerFmjfjIRFJNHzdsVhlyKUYp+2ap/vYJYcIpac0X8WGmKOG1gkxivpfhh8QIx
Qqgjkbh/rwKBgGFfm5iYWK3rvlZxktZGYHCuZZOqkf29ziou3bDMhS/UoZOpnQG3
kMw1RDNq7huj4p20xsEyQ9kp1YymtIsAxm2LSJSvRBHcdNtY9kCchWk27+FWbhzi
3iRcsA1fnytfrScg5FRym7yhe3DMQtvMQvGT4fBj/ENT0nGpLvBLW0QXAoGBAKsD
eumWZ/Z9EH9ThGqd8xfEkEhX8218rZzbu+/9DL4GMKHy0xQLoYAuz3fGorHYgjHW
J1ztEXbPj5lOUKosULV1nDhfY23WUqiJP68HlSLdXmPV0wh2As02bR28gVKZLlXe
mEadyxrODs5whiXBzpXEW56hwIMic28UHgvMv8jtAoGBAIa1M74g3WFMbjKmwu7C
Njt6Kg0XbsV1/+ROypmL3+Np9J//gIU4pkmahVqAwZa765qnKyjrhaWPCoT/RDcq
AM+g2IJWplBiKBKBeZQJfRcSX+1P9JK8YeV+xh1j/8WZx1dK/GFEPuVyGvxt+4Qr
VVpsPCxsj29Z21WESAiNLdlp
-----END PRIVATE KEY-----
{{ end }}

{{/* 
SSL key
*/}}
{{- define "server.crt" -}}
-----BEGIN CERTIFICATE-----
MIIEWTCCA0GgAwIBAgIUJdsaWDaU0t6k66Jnb6brTVGbIukwDQYJKoZIhvcNAQEL
BQAwgbsxCzAJBgNVBAYTAi0tMRIwEAYDVQQIDAlTb21lU3RhdGUxETAPBgNVBAcM
CFNvbWVDaXR5MRkwFwYDVQQKDBBTb21lT3JnYW5pemF0aW9uMR8wHQYDVQQLDBZT
b21lT3JnYW5pemF0aW9uYWxVbml0MR4wHAYDVQQDDBVsb2NhbGhvc3QubG9jYWxk
b21haW4xKTAnBgkqhkiG9w0BCQEWGnJvb3RAbG9jYWxob3N0LmxvY2FsZG9tYWlu
MB4XDTIxMDUzMTEzMDcxM1oXDTIyMDUzMTEzMDcxM1owgbsxCzAJBgNVBAYTAi0t
MRIwEAYDVQQIDAlTb21lU3RhdGUxETAPBgNVBAcMCFNvbWVDaXR5MRkwFwYDVQQK
DBBTb21lT3JnYW5pemF0aW9uMR8wHQYDVQQLDBZTb21lT3JnYW5pemF0aW9uYWxV
bml0MR4wHAYDVQQDDBVsb2NhbGhvc3QubG9jYWxkb21haW4xKTAnBgkqhkiG9w0B
CQEWGnJvb3RAbG9jYWxob3N0LmxvY2FsZG9tYWluMIIBIjANBgkqhkiG9w0BAQEF
AAOCAQ8AMIIBCgKCAQEAzLEmdvDI+LEq6avtjatqm6nmHhrW2cMZFJIS+hyVpAnq
ISOczIy0XPkMS5AKEKSOa3rfsdSpBMj8VBgi2U2uFXOEk8TJS4rD3U9ZEn55RvQJ
7oqXQzmpTOco2DYWub1dpWtnX+xMSqjSEz3Uu5UAv8skJPVkE9wYBdjw16vw0Eqr
WQXqRjcqeSLHoemVRLv+Kjy0IpG//p5CHcT+3P8MjHk8td/aos3wVL5/N+5pAvWX
tW6fu1KY5B4pEtiBIEiIStpkr2UKTIwE8xxRFL3ioJNFpTjqIbSJEINotlCw7B7P
AMUtpL6FijrlTJdVGd9U2ZBitI2LfQcBHJP4K9AgnQIDAQABo1MwUTAdBgNVHQ4E
FgQUla41RKZFObKVhbcvh+97VNFwNtgwHwYDVR0jBBgwFoAUla41RKZFObKVhbcv
h+97VNFwNtgwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEApb4V
ojS8xDbttWNRdcVlPtAmC1dpMdoBm1Cf6L1EjPX5oWHgkC1/s6D4YOCfxWd7emWv
A6Vfb3mZSUMwnnnHf13x9zNef0B+oj5ldA2tPgvCZUBW5YqLBXEqrP3/l3SdjKHY
GuuQoPcJ8hNKpsYwWUsX6zkOVhT+54g0cnPXfJDNe49DO7YzujagqHVwogsV0Sla
zWBoGGy9LqrObwukR1Mf3GcS2f4YV2olfh/qCi9+BtKaOmX1leEeO6j13XtOjPxI
xTNkltPf2k7IctD26L62a8RdFLDFZkwzI2qhcIplfD5xv/Yey7a9uIDkv/63Z7SL
iaxMmqkCjaZg7gCncQ==
-----END CERTIFICATE-----
{{ end }}
