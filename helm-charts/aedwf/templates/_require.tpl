{{- define "require" -}}
    {{- if .Values.ingress.enabled -}}
        {{- with .Values.ingress -}}
            {{- $host := .host | required "ingress.host is required" -}}
        {{- end -}}
    {{- end -}}
    {{- with .Values.airflow -}}
        {{- $fernet_key := .fernet_key | required "airflow.fernet_key is required (generate one using `python -c 'import cryptography.fernet;print(cryptography.fernet.Fernet.generate_key())'`)" -}}
        {{- $db_uri := .db_uri | required "airflow.db_uri is required" -}}
        {{- $dag_git_repo := .dag_git_repository | required "airflow.dag_git_repository is required" -}}
        {{- $dag_git_repo := .default_timezone | required "airflow.default_timezone is required" -}}
        {{- $secret_key := .secret_key | required "airflow.secret_key is required" -}}
    {{- end -}}
    {{- if .Values.smtp.enabled -}}
        {{- with .Values.smtp -}}
            {{- $smtp_host := .host | required "smtp.host is required" -}}
            {{- $smtp_from := .from | required "smtp.from is required" -}}
        {{- end -}}
    {{- end -}}
{{- end -}}
