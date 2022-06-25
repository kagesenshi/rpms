{{- define "require" -}}
    {{- $metastore_db_uri := .Values.hive.metastore_db_url | required "hive.metastore_db_url is required (remember to escape for xml)" -}}
    {{- $metastore_db_type := .Values.hive.metastore_db_type | required "hive.metastore_db_type is required" -}}
    {{- $metastore_db_driver := .Values.hive.metastore_db_driver | required "hive.metastore_db_driver is required" -}}
{{- end -}}
