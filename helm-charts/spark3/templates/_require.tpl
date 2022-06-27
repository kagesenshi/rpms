{{- define "require" -}}
    {{- $deploy_cluster := .Values.spark.deploy_cluster -}}
    {{- $deploy_thrift := .Values.spark.deploy_thrift -}}
    {{- if .Values.ingress.enabled -}}
        {{- with .Values.ingress -}}
            {{- if $deploy_cluster -}}
                {{- $host := .host | required "ingress.host is required" -}}
            {{- end -}}
            {{- if $deploy_thrift -}}
                {{- $host := .thrift_host | required "ingress.thrift_host is required" -}}
            {{- end -}}           
        {{- end -}}
    {{- end -}}

    {{- $metastore_url := .Values.spark.hive_metastore_uri | required "spark.hive_metastore_uri is required" -}}
    {{- $s3a_endpoint := .Values.s3a.endpoint | required "s3a.endpoint is required" -}}
    {{- $s3a_access_key := .Values.s3a.access_key | required "s3a.access_key is required" -}}
    {{- $s3a_secret_key := .Values.s3a.secret_key | required "s3a.secret_key is required" -}}
{{- end -}}
