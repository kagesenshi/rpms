{{- define "require" -}}
    {{- if .Values.ingress.enabled -}}
        {{- with .Values.ingress -}}
            {{- $host := .host | required "ingress.host is required" -}}
        {{- end -}}
    {{- end -}}
    {{- with .Values.git -}}
        {{- $gitweb_password := .gitweb_password | required "git.gitweb_password is required" -}}
    {{- end -}}
{{- end -}}
