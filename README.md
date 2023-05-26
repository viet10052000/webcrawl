ở local tải trình duyệt firefox

git clone https://github.com/viet10052000/webcrawl

tạo môi trường ảo venv:

trên window: 
python -m venv venv

trên linux , macOS:
python3 -m venv venv

kích khoạt môi trường ảo venv:

trên window: 
venv\Scripts\activate

trên linux , macOS:
source venv/bin/activate

tải các gói trong requiment.txt:
pip install -r requirements.txt

chạy chương trình 
flask run 
nếu muốn debug
flask run --debug

thoát hỏi môi trường ảo:
deactivate





