data = [{'a':1},{'a':2}]
df = spark.createDataFrame(data)
df.write.saveAsTable('mydata')
df.write.format('csv').mode('overwrite').save('s3a://spark-history/data')

