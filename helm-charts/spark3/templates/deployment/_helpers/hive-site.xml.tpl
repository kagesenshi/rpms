{{- define "hive-site" }}
<configuration>
   <property>
       <name>hive.metastore.uris</name>
       <value>{{ .Values.spark.hive_metastore_uri | default "thrift://hive-metastore:9083" }}</value>
   </property>
   <property>
       <name>beeline.hs2.jdbc.url.default</name>
       <value>cluster</value>
    </property>
    <property>
    <name>beeline.hs2.jdbc.url.cluster</name>
       <value>jdbc:hive2://{{ include "spark3.fullname" . }}-hs2:10000</value>
    </property>
</configuration>
{{- end }}
