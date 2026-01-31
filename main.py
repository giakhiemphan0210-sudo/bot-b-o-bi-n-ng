import requests
import time

# Cấu hình mốc chênh lệch (Ví dụ: 200.000 VNĐ hoặc 200 USD)
THRESHOLD = 200 
LAST_PRICE_FILE = "last_gold_price.txt"

def get_current_gold_price():
    # Giả lập lấy giá vàng từ API (hoặc scraping từ web giá vàng VN)
    # Để chính xác "200 giá" theo thị trường VN, bạn nên dùng API giá vàng SJC
    url = "https://api.metalpriceapi.com/v1/latest?api_key=YOUR_API_KEY&base=USD&currencies=XAU"
    data = requests.get(url).json()
    price = data['rates']['XAU'] # Giá tính theo đơn vị bạn chọn
    return price

def get_last_price():
    try:
        with open(LAST_PRICE_FILE, "r") as f:
            return float(f.read())
    except FileNotFoundError:
        return 0

def save_current_price(price):
    with open(LAST_PRICE_FILE, "w") as f:
        f.write(str(price))

def check_and_alert():
    current_price = get_current_gold_price()
    last_price = get_last_price()
    
    diff = abs(current_price - last_price)
    
    if diff >= THRESHOLD:
        direction = "📈 TĂNG" if current_price > last_price else "📉 GIẢM"
        msg = f"⚠️ **CẢNH BÁO BIẾN ĐỘNG VÀNG**\n"
        msg += f"Giá vừa {direction} {diff:.2f} giá!\n"
        msg += f"Giá hiện tại: {current_price:.2f}"
        
        send_to_telegram(msg) # Hàm gửi Telegram đã viết ở bước trước
        save_current_price(current_price)
        print(f"Đã gửi cảnh báo. Mốc giá mới: {current_price}")
    else:
        print(f"Biến động chưa đủ {THRESHOLD}. Giá hiện tại: {current_price}")

# Vòng lặp kiểm tra mỗi 5 phút (300 giây)
while True:
    check_and_alert()
    time.sleep(300)
