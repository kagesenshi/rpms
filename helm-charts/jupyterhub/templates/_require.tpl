{{- define "require" -}}
    {{- if .Values.ingress.enabled -}}
        {{- with .Values.ingress -}}
            {{- $host := .host | required "ingress.host is required" -}}
        {{- end -}}
    {{- end -}}
    {{- $spark_secret_name := .Values.spark.secret_name | required "spark.secret_name is required" -}}
    {{- $airflow_secret_name := .Values.airflow.secret_name | required "airflow.secret_name is required" -}}

{{- end }}
