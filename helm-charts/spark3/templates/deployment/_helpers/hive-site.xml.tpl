{{- define "hive-site" }}
<configuration>
        <property>
                <name>hive.metastore.uris</name>
                <value>{{ .Values.spark.hive_metastore_uri | default "thrift://hive-metastore:9083" }}</value>
        </property>
</configuration>
{{- end }}
