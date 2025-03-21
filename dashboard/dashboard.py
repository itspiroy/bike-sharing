import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

sns.set(style="whitegrid")

# Membaca dataset
day_df = pd.read_csv("https://raw.githubusercontent.com/itspiroy/bike-sharing/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/itspiroy/bike-sharing/refs/heads/main/data/hour.csv")

# Konversi kolom tanggal ke format datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Tentukan rentang tanggal minimum dan maksimum
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

# Sidebar untuk interaksi pengguna
with st.sidebar:
    st.image("https://st4.depositphotos.com/2664341/31427/v/380/depositphotos_314276156-stock-illustration-illustration-cartoon-cute-boy-riding.jpg")
    start_date, end_date = st.date_input(
        label="📅 Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.title("Bike Sharing Dataset")
st.write("Visualisasi ini menganalisis distribusi penyewaan sepeda berdasarkan tipe penyewa.")
st.markdown("---")

# Filter dataset berdasarkan rentang tanggal
day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]

# Menampilkan Total Penyewaan dan Rata-rata Harian
total_penyewaan = day_df['cnt'].sum()
rata_rata_harian = day_df['cnt'].mean()

col1, col2 = st.columns(2)
col1.metric("Total Penyewaan", f"{total_penyewaan:,}")
col2.metric("Rata-rata Harian", f"{rata_rata_harian:,.2f}")

st.markdown("---")

# Menampilkan Penyewaan Sepeda Harian
st.subheader("Penyewaan Sepeda Harian")
plt.figure(figsize=(12, 6))
sns.lineplot(x='dteday', y='cnt', data=day_df, marker='o')
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Penyewaan")
plt.xticks(rotation=45)
st.pyplot(plt)

# 1. Bagaimana pengaruh kondisi cuaca terhadap jumlah penggunaan sepeda pada berbagai jam dalam sehari?
st.subheader("Bagaimana pengaruh kondisi cuaca terhadap jumlah penggunaan sepeda pada berbagai jam dalam sehari?")
weather_avg = hour_df.groupby(['hr', 'weathersit'])['cnt'].mean().reset_index()
weather_avg['weathersit'] = weather_avg['weathersit'].map({
    1: 'Clear',
    2: 'Cloudy',
    3: 'Rain',
    4: 'Severe'
})

plt.figure(figsize=(10, 6))
colors = ['#99ff99', '#ff9999', '#ffcc99', '#66b3ff']
for i, (name, group) in enumerate(weather_avg.groupby('weathersit')):
    plt.bar(group['hr'] + i * 0.2, group['cnt'], width=0.2, label=name, color=colors[i])

plt.title('Pengaruh Cuaca terhadap Waktu Peminjaman Sepeda')
plt.xlabel('Jam dalam Sehari')
plt.ylabel('Jumlah Penggunaan Sepeda')
plt.xticks(range(0, 24))  
plt.legend(title='Cuaca')
st.pyplot(plt)

# 2. Bagaimana distribusi penyewaan sepeda berdasarkan tipe penyewa?
st.subheader("Bagaimana distribusi penyewaan sepeda berdasarkan tipe penyewa?")
hour_df['user_type'] = hour_df['registered'].apply(lambda x: 'Registered' if x > 0 else 'Casual')
user_type_avg = hour_df.groupby(['hr', 'user_type'])['cnt'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(x='hr', y='cnt', hue='user_type', data=user_type_avg, marker='o')
plt.title('Distribusi Penyewaan Sepeda Berdasarkan Tipe Penyewa')
plt.xlabel('Jam dalam Sehari (0-23)')
plt.ylabel('Jumlah Penggunaan Sepeda')
plt.xticks(range(0, 24))
st.pyplot(plt)
