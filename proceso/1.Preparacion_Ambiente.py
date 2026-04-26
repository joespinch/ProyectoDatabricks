# Databricks notebook source
# DBTITLE 1,Remove all widgets
dbutils.widgets.removeAll()

# COMMAND ----------

# DBTITLE 1,Create widgets
# MAGIC %sql
# MAGIC create widget text storageName default "adlsproyectoje";
# MAGIC create widget text catalogo default "catalog_au";

# COMMAND ----------

# DBTITLE 1,Get widget values
storageName = dbutils.widgets.get("storageName")

# COMMAND ----------

# DBTITLE 1,Create external location metastore
# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `extloc_uc_metastore`
# MAGIC URL 'abfss://metastore@${storageName}.dfs.core.windows.net/'
# MAGIC
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas raw del Data Lake';

# COMMAND ----------

# DBTITLE 1,Create external location raw
# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-raw`
# MAGIC URL 'abfss://raw@${storageName}.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas raw del Data Lake';

# COMMAND ----------

# DBTITLE 1,Create external location bronze
# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-bronze`
# MAGIC URL 'abfss://bronze@${storageName}.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas bronze del Data Lake';

# COMMAND ----------

# DBTITLE 1,Create external location silver
# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-silver`
# MAGIC URL 'abfss://silver@${storageName}.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas silver del Data Lake';

# COMMAND ----------

# DBTITLE 1,Create external location golden
# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-golden`
# MAGIC URL 'abfss://golden@${storageName}.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `credential`)
# MAGIC COMMENT 'Ubicación externa para las tablas golden del Data Lake';

# COMMAND ----------

# DBTITLE 1,Drop catalog
# MAGIC %sql
# MAGIC DROP CATALOG IF EXISTS catalog_au CASCADE;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS catalog_au 
# MAGIC MANAGED LOCATION 'abfss://metastore@${storageName}.dfs.core.windows.net/'
# MAGIC COMMENT 'Catalogo para la arquitectura medallion del ambiente de dev';
# MAGIC
# MAGIC

# COMMAND ----------

# DBTITLE 1,Create catalog
# MAGIC %md
# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS catalog_au
# MAGIC MANAGED LOCATION 'abfss://metastore@${storageName}.dfs.core.windows.net/unique_path/'
# MAGIC COMMENT 'Catalogo para la arquitectura medallion del ambiente de dev';

# COMMAND ----------

# DBTITLE 1,Drop schemas
# MAGIC %sql
# MAGIC DROP SCHEMA IF EXISTS catalog_au.bronze;
# MAGIC
# MAGIC DROP SCHEMA IF EXISTS catalog_au.raw;
# MAGIC
# MAGIC DROP SCHEMA IF EXISTS catalog_au.silver;
# MAGIC
# MAGIC DROP SCHEMA IF EXISTS catalog_au.golden;

# COMMAND ----------

# DBTITLE 1,Cleanup storage
dbutils.fs.rm(f"abfss://bronze@{storageName}.dfs.core.windows.net/",True)

dbutils.fs.rm(f"abfss://silver@{storageName}.dfs.core.windows.net/",True)

dbutils.fs.rm(f"abfss://golden@{storageName}.dfs.core.windows.net/",True)

# COMMAND ----------

# DBTITLE 1,Create schemas
# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS catalog_au.raw;
# MAGIC CREATE SCHEMA IF NOT EXISTS catalog_au.bronze;
# MAGIC CREATE SCHEMA IF NOT EXISTS catalog_au.silver;
# MAGIC CREATE SCHEMA IF NOT EXISTS catalog_au.golden;

# COMMAND ----------

# DBTITLE 1,Tablas Bronze
# MAGIC %md
# MAGIC ###Tablas Bronze

# COMMAND ----------

# DBTITLE 1,Create bronze circuits
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

# DBTITLE 1,Create bronze races
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

# DBTITLE 1,Create bronze constructors
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

# DBTITLE 1,Tablas Silver
# MAGIC %md
# MAGIC ###Tablas Silver

# COMMAND ----------

# DBTITLE 1,Create silver circuits_transformed
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

# DBTITLE 1,Tablas Golden
# MAGIC %md
# MAGIC ###Tablas Golden

# COMMAND ----------

# DBTITLE 1,Create golden table
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

# COMMAND ----------

# DBTITLE 1,Holas
# MAGIC %md
# MAGIC Holas

# COMMAND ----------

# DBTITLE 1,Mensaje de finalización
# MAGIC %sql
# MAGIC -- Mensaje de finalización
# MAGIC SELECT 'Proceso finalizado correctamente' AS message;

# COMMAND ----------

# DBTITLE 1,POKEMON
# MAGIC %md
# MAGIC POKEMON

# COMMAND ----------

# DBTITLE 1,Descripción ABILITIES
# MAGIC %md
# MAGIC #### Tabla ABILITIES
# MAGIC Catálogo de habilidades que pueden tener los Pokémon, identificadas por un ID único y su nombre.

