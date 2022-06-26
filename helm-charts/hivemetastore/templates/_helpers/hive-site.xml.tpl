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
        <property>
                <name>hive.metastore.warehouse.dir</name>
                <value>{{ .Values.hive.metastore_warehouse_dir }}</value>
        </property>
        <property>
                <name>fs.s3a.endpoint</name>
                <value>{{ .Values.s3a.endpoint }}</value>
        </property>
        <property>
                <name>fs.s3a.access.key</name>
                <value>{{ .Values.s3a.access_key }}</value>
        </property>
        <property>
                <name>fs.s3a.secret.key</name>
                <value>{{ .Values.s3a.secret_key }}</value>
        </property>
        <property>
                <name>fs.s3a.path.style.access</name>
                <value>true</value>
        </property>
        <property>
                <name>fs.s3a.impl</name>
                <value>org.apache.hadoop.fs.s3a.S3AFileSystem</value>
        </property>
        <property>
                <name>fs.s3a.aws.credentials.provider</name>
                <value>org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider</value>
        </property>
</configuration>
{{- end }}
