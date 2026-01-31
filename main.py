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

def get_market_report():
    # 1. Lấy giá Crypto (CoinGecko - Không cần Key)
    crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
    report = "📊 **BÁO CÁO THỊ TRƯỜNG TỔNG HỢP**\n\n"
    
    try:
        c_res = requests.get(crypto_url).json()
        btc_p, btc_c = c_res['bitcoin']['usd'], c_res['bitcoin']['usd_24h_change']
        eth_p, eth_c = c_res['ethereum']['usd'], c_res['ethereum']['usd_24h_change']
        report += f"🔹 **BTC:** ${btc_p:,} ({btc_c:.2f}%)\n"
        report += f"🔹 **ETH:** ${eth_p:,} ({eth_c:.2f}%)\n"
        if abs(btc_c) >= 5 or abs(eth_c) >= 5:
            report += "⚠️ **CẢNH BÁO:** Crypto biến động mạnh!\n"
    except Exception as e:
        report += "❌ Lỗi Crypto: Không thể lấy dữ liệu.\n"

    # 2. Lấy giá Vàng (MetalPrice - Cần Key)
    api_key = os.getenv('GOLD_API_KEY')
    gold_url = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=USD&currencies=XAU"
    
    try:
        g_res = requests.get(gold_url).json()
        # BỐC TÁCH LỖI: Nếu không có 'rates', in toàn bộ lỗi ra Logs để kiểm tra
        if 'rates' in g_res:
            gold_price = g_res['rates']['XAU']
            report += f"\n✨ **Vàng Thế giới:** ${gold_price:,.2f}/oz"
        else:
            # Đây là dòng giúp bạn biết TẠI SAO API bị lỗi
            error_msg = g_res.get('error', {}).get('message', 'Sai API Key hoặc hết hạn mức')
            report += f"\n❌ **Lỗi Vàng:** {error_msg}"
            print(f"Full API Error Response: {g_res}") 
    except Exception as e:
        report += f"\n❌ Lỗi kết nối API Vàng: {e}"

    return report

if __name__ == "__main__":
    final_report = get_market_report()
    send_telegram(final_report)
