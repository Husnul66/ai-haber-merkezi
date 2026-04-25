import streamlit as st
import os
from crewai import Agent, Task, Crew, LLM

# Web sayfasının başlık ve ayarları
st.set_page_config(page_title="AI Haber Merkezi", page_icon="📰", layout="centered")

st.title("🤖 Otonom AI Haber Merkezi")
st.markdown("Bu sistem, **Gemini 1.5 Pro** kullanarak bugünün en güncel yapay zeka haberlerini bulur ve profesyonel bir bültene çevirir.")

# Güvenlik: API Anahtarını arayüzden (kullanıcıdan) alıyoruz
api_key = st.text_input("Gemini API Anahtarınızı Girin:", type="password")

# Butona basıldığında çalışacak sistem
if st.button("Haberleri Topla ve Bülteni Hazırla 🚀"):
    if not api_key:
        st.warning("Lütfen işleme başlamadan önce bir API anahtarı girin.")
    else:
        # Ajanların kullanacağı beyni arayüzden gelen anahtarla kuruyoruz
        gemini_llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=api_key,
            temperature=0.7
        )

        # 1. AJAN
        arastirmaci = Agent(
            role='Teknoloji Analisti',
            goal='Bugünün en önemli 3 yapay zeka haberini bulmak',
            backstory='Sen teknik dökümanları tarayıp en önemli noktaları çıkaran bir uzmansın.',
            llm=gemini_llm,
            verbose=True
        )

        # 2. AJAN
        editor = Agent(
            role='Teknoloji Editörü',
            goal='Haberleri profesyonel bir bültene dönüştürmek',
            backstory='Sen teknik bilgileri şık bir dile çeviren bir editörsün.',
            llm=gemini_llm,
            verbose=True
        )

        # GÖREVLER
        gorev1 = Task(
            description='Bugünün en önemli 3 yapay zeka haberini teknik detaylarıyla belirle.',
            expected_output='3 haber başlığı ve kısa teknik detayları içeren liste.',
            agent=arastirmaci
        )

        gorev2 = Task(
            description='Gelen haber listesini kullanarak profesyonel, emojili bir Türkçe bülten oluştur.',
            expected_output='Şık bir teknoloji bülteni.',
            agent=editor,
            context=[gorev1]
        )

        # EKİP
        haber_ekibi = Crew(agents=[arastirmaci, editor], tasks=[gorev1, gorev2])

        # Yükleme animasyonu ve çalıştırma
        with st.spinner("Ajanlar interneti tarıyor ve bülteni yazıyor (Bu işlem 1-2 dakika sürebilir)..."):
            try:
                sonuc = haber_ekibi.kickoff()
                st.success("✅ Bülten Başarıyla Oluşturuldu!")
                
                # Sonucu şık bir kutu içinde ekrana bas
                st.markdown("---")
                st.markdown(sonuc)
                st.markdown("---")
            except Exception as e:
                st.error(f"Sistemde bir hata oluştu: {e}")