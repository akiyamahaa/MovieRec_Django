HƯỚNG DẪN CÀI ĐẶT HỆ THỐNG GỢI Ý CHO NGƯỜI DÙNG.
Hệ thống yêu cầu có python từ 3.7 trở lên


Trong giao diện command-line
Bước 1: tại thư mục movie_rec, cài đặt môi trường python bằng lệnh :
py -m venv venv

Bước 2 :kích hoạt môi trường bằng lệnh :
venv/Script/activate

Bước 3: cài đặt các thư viện cho project : 
pip install -r requirements.txt

Bước 4: truy cập vào thư mục chính project :
cd movie_recommendation

Bước 5: Tạo CSDL cho hệ thống bằng lệnh :
py manage.py makemigrations 

Bước 6: Lấy tất cả thay đổi trên model chưa được apply và chạy trên db, đồng bộ thay đổi đó cho  model trên database bằng lệnh sau:
py manage.py migrate


Bước 7: tải file db.sqlite3 - CSDL có sẵn dữ liệu đánh giá được import vào tại đây: https://drive.google.com/drive/folders/1xKvG6s6lt3R3WqT4pInTmucBhqAMPekI?usp=sharing
Ghi đè db.sqlite3 với db.sqlite3 ở thư mục movie_rec/movie_recommendation/

Bước 8 :tải mô hình đã được học bao gồm 2 file NeuMF.h5 và glob_mean.csv tại đây: https://drive.google.com/drive/folders/1xKvG6s6lt3R3WqT4pInTmucBhqAMPekI?usp=sharing
Di chuyển 2 file đó vào thư mục movie_rec/movie_recommendation/model_recsys

Bước 9 :khởi chạy hệ thống. Chạy câu lệnh:
py manage runserver
Hệ thống sẽ chạy ở cổng http://127.0.0.1:8000/
Hệ thống đã có sẵn TK quản trị viên là admin, TK người dùng đã được mô hình gợi ý là user1, user2. Mật khẩu mặc định là 1234
Để khởi tạo quản trị viên, ta sử dụng lệnh : py manage.py createsuperuser

------------------------------------------------------------------------------------------------------------------------------------------------

HƯỚNG DẪN HUẤN LUYỆN MÔ HÌNH MỚI: 
Bước 1: cần export tập dữ liệu đánh giá, bằng câchs truy cập đường dẫn http://127.0.0.1:8000/download-csv/
quá trình export dữ liệu từ CSDL cần mất 1 thời gian

Bước 2: sau khi export cơ sở dữ liệu xong, đem dữ liệu huấn luyện mô hình trên google colab ở file NeuMF.ipynb ở folder train_model đường dẫn 
https://drive.google.com/drive/folders/1xKvG6s6lt3R3WqT4pInTmucBhqAMPekI?usp=sharing

Bước 3: sau khi huấn luyện xong tải 2 file NeuMF.h5 và glob_mean.csv và đưa vào folder movie_rec/movie_recommendation/model_recsys.

Bước 4: hệ thống sau khi huấn luyện mô hình sẽ có gợi ý mới cho người dùng.

