{{- define "require" -}}
    {{- if .Values.ingress.enabled -}}
        {{- with .Values.ingress -}}
            {{- $host := .host | required "ingress.host is required" -}}
        {{- end -}}
    {{- end -}}
    {{- with .Values.git -}}
        {{- $pubkeys := .ssh_public_keys | required "git.ssh_public_keys is required (separated by ';')" -}}
        {{- $gitweb_password := .gitweb_password | required "git.gitweb_password is required" -}}

    {{- end -}}
{{- end -}}