# COMMAND ----------

# DBTITLE 1,Crear tabla ABILITIES
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE `${catalogo}`.bronze.ABILITIES (
# MAGIC     habilidad_id INT,
# MAGIC     nombre_habilidad STRING
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/ABILITIES";

# COMMAND ----------

# DBTITLE 1,Descripción EXPERIENCE_TYPES
# MAGIC %md
# MAGIC #### Tabla EXPERIENCE_TYPES
# MAGIC Tipos de experiencia que determinan cómo los Pokémon ganan puntos de experiencia al subir de nivel.

# COMMAND ----------

# DBTITLE 1,Crear tabla EXPERIENCE_TYPES
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE `${catalogo}`.bronze.EXPERIENCE_TYPES (
# MAGIC     tipo_experiencia_id INT,
# MAGIC     nombre_tipo_experiencia STRING
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/EXPERIENCE_TYPES";

# COMMAND ----------

# DBTITLE 1,Descripción GENERATIONS
# MAGIC %md
# MAGIC #### Tabla GENERATIONS
# MAGIC Información sobre las generaciones de Pokémon, incluyendo número de generación y descripción.

# COMMAND ----------

# DBTITLE 1,Crear tabla GENERATIONS
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE `${catalogo}`.bronze.GENERATIONS (
# MAGIC     generacion_id INT,
# MAGIC     numero_generacion INT,
# MAGIC     descripcion STRING
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/GENERATIONS";

# COMMAND ----------

# DBTITLE 1,Descripción POKEMON
# MAGIC %md
# MAGIC #### Tabla POKEMON
# MAGIC Tabla principal con los datos de cada Pokémon: estadísticas base, dimensiones físicas, tipo, generación y características especiales (legendario, mega evolución, formas regionales).

# COMMAND ----------

# DBTITLE 1,Crear tabla POKEMON
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE `${catalogo}`.bronze.POKEMON (
# MAGIC     pokemon_id INT,
# MAGIC     numero_pokedex INT,
# MAGIC     nombre STRING,
# MAGIC     tipo1_id INT,
# MAGIC     tipo2_id INT,
# MAGIC     generacion_id INT,
# MAGIC     tipo_experiencia_id INT,
# MAGIC     experiencia_nivel_100 INT,
# MAGIC     evolucion_final INT,
# MAGIC     tasa_captura INT,
# MAGIC     legendario INT,
# MAGIC     mega_evolucion INT,
# MAGIC     forma_alola INT,
# MAGIC     forma_galar INT,
# MAGIC     ps INT,
# MAGIC     ataque INT,
# MAGIC     defensa INT,
# MAGIC     ataque_especial INT,
# MAGIC     defensa_especial INT,
# MAGIC     velocidad INT,
# MAGIC     total_base INT,
# MAGIC     media DOUBLE,
# MAGIC     desviacion_estandar DOUBLE,
# MAGIC     altura_m DOUBLE,
# MAGIC     peso_kg DOUBLE,
# MAGIC     imc DOUBLE
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/POKEMON";

# COMMAND ----------

# DBTITLE 1,Descripción POKEMON_ABILITIES
# MAGIC %md
# MAGIC #### Tabla POKEMON_ABILITIES
# MAGIC Relación muchos a muchos entre Pokémon y sus habilidades.

# COMMAND ----------

# DBTITLE 1,Crear tabla POKEMON_ABILITIES
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE `${catalogo}`.bronze.POKEMON_ABILITIES (
# MAGIC     pokemon_id INT,
# MAGIC     habilidad_id INT
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/POKEMON_ABILITIES";

# COMMAND ----------

# DBTITLE 1,Descripción POKEMON_TYPE_EFFECTIVENESS
# MAGIC %md
# MAGIC #### Tabla POKEMON_TYPE_EFFECTIVENESS
# MAGIC Efectividad de cada tipo atacante contra cada Pokémon, expresada como multiplicador de daño.

# COMMAND ----------

# DBTITLE 1,Crear tabla POKEMON_TYPE_EFFECTIVENESS
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE `${catalogo}`.bronze.POKEMON_TYPE_EFFECTIVENESS (
# MAGIC     pokemon_id INT,
# MAGIC     tipo_atacante_id INT,
# MAGIC     multiplicador DOUBLE
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/POKEMON_TYPE_EFFECTIVENESS";

# COMMAND ----------

# DBTITLE 1,Descripción TYPES
# MAGIC %md
# MAGIC #### Tabla TYPES
# MAGIC Catálogo de tipos de Pokémon (fuego, agua, planta, etc.).

# COMMAND ----------

# DBTITLE 1,Crear tabla TYPES
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE `${catalogo}`.bronze.TYPES (
# MAGIC     tipo_id INT,
# MAGIC     nombre_tipo STRING
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/TYPES";