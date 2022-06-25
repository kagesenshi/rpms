{{- define "hive-site" }}
<configuration>
        <property>
                <name>javax.jdo.option.ConnectionURL</name>
                <value>{{ .Values.hive.metastore_db_url }}</value>
        </property>
        <property>
                <name>javax.jdo.option.ConnectionDriverName</name>
                <value>{{ .Values.hive.metastore_db_driver }}</value>
        </property>
        <property>
                <name>javax.jdo.option.ConnectionUserName</name>
                <value>{{ .Values.hive.metastore_db_user }}</value>
        </property>
        <property>
                <name>javax.jdo.option.ConnectionPassword</name>
                <value>{{ .Values.hive.metastore_db_password }}</value>
        </property>
</configuration>
{{- end }}
