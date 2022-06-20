{{- define "beeline-site" -}}
<configuration>
 <property>
 <name>beeline.hs2.jdbc.url.default</name>
 <value>cluster</value>
 </property>
 <property>
 <name>beeline.hs2.jdbc.url.cluster</name>
 <value>jdbc:hive2://{{ include "spark3.fullname" . }}-thrift:10000</value>
 </property>
</configuration>
{{- end }}
