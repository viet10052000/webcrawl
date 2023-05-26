git clone https://github.com/viet10052000/webcrawl

tạo môi trường ảo venv:
python3 -m venv venv

kích khoạt môi trường ảo venv:
source venv/bin/activate

tải các gói trong requiment.txt:
pip3 install -r requirements.txt

thay đổi mongodb : 
trong .env đổi đường dẫn 
MONGODB_URI=mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net
DATABASE_NAME=shops

link truy cập web đã chạy ngầm: http://127.0.0.1:9999/

chạy chương trình trực tiếp
flask run --port=8999
nếu muốn debug
flask run --debug --port=8999

tài khoản admin:
email:admin1@gmail.com
password: 123
tài khoản user:
email:viet123@gmail.com
password:123

nếu muốn chạy ngầm thì phải cài supervisor : trong server hiện tại đã cài rồi nên không phải cài đặt nữa còn nếu chưa có thì 
- pip3 install supervisor

Hướng dẫn sử dụng supervisor trên server
- Quản lý các tiến trình chạy trên Linux. 
- Đảm bảo một tiến trình nào đó luôn luôn chạy không ngừng nghỉ.
- Các bước config :
	+ b1. Config file 
	Với user nào sẽ có quyền với file đó. Ví dụ : crawl01 sẽ đọc, sửa với file crawl01.ini
		nano /etc/supervisord.d/crawl03.ini
	[program:webcrawl]
	directory=/home/crawl03/webcrawl
	command=/home/crawl03/webcrawl/venv/bin/flask run --host=0.0.0.0 --port=9999
	user=crawl03
	autostart=true
	autorestart=true
	stopasgroup=true
	killasgroup=true

        **directory trỏ tới đường dẫn tuyệt đối thư mục muốn chạy ngầm
        **command đường dẫn tuyệt đối để chạy chương trình

	+ b2. Đọc lại các file config
		sudo  supervisorctl reread
	+ b3.  Add , remove, restart lại những process nào thay đổi
		sudo  supervisorctl update
	+ b4. Xem status các process
		sudo  supervisorctl status





