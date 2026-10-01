# Databricks notebook source
from pyspark.sql import functions as F

dbutils.widgets.text("source_table", "main.default.customers")
dbutils.widgets.text("target_table", "main.default.customer_metrics")

source_table = dbutils.widgets.get("source_table")
target_table = dbutils.widgets.get("target_table")

customer_metrics = (
    spark.table(source_table)
    .groupBy("country")
    .agg(F.countDistinct("customer_id").alias("customer_count"))
)

(
    customer_metrics.write.mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(target_table)
)
