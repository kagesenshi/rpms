{{- define "require" -}}
    {{- if .Values.ingress.enabled -}}
        {{- with .Values.ingress -}}
            {{- $host := .host | required "ingress.host is required" -}}
        {{- end -}}
    {{- end -}}

    {{- $metastore_url := .Values.spark.hive_metastore_uri | required "spark.hive_metastore_uri is required" -}}
    {{- $s3a_endpoint := .Values.s3a.endpoint | required "s3a.endpoint is required" -}}
    {{- $s3a_access_key := .Values.s3a.access_key | required "s3a.access_key is required" -}}
    {{- $s3a_secret_key := .Values.s3a.secret_key | required "s3a.secret_key is required" -}}
{{- end -}}
