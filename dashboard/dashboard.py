import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

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

    # Perbaikan: Konversi tanggal ke datetime sebelum filter
    start_date, end_date = st.date_input(
        label="📅 Rentang Waktu",
        min_value=min_date.date(),
        max_value=max_date.date(),
        value=[min_date.date(), max_date.date()]
    )

    # Konversi start_date dan end_date ke datetime64
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    selected_season = st.multiselect(
        "🗓 Pilih Musim:",
        options=["Spring", "Summer", "Fall", "Winter"],
        default=["Spring", "Summer", "Fall", "Winter"]
    )

st.title("Bike Sharing Dataset")
st.write("Visualisasi ini menganalisis distribusi penyewaan sepeda berdasarkan musim dan tipe penyewa.")
st.markdown("---")

# Filter dataset berdasarkan rentang tanggal dan musim
day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
filtered_day_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
filtered_day_df = filtered_day_df[filtered_day_df['season'].isin(selected_season)]

# 1. Pengaruh kondisi cuaca terhadap jumlah penggunaan sepeda pada berbagai jam dalam sehari
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
plt.tight_layout()

st.pyplot(plt)

# 2. Distribusi penyewaan sepeda berdasarkan tipe penyewa
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
