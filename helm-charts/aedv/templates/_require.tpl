{{- define "require" -}}
    {{- if .Values.ingress.enabled -}}
        {{- with .Values.ingress -}}
            {{- $host := .host | required "ingress.host is required" -}}
        {{- end -}}
    {{- end -}}
    {{- with .Values.superset -}}
        {{- $secret_key := .secret_key | required "superset.secret_key is required" -}}
        {{- $db_uri := .db_uri | required "superset.db_uri is required" -}}
    {{- end -}}
    {{- if .Values.smtp.enabled -}}
        {{- with .Values.smtp -}}
            {{- $smtp_host := .host | required "smtp.host is required" -}}
            {{- $smtp_from := .from | required "smtp.from is required" -}}
        {{- end -}}
    {{- end -}}
{{- end -}}
