{{- define "require" -}}
    {{- $metastore_url := .Values.spark.hive_metastore_uri | required "spark.hive_metastore_uri is required" -}}
{{- end -}}
