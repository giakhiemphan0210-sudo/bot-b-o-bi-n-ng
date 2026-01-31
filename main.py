import os
import requests

def get_current_gold_price():
    api_key = os.getenv('GOLD_API_KEY')
    url = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=USD&currencies=XAU"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Bước kiểm tra sống còn: Chỉ truy cập nếu dữ liệu thực sự tồn tại
        if 'rates' in data and 'XAU' in data['rates']:
            return data['rates']['XAU']
        else:
            # Ghi log chi tiết để Analyst phân tích tại sao API lỗi
            print(f"⚠️ API Error or invalid response structure: {data}")
            return None
            
    except Exception as e:
        print(f"❌ Network connection error: {e}")
        return None

def check_and_alert():
    price = get_current_gold_price()
    
    # Nếu giá là None (lỗi API), chúng ta dừng hệ thống tại đây để tránh crash
    if price is None:
        print("🛑 System halted: Could not retrieve market data.")
        return

    # Nếu có giá, tiếp tục logic gửi Telegram và so sánh "200 giá" của bạn
    print(f"✅ Market Data Retrieved: {price}")
    # (Thêm code gửi Telegram của bạn ở đây)

if __name__ == "__main__":
    check_and_alert()
