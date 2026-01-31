import requests
import os

def send_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=Markdown"
    try:
        requests.get(url)
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")

def get_gold_price():
    api_key = os.getenv('GOLD_API_KEY')
    url = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=USD&currencies=XAU"
    try:
        response = requests.get(url)
        data = response.json()
        # Chống lỗi KeyError: 'rates' bằng cách kiểm tra trước
        if 'rates' in data:
            return data['rates']['XAU']
        else:
            print(f"Lỗi API Vàng: {data}")
            return None
    except:
        return None

def get_crypto_data():
    # Lấy giá BTC và ETH kèm biến động 24h
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
    try:
        return requests.get(url).json()
    except:
        return None

def main():
    gold = get_gold_price()
    crypto = get_crypto_data()
    
    report = "📊 **BÁO CÁO THỊ TRƯỜNG TỔNG HỢP**\n\n"
    
    # Xử lý Vàng
    if gold:
        report += f"✨ **Vàng Thế giới:** ${gold:,.2f}/oz\n"
    else:
        report += "❌ Lỗi: Không lấy được giá Vàng (Check API Key).\n"

    # Xử lý Crypto & Cảnh báo biến động mạnh
    if crypto:
        btc_p, btc_c = crypto['bitcoin']['usd'], crypto['bitcoin']['usd_24h_change']
        eth_p, eth_c = crypto['ethereum']['usd'], crypto['ethereum']['usd_24h_change']
        
        report += f"🔹 **BTC:** ${btc_p:,} ({btc_c:.2f}%)\n"
        report += f"🔹 **ETH:** ${eth_p:,} ({eth_c:.2f}%)\n"
        
        # Cảnh báo biến động > 5%
        if abs(btc_c) >= 5 or abs(eth_c) >= 5:
            report += "\n⚠️ **CẢNH BÁO:** Thị trường biến động mạnh (>5%)!"
    
    send_telegram(report)

if __name__ == "__main__":
    main()
