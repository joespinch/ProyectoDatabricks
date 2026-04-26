# Databricks notebook source
dbutils.widgets.removeAll()

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType
from pyspark.sql.functions import current_timestamp, to_timestamp, concat, col, lit

# COMMAND ----------

dbutils.widgets.text("container", "raw")
dbutils.widgets.text("catalogo", "catalog_au")
dbutils.widgets.text("esquema", "bronze")
dbutils.widgets.text("storageName", "adlssmartdata1702")

# COMMAND ----------

container = dbutils.widgets.get("container")
catalogo = dbutils.widgets.get("catalogo")
esquema = dbutils.widgets.get("esquema")
storageName = dbutils.widgets.get("storageName")

ruta = f"abfss://{container}@{storageName}.dfs.core.windows.net/constructors.json"

# COMMAND ----------

constructors_schema = StructType(fields=[
    StructField("constructorId", IntegerType(), False),
    StructField("constructorRef", StringType(), True),
    StructField("name", StringType(), True),
    StructField("nationality", StringType(), True),
    StructField("url", StringType(), True)
])

# COMMAND ----------

df_constructors = spark.read \
    .schema(constructors_schema) \
    .option("multiLine", True) \
    .json(ruta)

# COMMAND ----------

constructors_final_df = df_constructors.select(
    col("constructorId").alias("constructor_id"),
    col("constructorRef").alias("constructor_ref"),
    col("name"),
    col("nationality")
).withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

constructors_final_df.write \
    .mode("overwrite") \
    .insertInto(f"{catalogo}.{esquema}.constructors")