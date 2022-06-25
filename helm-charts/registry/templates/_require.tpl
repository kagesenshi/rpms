{{- define "require" -}}
    {{- if .Values.ingress.enabled -}}
        {{- with .Values.ingress -}}
            {{- $host := .host | required "ingress.host is required" -}}
        {{- end -}}
    {{- end -}}
    {{- with .Values.registry -}}
        {{- $user := .user | required "registry.user is required" -}}
        {{- $password := .password | required "registry.password is required" -}}

    {{- end -}}
{{- end -}}
