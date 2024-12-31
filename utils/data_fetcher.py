
import requests
import streamlit as st

class DataFetcher:
    """
    CoinGecko API'sinden kripto para verilerini fetch etmek için kullanılacak sınıf.
    """

    COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

    @staticmethod
    def fetch_current_price(crypto_id: str) -> float:
        """
        Güncel kripto para fiyatını USD cinsinden alır.

        Parameters:
            crypto_id (str): CoinGecko'daki kripto para ID'si (örn. 'bitcoin').

        Returns:
            float: Kripto paranın güncel USD fiyatı.
        """
        url = f"{DataFetcher.COINGECKO_API_URL}/simple/price"
        params = {"ids": crypto_id, "vs_currencies": "usd"}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            price = data.get(crypto_id, {}).get("usd", None)
            if price is None:
                st.error(f"{crypto_id.capitalize()} için fiyat bilgisi bulunamadı.")
            return price
        except requests.RequestException as e:
            st.error(f"Fiyat verisi alınamadı: {e}")
            return None

    @staticmethod
    def fetch_historical_price(crypto_id: str, date_str: str) -> float:
        """
        Belirli bir tarihteki kripto para fiyatını CoinGecko API'den alır.

        Parameters:
            crypto_id (str): CoinGecko'daki kripto para ID'si (örn. 'bitcoin').
            date_str (str): Tarih stringi, format "DD-MM-YYYY".

        Returns:
            float: Belirtilen tarihteki USD fiyatı veya None.
        """
        url = f"{DataFetcher.COINGECKO_API_URL}/coins/{crypto_id}/history"
        params = {"date": date_str, "localization": "false"}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            price = data['market_data']['current_price']['usd']
            return price
        except (requests.RequestException, KeyError) as e:
            st.error(f"Belirtilen tarihte fiyat bilgisi alınamadı: {e}")
            return None