# Databricks notebook source
# MAGIC %md
# MAGIC ##Grants

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT SELECT ON TABLE catalog_au.bronze.circuits TO `jorgee@osom.biz`;

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT USE CATALOG ON CATALOG catalog_au TO `jorgee@osom.biz`;

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT USE SCHEMA ON SCHEMA catalog_au.bronze TO `jorgee@osom.biz`;
# MAGIC
# MAGIC GRANT USE SCHEMA ON SCHEMA catalog_au.bronze TO `DEs`;

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT CREATE TABLE ON SCHEMA catalog_au.bronze TO `jorgee@osom.biz`;