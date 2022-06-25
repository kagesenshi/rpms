{{- define "require" -}}
    {{- if .Values.ingress.enabled -}}
        {{- with .Values.ingress -}}
            {{- $host := .host | required "ingress.host is required" -}}
            {{- $console_host := .console_host | required "ingress.console_host is required" -}}
        {{- end -}}
    {{- end -}}
    {{- with .Values.minio -}}
        {{- $root_user := .root_user | required "minio.root_user is required" -}}
        {{- $instance_storage := .instance_storage | required "minio.instance_storage is required" -}}
    {{- end -}}
{{- end -}}
