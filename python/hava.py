import requests
import json
import tkinter as tk
from tkinter import messagebox

# OpenWeatherMap API anahtarı
API_KEY = '8b1b8a53440c323433037ba5924b9213'

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title('Hava Durumu Uygulaması')
        master.geometry('500x350')
        master.resizable(False, False)

        # Şehir seçim etiketi ve giriş kutusu
        self.city_label = tk.Label(master, text='Şehir: ')
        self.city_label.pack()
        self.city_entry = tk.Entry(master, width=40, font=('Arial', 14))
        self.city_entry.pack(pady=10)

        # Hava durumu butonu
        self.weather_button = tk.Button(master, text='Hava Durumu Göster', command=self.show_weather)
        self.weather_button.pack(pady=10)

        # Hava durumu sonuçları için çerçeve
        self.result_frame = tk.Frame(master)
        self.result_frame.pack()

    def show_weather(self):
        # Önceki sonuçları temizle
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Şehir adını al
        city = self.city_entry.get()
        if not city:
            messagebox.showerror('Hata', 'Lütfen bir şehir adı girin.')
            return

        # API'den hava durumu tahminlerini al
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)

        # Yanıtın durum koduna göre kontrol et
        if response.status_code != 200:
            messagebox.showerror('Hata', 'Hava durumu tahmini alınamadı. Lütfen şehir adını kontrol edin.')
            return

        # Yanıtı JSON olarak işle
        data = json.loads(response.text)

        # Hava durumu tahminlerini göster
        city_label = tk.Label(self.result_frame, text=data['city']['name'], font=('Arial', 18, 'bold'))
        city_label.pack()
        for i in range(0, 40, 8):
            date = data['list'][i]['dt_txt']
            temp = data['list'][i]['main']['temp']
            humidity = data['list'][i]['main']['humidity']
            weather = data['list'][i]['weather'][0]['description']
            icon = data['list'][i]['weather'][0]['icon']
            self.add_weather_widget(date, temp, humidity, weather, icon)

    def add_weather_widget(self, date, temp, humidity, weather, icon):
        # Hava durumu tahminleri için çerçeve oluştur
        weather_frame = tk.Frame(self.result_frame, padx=10, pady=10)
        weather_frame.pack(side=tk.LEFT)

        # Tarih etiketi