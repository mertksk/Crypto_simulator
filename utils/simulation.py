
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class CryptoSimulation:
    """
    Kripto para fiyat simülasyonunu gerçekleştiren sınıf.
    """

    def __init__(self, initial_price: float, start_date: datetime, days: int = 30):
        """
        Sınıfın yapıcı metodu.

        Parameters:
            initial_price (float): Kripto paranın başlangıç fiyatı.
            start_date (datetime): Simülasyonun başlangıç tarihi.
            days (int): Simülasyon süresi (gün cinsinden).
        """
        self.initial_price = initial_price
        self.start_date = start_date
        self.days = days
        self.df = self.simulate()

    def simulate(self) -> pd.DataFrame:
        """
        Günlük fiyat değişikliklerini simüle eder.

        Returns:
            pd.DataFrame: Günlük fiyatlar ve yüzde değişimleri içeren bölüm
        """
        # Sabit tohum kaldırıldı; böylece her simülasyon rastgele sonuç verir
        daily_changes = np.random.uniform(-0.05, 0.05, self.days)  # -5% ila +5%
        prices = [self.initial_price]

        for change in daily_changes:
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)

        simulated_dates = [self.start_date + timedelta(days=i) for i in range(1, self.days + 1)]

        df = pd.DataFrame({
            'Day': range(1, self.days + 1),
            'Date': simulated_dates,
            'Daily Change (%)': daily_changes * 100,
            'Price (USD)': prices[1:]
        })

        return df

    def get_final_investment(self, initial_investment: float) -> (float, float):
        """
        Simülasyon sonunda elde edilen yatırımı ve kar/zararı hesaplar.

        Parameters:
            initial_investment (float): Başlangıç yatırım tutarı.

        Returns:
            tuple: (Final yatırım miktarı, Kar/Zarar)
        """
        final_price = self.df["Price (USD)"].iloc[-1]
        final_investment = (final_price / self.initial_price) * initial_investment
        profit_loss = final_investment - initial_investment
        return final_investment, profit_loss