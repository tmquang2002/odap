from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, regexp_replace, expr
from pyspark.sql.types import StructType, StringType, FloatType
import os
import requests
from bs4 import BeautifulSoup
import csv
import copy

def get_exchange_rate():
    url = 'https://wise.com/vn/currency-converter/usd-to-vnd-rate'

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Tìm thẻ <span> có class là 'text-success'
        exchange_rate_element = soup.find('span', {'class': 'text-success'})

        if exchange_rate_element:
            exchange_rate = float(exchange_rate_element.text.strip().replace(',', ''))  # Chuyển đổi sang kiểu số
            return exchange_rate
        else:
            print("Không tìm thấy thông tin tỷ giá.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def process_dataframe(df, batch_id):
 # Định nghĩa schema cho dữ liệu streaming
    schema = StructType().add("User", StringType())\
                         .add("Card", StringType())\
                         .add("Year", StringType())\
                         .add("Month", StringType())\
                         .add("Day", StringType())\
                         .add("Time", StringType())\
                         .add("Amount", StringType())\
                         .add("Use Chip", StringType())\
                         .add("Merchant Name", StringType())\
                         .add("Merchant City", StringType())\
                         .add("Merchant State", StringType())\
                         .add("Zip", StringType())\
                         .add("MCC", StringType())\
                         .add("Errors?", StringType())\
                         .add("Is Fraud?", StringType())
     # Chuyển đổi giá trị từ Kafka thành chuỗi
    value_str = df.selectExpr("CAST(value AS STRING)").alias("value")

    # Phân tích chuỗi JSON thành DataFrame
    parsed_df = value_str.select(from_json("value", schema).alias("data")).select("data.*")

    # Gọi hàm get_exchange_rate() để lấy tỷ giá
    exchange_rate = get_exchange_rate()

    if exchange_rate is not None:
        # Lọc các giao dịch thành công và không có giá trị null
        processed_df = parsed_df.filter("`Is Fraud?` = 'No' AND `Use Chip` != 'Online Transaction' AND `Errors?` = ''") \
        .withColumn("Amount", regexp_replace("Amount", "\\$", "").cast(FloatType())) \
        .filter(col("Amount").isNotNull() & (col("Amount") > 0))  # Lọc các giao dịch có Amount > 0

        # Chuyển đổi kiểu dữ liệu cột "Amount" và tính tổng thành tiền VNĐ
        processed_df = processed_df.withColumn("Amount_VND", (col("Amount") * exchange_rate).cast(FloatType()))
        csv_file_path = 'processed_data.csv'

        # Chọn các cột cần lưu trữ
        selected_columns = ["Card", "Year", "Month", "Day", "Time", "Merchant Name", "Merchant City", "Amount_VND"]
        clean_df_selected = processed_df.select(selected_columns)
        
        # Lưu dữ liệu
        result_array = clean_df_selected.collect()
        for row in result_array:
            print(row)
            with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                if file.tell() == 0:
                    csv_writer.writerow(selected_columns)
                csv_writer.writerow(row)

def main():
    # Thiết lập biến môi trường cho Spark Kafka dependencies
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 pyspark-shell'

    # Tạo một phiên Spark
    spark = SparkSession.builder.appName("CreditCardProcessing").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Đọc dữ liệu từ Kafka sử dụng structured streaming API
    kafka_stream_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "groupseven") \
        .load()

    query = kafka_stream_df.writeStream \
        .foreachBatch(process_dataframe)\
        .trigger(processingTime="6 seconds") \
        .start().awaitTermination()

if __name__ == "__main__":
    main()
