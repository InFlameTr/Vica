import google.generativeai as genai
import random
import os

# Google AI Studio API anahtarını buraya yaz
API_KEY = "AIzaSyDkh-Z3l8tb4UfQEpqar1Eo0TcG3lZqjaw"
genai.configure(api_key=API_KEY)

# Temalar ve örnek sözler
themes = ["azim", "başarı", "sabır", "öz disiplin", "kendine güven", "korku", "başarısızlıkla başa çıkma"]
styles = [
    "şiirsel", "özlü söz gibi", "bilge bir mentor gibi", "gizemli", "yazar gibi", "keskin ve kısa"
]
formats = [
    "1 cümlelik motivasyon", "vecize", "instagram gönderisi gibi", "minimal", "hikayevari"
]
example_quotes = [
    "Başarı, çekilen acıların gölgesinde büyür.",
    "Sana ve hayallerine inanacak birini bul.",
    "Bir gün sıradan bir sabah olmayan bir güne uyanacaksın.",
    "Bazen sadece senin gördüğün rüya için her şeyi riske atman gerekir.",
    "Zor sınavlar güçlü insanlar yetiştirir, hiçbir şeyi boşa yaşamadın.",
    "Hiçbir şeyi riske atmazsan her şeyi riske atmış olursun.",
    "Kural basit, kendinden başkasını hayatının merkezine koyma.",
    'Gün gelecek herkes "Biz inanmıyorduk ama o başardı" diyecek.',
    'Zaman her şeyi değiştirir.',
    'Yolumun farklı olması kaybolduğum anlamına gelmez.',
    'En güzel intikam başarıdır, seni sevmeyen herkesi üzer.',
    'Uçmak istiyorsan seni aşağı çeken her şeyi bırak.',
    'Sessizliği zayıflıkla karıştırmayın zeki insanlar yüksek sesle plan yapmaz.'
]

REQUOTES_FILE = "requotes.txt"
QUOTES_FILE = "quotes.txt"
MAX_QUOTES = 15

# Önceki sözlerle benzerliği kontrol eden yardımcı fonksiyon
def is_similar_to_previous(new_quote, previous_quotes):
    return any(new_quote.lower() in q.lower() or q.lower() in new_quote.lower() for q in previous_quotes)

def load_quotes():
    if not os.path.exists(QUOTES_FILE):
        return []
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def save_quotes(quotes):
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        f.writelines([q + "\n" for q in quotes])

def add_quote(new_quote):
    quotes = load_quotes()
    if is_similar_to_previous(new_quote, quotes):
        print("⚠️ Bu söz çok benzer. Yeni üretim deneniyor...")
        return False  # Benzerse yeni üretim tetiklenecek

    if len(quotes) >= MAX_QUOTES:
        quotes.pop(0)  # en eskiyi sil

    quotes.append(new_quote)
    save_quotes(quotes)
    print("✅ Yeni söz eklendi:", new_quote)
    return True

# Ana söz üretme fonksiyonu
def generate_quote():
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

        for attempt in range(5):  # En fazla 5 deneme
            theme = random.choice(themes)
            style = random.choice(styles)
            format_type = random.choice(formats)
            prompt = prompt = f"""
            '{theme}' temalı, {style} bir tarzda, {format_type} olacak şekilde ÖZGÜN, KISA ve NET bir motivasyon sözü üret.
            Lütfen sadece TEK CÜMLE olsun ve 20 kelimeden uzun olmasın.
            Klişe olmasın, yaratıcı olsun.
            """

            prompt += "\n".join([f"- {quote}" for quote in example_quotes])

            response = model.generate_content(prompt)
            quote = response.text.strip() if response.text else "Söz üretilemedi."

            if add_quote(quote):
                return quote  # Benzersiz ve eklendi
            else:
                continue  # Benzerse tekrar üret

        return get_random_quote_from_file()

    except Exception as e:
        if "429" in str(e):  # kotayı aşarsa
            return get_random_quote_from_file()
        return "Söz üretilemedi, lütfen tekrar deneyin."


def get_random_quote_from_file():
    # Dosyadan tüm satırları oku
    with open(REQUOTES_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if not lines:
        return "Söz kalmadı, lütfen dosyayı doldurun."
    
    # Rastgele bir satır seç
    chosen = random.choice(lines).strip()
    
    # Dosyaya yazarken seçilen satırı çıkar
    lines.remove(chosen + "\n")  # satır sonu ile eşleşme için
    
    # Güncellenmiş listeyi dosyaya geri yaz
    with open(REQUOTES_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    return chosen


# Örnek çalıştırma
if __name__ == "__main__":
    print("🔄 Yeni söz üretiliyor...")
    final_quote = generate_quote()
    print("📌 Üretilen söz:", final_quote)
