# Databricks notebook source
dbutils.widgets.removeAll()

# COMMAND ----------

# MAGIC %sql
# MAGIC create widget text storageName default "adlssmartdata1702";

# COMMAND ----------

storageName = dbutils.widgets.get("storageName")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-metastore`
# MAGIC URL 'abfss://metastore@${storageName}.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas raw del Data Lake';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-raw`
# MAGIC URL 'abfss://raw@${storageName}.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas raw del Data Lake';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-bronze`
# MAGIC URL 'abfss://bronze@${storageName}.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas bronze del Data Lake';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-silver`
# MAGIC URL 'abfss://silver@${storageName}.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas silver del Data Lake';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-golden`
# MAGIC URL 'abfss://golden@${storageName}.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas golden del Data Lake';

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP CATALOG IF EXISTS catalog_au CASCADE;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS catalog_au
# MAGIC MANAGED LOCATION 'abfss://metastore@${storageName}.dfs.core.windows.net/'
# MAGIC COMMENT 'Catalogo para la arquitectura medallion del ambiente de dev';

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP SCHEMA IF EXISTS catalog_au.raw;
# MAGIC DROP SCHEMA IF EXISTS catalog_au.bronze;
# MAGIC DROP SCHEMA IF EXISTS catalog_au.silver;
# MAGIC DROP SCHEMA IF EXISTS catalog_au.golden;

# COMMAND ----------

dbutils.fs.rm(f"abfss://bronze@{storageName}.dfs.core.windows.net/",True)
dbutils.fs.rm(f"abfss://silver@{storageName}.dfs.core.windows.net/",True)
dbutils.fs.rm(f"abfss://golden@{storageName}.dfs.core.windows.net/",True)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS catalog_au.raw;
# MAGIC CREATE SCHEMA IF NOT EXISTS catalog_au.bronze;
# MAGIC CREATE SCHEMA IF NOT EXISTS catalog_au.silver;
# MAGIC CREATE SCHEMA IF NOT EXISTS catalog_au.golden;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Tablas Bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS catalog_au.bronze.circuits (
# MAGIC circuit_id integer,
# MAGIC circuit_ref string,
# MAGIC name string,
# MAGIC location string,
# MAGIC country string,
# MAGIC latitude double,
# MAGIC longitude double,
# MAGIC altitude integer,
# MAGIC ingestion_date timestamp
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/circuits"

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS catalog_au.bronze.races (
# MAGIC race_id integer,
# MAGIC race_year integer,
# MAGIC round integer,
# MAGIC circuit_id integer,
# MAGIC name string,
# MAGIC ingestion_date timestamp
# MAGIC )
# MAGIC USING DELTA
# MAGIC PARTITIONED BY (race_year)
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/races"

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS catalog_au.bronze.constructors (
# MAGIC   constructor_id integer,
# MAGIC   constructor_ref string,
# MAGIC   name string,
# MAGIC   nationality string,
# MAGIC   ingestion_date timestamp
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/constructors"

# COMMAND ----------

# MAGIC %md
# MAGIC ###Tablas Silver

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS catalog_au.silver.circuits_transformed (
# MAGIC   race_id integer,
# MAGIC   race_year integer,
# MAGIC   round integer,
# MAGIC   circuit_id integer,
# MAGIC   name_race string,
# MAGIC   ingestion_date timestamp,
# MAGIC   circuit_ref string,
# MAGIC   name string,
# MAGIC   location string,
# MAGIC   country string,
# MAGIC   latitude double,
# MAGIC   longitude double,
# MAGIC   altitude integer,
# MAGIC   altitude_category string,
# MAGIC   years_diferences integer,
# MAGIC   lat_diff integer,
# MAGIC   race_type string,
# MAGIC   near_equator string
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://silver@${storageName}.dfs.core.windows.net/circuits_transformed"

# COMMAND ----------

# MAGIC %md
# MAGIC ###Tablas Golden

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS catalog_au.golden.golden_raced_partitioned (
# MAGIC   race_year integer,
# MAGIC   conteo long,
# MAGIC   max_altitude integer,
# MAGIC   min_altitude integer,
# MAGIC   country string,
# MAGIC   race_type string,
# MAGIC   near_equator string
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://golden@${storageName}.dfs.core.windows.net/golden_raced_partitioned"