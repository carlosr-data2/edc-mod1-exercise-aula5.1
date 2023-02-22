from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max

# Cria objeto da Spark Session
spark = (SparkSession.builder.appName("DeltaExercise")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)


# subiu cluster emr em 20 minutos
'''
Status :FAILED
Reason :S3 Service Error.
Log File :s3://datalake-ney-igti-edc-tf/emr-logs/j-2KO0J1V4VIJN0/steps/s-OIFQ37DVMT6N/stderr.gz
Details :Caused by: com.amazon.ws.emr.hadoop.fs.shaded.com.amazonaws.services.s3.model
.AmazonS3Exception: Access Denied (Service: Amazon S3; Status Code: 403;
 Error Code: AccessDenied; Request ID: 9T6TWMWBY6HEVH59; S3 Extended Request 
 ID: +YZ9mKrzkJ7HEag7O/ZxNWYhkYFAUr6gEZzQqe+eBkx7kFhyHvJpp0KLx78w04bGZJbSJ/tXyiLhC3j37QIvbQ==;
  Proxy: null), S3 Extended Request ID: +YZ9mKrzkJ7HEag7O/ZxNWYhkYFAUr6gEZzQqe+eBkx7kFhyHvJpp0KL
  x78w04bGZJbSJ/tXyiLhC3j37QIvbQ==

alterar os noomes dos buckets

'''



# Importa o modulo das tabelas delta
from delta.tables import *

# Leitura de dados
enem = (
    spark.read.format("csv")
    .option("inferSchema", True)
    .option("header", True)
    .option("delimiter", ";")
    .load("s3://datalake-ney-igti-edc/raw-data/enem")
)

# Escreve a tabela em staging em formato delta
print("Writing delta table...")
(
    enem
    .write
    .mode("overwrite")
    .format("delta")
    .partitionBy("year")
    .save("s3://datalake-ney-igti-edc-tf/staging-zone/enem")
)
