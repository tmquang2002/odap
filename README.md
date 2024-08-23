# Đồ án môn Xử lý và phân tích dữ liệu trực tuyến

## Giới thiệu

Đây là đồ án môn học với mục tiêu xây dựng hệ thống quản lý và xử lý dữ liệu giao dịch thẻ tín dụng theo thời gian thực, dựa trên các công nghệ như Kafka, Spark Streaming, Hadoop, Power BI, và Airflow.

## Mô tả bài toán

Một công ty tài chính muốn xây dựng hệ thống quản lý dữ liệu giao dịch thẻ tín dụng. Các giao dịch này được phát sinh từ các máy POS tại các cửa hàng, nhà hàng, và các địa điểm khác. Mỗi giao dịch này được gửi qua hệ thống kafka theo thời gian thực. Sinh viên dùng Kafka để mô phỏng từng giao dịch được phát sinh với các thông tin được cho trước dạng csv. 

Cấu trúc thông tin như sau: `User,Card,Year,Month,Day,Time,Amount,Use Chip,Merchant Name,Merchant City,Merchant State,Zip,MCC,Errors?,Is Fraud?`

Kafka sẽ đọc từng dòng csv và gửi qua topic được định nghĩa trước để giả lập một giao dịch được phát sinh từ máy POS.

## Chức năng

*Xử lý dữ liệu giao dịch theo thời gian thực.
*Kiểm tra lỗi và xác định các giao dịch gian lận (Fraud).
*Lưu trữ thông tin giao dịch thành công vào cơ sở dữ liệu.
*Thống kê số lượng và giá trị giao dịch theo ngày, tháng, năm và trực quan hóa dữ liệu.

## Kiến trúc

