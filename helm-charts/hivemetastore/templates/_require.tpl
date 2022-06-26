{{- define "require" -}}
    {{- $metastore_db_uri := .Values.hive.metastore_db_url | required "hive.metastore_db_url is required (remember to escape for xml)" -}}
    {{- $metastore_db_type := .Values.hive.metastore_db_type | required "hive.metastore_db_type is required" -}}
    {{- $metastore_db_driver := .Values.hive.metastore_db_driver | required "hive.metastore_db_driver is required" -}}
    {{- $metastore_warehouse_dir := .Values.hive.metastore_warehouse_dir | required "hive.metastore_warehouse_dir is required" -}}


    {{- $s3a_endpoint := .Values.s3a.endpoint | required "s3a.endpoint is required" -}}
    {{- $s3a_access_key := .Values.s3a.access_key | required "s3a.access_key is required" -}}
    {{- $s3a_secret_key := .Values.s3a.secret_key | required "s3a.secret_key is required" -}}
{{- end -}}
