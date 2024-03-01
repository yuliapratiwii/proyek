import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Fungsi untuk menghitung total penyewaan per jam
def get_total_count_by_hour_df(hour_df):
    hour_count_df =  hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})
    return hour_count_df

# Fungsi untuk menghitung total penyewaan per hari dalam rentang tahun 2011-2012
def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')
    return day_df_count_2011

# Fungsi untuk menghitung total pelanggan terdaftar per hari
def total_registered_df(day_df):
    reg_df =  day_df.groupby(by="dteday").agg({"registered": "sum"})
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

# Fungsi untuk menghitung total pelanggan casual per hari
def total_casual_df(day_df):
    cas_df =  day_df.groupby(by="dteday").agg({"casual": ["sum"]})
    cas_df = cas_df.reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

# Fungsi untuk menghitung total order per jam
def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

# Fungsi untuk menghitung total penyewaan berdasarkan musim
def macem_season(day_df): 
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index() 
    return season_df

# Membaca data dari file CSV
days_df = pd.read_csv("dashboard/day_clean.csv")
hours_df = pd.read_csv("dashboard/hour_clean.csv")

# Melakukan penyesuaian pada kolom datetime
datetime_columns = ["dteday"]
for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

# Menentukan rentang tanggal yang dapat dipilih
min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

# Filter data berdasarkan rentang tanggal yang dipilih
start_date, end_date = st.date_input(
    label='Rentang Waktu',
    min_value=min_date_days,
    max_value=max_date_days,
    value=[min_date_days, max_date_days])

main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

# Menghasilkan visualisasi dengan Streamlit
st.header('Data Bike Sharing')



# Visualisasi Jumlah Penyewaan Sepeda Berdasarkan Musim
st.subheader("Tren Peminjaman Sepeda Berdasarkan Musim")
colors = ["#FFA07A", "#87CEEB", "#32CD32", "#FFD700"]
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="season", y="count_cr", data=macem_season(main_df_days), palette=colors, ax=ax)
ax.set_title("Jumlah Peminjaman Sepeda Berdasarkan Musim", fontsize=16)
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Jumlah Peminjaman", fontsize=12)
st.pyplot(fig)
st.write("Terlihat bahwa Fall Season memiliki tingkat penyewaan tertinggi yaitu 1,061,129, sedangkan pada Spring Season memiliki tingkat penyewaan yang rendah yaitu 471,348.")


# Visualisasi Tren Peminjaman Sepeda Tahunan
st.subheader("Tren Peminjaman Sepeda Tahunan")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=count_by_day_df(main_df_days), x="dteday", y="count_cr", color="#FFA07A", ax=ax)
ax.set_title("Tren Peminjaman Sepeda Tahunan", fontsize=16)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Jumlah Peminjaman", fontsize=12)
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)
st.write('dari visualisasi data pada gambar diatas, pada  September 2012 memiliki jumlah order terbayak dan pada januari 2011 mengalami penurunan order yang cukup signifikan')

# Total Penyewaan Sepeda per Tahun
st.subheader("Total Peminjaman Sepeda per Tahun")
total = main_df_days.groupby('year')[['registered', 'casual']].sum()
total['Jumlah penyewa'] = total.sum(axis=1)
years = total.index
total_rentals = total['Jumlah penyewa']
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(years, total_rentals, color=['#90CAF9', '#2196F3'])
ax.set_xlabel('Tahun')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Total Penyewaan Sepeda per Tahun')
st.pyplot(fig)
st.write("Terlihat jelas bahwa jumlah penyewaan pada tahun 2012 lebih tinggi dengan jumlah 2049576 daripada tahun 2011 dengan jumlah 2049576")