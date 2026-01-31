import requests
import os

def get_market_data():
    # 1. Lấy dữ liệu Crypto (BTC & ETH) từ CoinGecko
    crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
    
    # 2. Lấy giá Vàng từ MetalPriceAPI
    gold_api_key = os.getenv('GOLD_API_KEY')
    gold_url = f"https://api.metalpriceapi.com/v1/latest?api_key={gold_api_key}&base=USD&currencies=XAU"
    
    report = "🚀 **BÁO CÁO THỊ TRƯỜNG TỔNG HỢP**\n\n"
    has_big_move = False

    try:
        # Xử lý Crypto
        c_res = requests.get(crypto_url).json()
        for coin in ['bitcoin', 'ethereum']:
            name = coin.upper()
            price = c_res[coin]['usd']
            change = c_res[coin]['usd_24h_change']
            
            report += f"🔹 **{name}:** ${price:,} ({change:.2f}%)\n"
            
            # Cảnh báo biến động mạnh (>5%)
            if abs(change) >= 5:
                report += f"      ⚠️ CẢNH BÁO: {name} biến động mạnh!\n"
                has_big_move = True

        # Xử lý Vàng (Cơ chế bảo vệ tránh KeyError 'rates')
        g_res = requests.get(gold_url).json()
        if 'rates' in g_res:
            gold_price = g_res['rates']['XAU']
            report += f"\n✨ **VÀNG Thế giới:** ${gold_price:,.2f}/oz\n"
            
            # Đọc giá cũ để so sánh 200 giá
            if os.path.exists("last_gold.txt"):
                with open("last_gold.txt", "r") as f:
                    last_price = float(f.read())
                
                diff = abs(gold_price - last_price)
                if diff >= 200:
                    direction = "TĂNG" if gold_price > last_price else "GIẢM"
                    report += f"      ⚠️ BÁO ĐỘNG: Vàng {direction} {diff:.2f} giá!\n"
                    has_big_move = True
            
            # Lưu giá mới làm mốc
            with open("last_gold.txt", "w") as f:
                f.write(str(gold_price))
        else:
            report += f"\n❌ Lỗi Vàng: {g_res.get('error', {}).get('message', 'Nguồn dữ liệu lỗi')}\n"

    except Exception as e:
        report = f"❌ Hệ thống gặp lỗi kỹ thuật: {str(e)}"

    return report, has_big_move

def send_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=Markdown"
    requests.get(url)

# Thực thi
msg, urgent = get_market_data()
send_telegram(msg)
