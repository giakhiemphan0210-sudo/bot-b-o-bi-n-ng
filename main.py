import os
import requests

def send_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=Markdown"
    requests.get(url)

def main():
    report = "📊 **BÁO CÁO THỊ TRƯỜNG**\n"
    
    # 1. Crypto (Dùng CoinGecko - Không cần Key)
    try:
        c_res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true").json()
        btc, eth = c_res['bitcoin']['usd'], c_res['ethereum']['usd']
        report += f"\n🪙 BTC: ${btc:,}\n🔹 ETH: ${eth:,}"
    except:
        report += "\n❌ Lỗi dữ liệu Crypto"

    # 2. Vàng (Kiểm tra lỗi API Key)
    key = os.getenv('GOLD_API_KEY')
    try:
        g_res = requests.get(f"https://api.metalpriceapi.com/v1/latest?api_key={key}&base=USD&currencies=XAU").json()
        if 'rates' in g_res:
            report += f"\n✨ Vàng: ${g_res['rates']['XAU']:,.2f}/oz"
        else:
            report += f"\n⚠️ Lỗi Vàng: {g_res.get('error', {}).get('message', 'Sai API Key')}"
    except:
        report += "\n❌ Lỗi kết nối API Vàng"

    send_telegram(report)

if __name__ == "__main__":
    main()
