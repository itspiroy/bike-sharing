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
    
    selected_season = st.multiselect(
        "🗓 Pilih Musim:",
        options=["Spring", "Summer", "Fall", "Winter"],
        default=["Spring", "Summer", "Fall", "Winter"]
    )

st.title("Bike Sharing Dataset")
st.write("Visualisasi ini menganalisis distribusi penyawaan sepeda berdasarkan musim dan tipe penyewa.")
st.markdown("---")

# Filter dataset berdasarkan rentang tanggal dan musim
day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df = day_df[day_df['season'].isin(selected_season)]

# 1. Visualisasi distribusi penyewaan sepeda pada setiap musim
st.subheader("Bagaimana distribusi penyewaan sepeda pada setiap musim?")
season_avg = day_df.groupby('season')['cnt'].mean().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(x='season', y='cnt', data=season_avg, palette=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
plt.title('Distribusi Penyewaan Sepeda pada Setiap Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Penggunaan Sepeda')
st.pyplot(plt)

# 2. Visualisasi distribusi penyewaan sepeda berdasarkan tipe penyewa
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
