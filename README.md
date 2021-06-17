Hướng dãn cài đặt hệ thống gợi ý phim cho người dùng.
Hệ thống yêu cầu có python từ 3.7 trở lên

Trong giao diện command-line
cài đặt môi trường : py -m venv venv

kích hoạt môi trường bằng lệnh : pip install -r requirements.txt

py manage.py makemigrations 
py manage.py migrate

cd movie_recommendation
tải CSDL có sẵn dữ liệu đánh giá được import vào tại đây: https://drive.google.com/drive/folders/1xKvG6s6lt3R3WqT4pInTmucBhqAMPekI?usp=sharing
tải mô hình đã được học bao gồm 2 file NeuMF.h5 và glob_mean.csv tại đây: https://drive.google.com/drive/folders/1xKvG6s6lt3R3WqT4pInTmucBhqAMPekI?usp=sharing

mkdir model_recsys
copy 2 file  NeuMF.h5 và glob_mean.csv vào folder model_recsys

khởi chạy hệ thống. py manage runserver

