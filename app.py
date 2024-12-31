import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from PIL import Image
from utils.data_fetcher import DataFetcher
from utils.simulation import CryptoSimulation
import numpy as np

# ---------------------------
# Özel CSS Stillendirmesi
# ---------------------------
def local_css():
    st.markdown(
        """
        <style>
        /* Genel Arkaplan */
        .reportview-container {
            background-color: #f0f2f6;
        }
        /* Başlık Stili */
        .title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: #1F4E79;
            margin-top: 20px;
        }
        /* Alt Başlık Stili */
        .subtitle {
            font-size: 24px;
            color: #4B8BBE;
            text-align: center;
            margin-bottom: 40px;
        }
        /* Buton Stili */
        .stButton button {
            color: white;
            background-color: #1F4E79;
            padding: 10px 24px;
            border-radius: 8px;
            border: none;
            font-size: 16px;
        }
        /* DataFrame Stili */
        .dataframe {
            font-size: 14px;
        }
        /* Footer Stili */
        .footer {
            text-align: center;
            color: gray;
            margin-top: 50px;
        }
        /* Sidebar Başlık Stili */
        .sidebar .sidebar-content {
            background-color: #ffffff;
            color: #1F4E79;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

local_css()

# ---------------------------
# Logo
# ---------------------------
try:
    st.markdown(
        '<div style="text-align: center;">'
        '<img src="https://img.freepik.com/free-psd/3d-cryptocurrency-icon-bitcoin-illustration_629802-4.jpg" width="150">'
        '</div>',
        unsafe_allow_html=True
    )
except:
    st.warning("Logo yüklenemedi.")


st.markdown('<div class="title">🚀 Kripto Para Yatırım Simülasyonu</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">30 Günlük Yatırım Senaryosu ile Potansiyel Kazanç ve Zararınızı Keşfedin</div>', unsafe_allow_html=True)

# ---------------------------
# Kullanici Giris Alani
# ---------------------------
st.sidebar.header("📊 Simülasyon Ayarları")

# Kullanıcı Girdileri
crypto_options = [
    "bitcoin",
    "ethereum",
    "ripple",
    "litecoin",
    "cardano",
    "dogecoin",
    "polkadot",
    "solana",
    "chainlink",
    "binancecoin"
]
crypto_input = st.sidebar.selectbox(
    "Kripto Para Seçiniz:",
    options=crypto_options,
    index=0
)

initial_investment = st.sidebar.number_input(
    "Başlangıç Yatırım Tutarı (USD):",
    min_value=1.0,
    value=1000.0,
    step=50.0,
    format="%.2f"
)

start_date = st.sidebar.date_input(
    "Simülasyon Başlangıç Tarihi:",
    value=datetime.today() - timedelta(days=1),
    min_value=datetime(2010, 7, 17),
    max_value=datetime.today() - timedelta(days=1)
)

simulation_days = 30  # Sabit simülasyon dönemi

# ---------------------------
# Simülasyon Butonu ve İşlemler
# ---------------------------
if st.sidebar.button("Simülasyonu Başlat 🚀"):
    with st.spinner('Veriler alınıyor ve simülasyon gerçekleştiriliyor...'):
        # Tarihi formatla (CoinGecko API, DD-MM-YYYY formatını kullanır)
        date_str = start_date.strftime("%d-%m-%Y")

        # Geçmiş fiyatı al
        fetcher = DataFetcher()
        initial_price = fetcher.fetch_historical_price(crypto_input.lower(), date_str)

        if initial_price is not None:
            # Simülasyonu çalıştır
            simulation = CryptoSimulation(initial_price, start_date, simulation_days)
            df = simulation.df

            # Sonuçları hesapla
            final_investment, profit_loss = simulation.get_final_investment(initial_investment)

            # Renkli Kazanç/Zarar Mesajı
            if profit_loss > 0:
                pl_color = "#28a745"  # Yeşil
                pl_symbol = "📈"
            elif profit_loss < 0:
                pl_color = "#dc3545"  # Kırmızı
                pl_symbol = "📉"
            else:
                pl_color = "gray"
                pl_symbol = "➖"

            # Sonuçları göster
            st.markdown("<hr>", unsafe_allow_html=True)
            with st.container():
                col1, col2, col3 = st.columns(3)
                col1.metric("Başlangıç Yatırımı", f"${initial_investment:,.2f}")
                col2.metric("30 Gün Sonunda Yatırım", f"${final_investment:,.2f}")
                col3.markdown(f"**Toplam Kazanç/Zarar:** <span style='color:{pl_color};'>{pl_symbol} ${profit_loss:,.2f}</span>", unsafe_allow_html=True)

            # Tabloyu göster
            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader("🗓️ Günlük Fiyat Değişimleri")
            st.dataframe(
                df[['Date', 'Daily Change (%)', 'Price (USD)']].style.format({
                    'Daily Change (%)': "{:+.2f}%",
                    'Price (USD)': "${:,.2f}"
                }),
                height=300
            )

            # İnteraktif Grafik
            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader(f"📈 {crypto_input.capitalize()} Yatırım Grafiği")
            fig = px.line(
                df,
                x='Date',
                y='Price (USD)',
                markers=True,
                title=f"{crypto_input.capitalize()} Simülasyonu ({simulation_days} Gün)",
                labels={
                    'Date': 'Tarih',
                    'Price (USD)': 'Fiyat (USD)'
                },
                template='plotly_white'
            )
            fig.update_layout(
                xaxis_title="Tarih",
                yaxis_title="Fiyat (USD)",
                xaxis=dict(tickformat="%d-%m-%Y"),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Son Tartışma ve Ek Bilgiler
            st.markdown("<hr>", unsafe_allow_html=True)
            st.info(
                f"### Notlar 👇\n"
                f"- Simülasyon, **{simulation_days} gün** boyunca her gün rastgele **-5% ile +5%** arasında değişim uygulanarak gerçekleştirilmiştir.\n"
                f"- Başlangıç tarihi **{start_date.strftime('%d %B %Y')}** olarak seçilmiştir.\n"
                f"- Gerçek piyasa koşullarını yansıtmamaktadır ve sadece eğitsel amaçlıdır."
            )

            # İleri Düzey Analiz 
            with st.expander("🔍 Daha Fazla Veri"):
                # Volatilite Hesaplama
                volatility = df['Daily Change (%)'].std()
                st.markdown(f"### 📊 Volatilite Analizi")
                st.markdown(f"**30 Günlük Fiyat Volatilitesi (Standart Sapma):** {volatility:.2f}%")

                # Günlük Getiri Dağılımı
                st.markdown("### 📉 Günlük Getiri Dağılımı")
                fig2 = px.histogram(
                    df,
                    x='Daily Change (%)',
                    nbins=20,
                    title='Günlük Getiri Dağılımı',
                    labels={'Daily Change (%)': 'Günlük Değişim (%)'},
                    template='plotly_white'
                )
                st.plotly_chart(fig2, use_container_width=True)

                # Hareketli Ortalamalar
                st.markdown("### 📈 Hareketli Ortalamalar")
                df['7G MA'] = df['Price (USD)'].rolling(window=7).mean()
                df['14G MA'] = df['Price (USD)'].rolling(window=14).mean()
                fig3 = px.line(
                    df,
                    x='Date',
                    y=['Price (USD)', '7G MA', '14G MA'],
                    labels={'value': 'Fiyat (USD)', 'variable': 'Göstergeler'},
                    title='Hareketli Ortalamalar',
                    template='plotly_white'
                )
                st.plotly_chart(fig3, use_container_width=True)

    st.success("Simülasyon tamamlandı! 📊")

# ---------------------------
# Footer / alt kisim
# ---------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="footer">
    © 2025 Kripto Para Yatırım Simülasyonu. Tüm hakları saklıdır.
    </div>
    """,
    unsafe_allow_html=True
)