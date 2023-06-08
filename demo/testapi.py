import requests
headers = {
    'User-Agent': 'Mozilla/5.0',  # User-Agent mô phỏng trình duyệt web
    'Content-Type': 'application/json'  # Header Content-Type nếu cần thiết
}
i = 0
for page in range(20):
  # Gửi yêu cầu GET đến API
  response = requests.get('https://tiki.vn/api/v2/products?limit=100&include=advertisement&aggregations=2&trackity_id=b5d3ba57-f3a6-fc01-a24e-355a8b7b86f4&q=%C4%91i%E1%BB%87n+tho%E1%BA%A1i+samsung&sort=price,desc&_v=filter_revamp&page='+ str(page),headers=headers)
  # Kiểm tra mã trạng thái HTTP
  if response.status_code == 200:
      # Lấy dữ liệu từ phản hồi
      data = response.json()
      ids = []
      for item in data["data"]:
        ids.append(item["id"])
        i+=1
      print(ids)
  else:
      # Xử lý lỗi nếu mã trạng thái không phải là 200
      print('Yêu cầu không thành công. Mã trạng thái:', response.status_code)
      continue
print(i)
