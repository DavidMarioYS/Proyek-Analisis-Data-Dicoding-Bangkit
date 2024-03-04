import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Membaca file day.csv
day_df = pd.read_csv('day.csv')

st.title('Proyek Analisis Data: [Bike Sharing Dataset]')

st.markdown(
    """
    - **Nama:** DAVID MARIO YOHANES SAMOSIR
    - **Email:** david.mario@undiksha.ac.id
    - **ID Dicoding:** davidmarioys
    """
)

with st.sidebar:
    
    st.title('Profile')
    
    st.markdown(
    """
    - **Nama:** DAVID MARIO YOHANES SAMOSIR
    - **Email:** david.mario@undiksha.ac.id
    - **ID Dicoding:** davidmarioys 
    """
    )
    
st.title('Pertanyaan Bisnis')
col1, col2, col3 = st.columns(3)
 
with col1:
    st.header("Pertanyaan 1")
    st.write('Berapa persentase dari penggunaan sepeda pada hari kerja dan libur?')
 
with col2:
    st.header("Pertanyaan 2")
    st.write('Bagaimana cuaca dan musim mempengaruhi preferensi peminjaman sepeda pada hari kerja dan libur?')
 
with col3:
    st.header("Pertanyaan 3")
    st.write('Berapa persentase kenaikan atau penurunan dari penggunaan sepeda berdasarkan peminjam yang terdaftar dan tidak terdaftar setiap bulannya.')
    
st.title('Proses Data')
tab1, tab2, tab3, tab4 = st.tabs(["Data Wrangling", "Exploratory Data Analysis (EDA)", "Data Visualization", "Conclusion"])
 
with tab1:
    st.header("Data Wrangling")
    st.subheader('Gathering Data')
    st.markdown(
    """
    - Membaca file dengan format `.csv`
    - Menampilkan isi file
    """
    )
    st.dataframe(day_df)
    
    st.subheader('Assessing Data')
    st.markdown(
    """
    - Mengecek data yang tidak lengkap dengan perintah `.isna().sum()`
    - Mengecek data invalid dengan `.info()`
    - Mengecek data duplikat dengan perintah `.duplicated().sum()`
    """
    )
    nan_df = day_df[day_df.isna()]
    st.dataframe(nan_df)
    
    st.subheader('Cleaning Data')
    st.markdown(
    """
    - Melakukan pembersihan data dengan perintah `drop` pada data bias
    """
    )
     
with tab2:
    st.header("Exploratory Data Analysis (EDA)")
    st.markdown(
    ### Explore Data day_df
    """
    - Mengelompokan data berdasarkan data `season` terhadap jumlah pengguna dan cuaca
    """
    )
    season_counts = day_df.groupby(by="season").cnt.count().rename({1: '1. Spring', 2: '2. Summer', 3: '3. Fall', 4: '4. Winter'})
    st.dataframe(season_counts.reset_index().rename(columns={'season': 'Musim', 'cnt': 'Jumlah'}))
    # Groupby Musim Berdasarkan Keadaan Cuaca
    seasonal_analysis = day_df.groupby(by="season").agg({
        "cnt": ["mean", "std"],
        "temp": ["mean", "std"],
        "hum": ["mean", "std"],
        "windspeed": ["mean", "std"]
    }).reset_index()
    st.table(seasonal_analysis)
    
    st.markdown(
    ### Explore Data day_df
    """
    - Mengelompokan berdasarkan data `holiday` terhadap jumlah pengguna
    """
    )
    st.write("Data Holiday:")
    holiday_count = day_df.groupby(by="holiday").cnt.count().reset_index()
    st.dataframe(holiday_count)
    # Groupby Hari Libur
    holiday_analysis = day_df.groupby(by="holiday").agg({
        "cnt": ["max", "min", "mean", "std"]
    }).reset_index()
    st.table(holiday_analysis)
    
    st.write("Data Workingday:")
    workingday_count = day_df.groupby(by="workingday").cnt.count()
    st.dataframe(workingday_count)
    # Groupby Hari Kerja
    workday_analysis = day_df.groupby(by="workingday").agg({
        "cnt": ["max", "min", "mean", "std"]
    }).reset_index()
    st.table(workday_analysis)
        
    st.markdown(
    ### Explore Data day_df
    """
    - Mengelompokan berdasarkan data `weathersit` terhadap jumlah pengguna
    """
    )
    weather_count = day_df.groupby(by="weathersit").cnt.sum().rename({1: '1. Cerah', 2: '2. Mendung', 3: '3. Hujan'})
    st.dataframe(weather_count)
    # Groupby Cuaca
    holiday_analysis = day_df.groupby(by="weathersit").agg({
        "cnt": ["mean", "std"],
        "temp": ["mean", "std"],
        "hum": ["mean", "std"],
        "windspeed": ["mean", "std"]
    }).reset_index()
    st.table(holiday_analysis)
    
    st.markdown(
    ### Explore Data day_df
    """
    - Mengelompokan berdasarkan data `mnth` terhadap jumlah pengguna terdaftar dan tidak terdaftar
    """
    )
    month_count = day_df.groupby(by="mnth").cnt.count()
    st.dataframe(month_count.reset_index())
    # Groupby Bulan
    st.write("Data Casual:")
    month_analysis = day_df.groupby(by="mnth").agg({
        "casual": ["max", "min", "sum", "mean", "std"]
    }).reset_index()
    st.table(month_analysis)
    st.write("Data Registered:")
    # Groupby Bulan
    month_analysis = day_df.groupby(by="mnth").agg({
        "registered": ["max", "min", "sum", "mean", "std"]
    }).reset_index()
    st.table(month_analysis)
 
with tab3:
    st.header("Data Visualization")
    st.subheader('Histogram Day.csv')
    fig, ax = plt.subplots(figsize=(10, 10))
    day_df.hist(ax=ax)
    st.pyplot(fig)
    
    st.subheader('Histogram Day.csv')
    # Membuat DataFrame untuk heatmap
    heatmap_data = day_df[['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']]
    # Menghitung korelasi antar kolom
    correlation_matrix = heatmap_data.corr()
    # Menampilkan heatmap pada Streamlit
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)
    st.pyplot(fig)
    
    st.title('Pertanyaan 1')
    st.text('Berapa persentase dari penggunaan sepeda pada hari kerja dan libur?')
    st.write("- Total peminjaman pada hari libur")
    total_rental_holiday = day_df.groupby(by="holiday").cnt.sum()
    st.dataframe(total_rental_holiday)
    st.write("- Total peminjaman pada hari kerja")
    total_rental_workday = day_df.groupby(by="workingday").cnt.sum()
    st.dataframe(total_rental_workday)
    # Visualisasi perbandingan
    labels = ['Hari Libur', 'Hari Kerja']
    values_holiday = total_rental_holiday.values
    values_workday = total_rental_workday.values
    # Warna untuk pie chart
    colors_holiday = ['blue', 'yellow']
    colors_workday = ['blue', 'yellow']
    values_holiday = day_df[day_df['holiday'] == 0]['cnt'].sum(), day_df[day_df['holiday'] == 1]['cnt'].sum()
    values_workday = day_df[day_df['workingday'] == 0]['cnt'].sum(), day_df[day_df['workingday'] == 1]['cnt'].sum()
    labels = ['Peminjaman Sepeda', 'Lainnya']
    # Visualisasi Pie Chart pada Streamlit
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
    # Pie Chart Hari Libur
    ax1.pie(values_holiday, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors_holiday)
    ax1.set_title('Persentase Peminjaman Sepeda pada Hari Libur')
    # Pie Chart Hari Kerja
    ax2.pie(values_workday, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors_workday)
    ax2.set_title('Persentase Peminjaman Sepeda pada Hari Kerja')
    # Keterangan warna
    legend_labels = ['Peminjaman Sepeda', 'Lainnya']
    fig.legend(legend_labels, loc='lower center', bbox_to_anchor=(1, 0.5))
    # Layout Subplot yang Rapi
    fig.tight_layout()
    # Menampilkan Pie Chart pada Streamlit
    st.pyplot(fig)

    st.markdown(
        """
        - Hari Libur:
        > 97.6% peminjaman sepeda pada hari libur terkonsentrasi pada Peminjaman Sepeda
        > Hanya 2.4% peminjaman sepeda pada hari libur yang termasuk dalam kategori Lainnya
        """
        """
        - Hari Kerja:
        > 30.4% peminjaman sepeda pada hari kerja terkonsentrasi pada Peminjaman Sepeda
        > 69.6% peminjaman sepeda pada hari kerja termasuk dalam kategori Lainnya
        """
    )
        
    st.title('Pertanyaan 2')
    st.text('Bagaimana cuaca dan musim mempengaruhi preferensi peminjaman sepeda pada hari kerja dan libur?')
    # Data
    heatmap_data = day_df.pivot_table(index='season', columns='weathersit', values='cnt', aggfunc='sum')
    # Plot Heatmap
    st.write("- Heatmap berdasarkan Cuaca dan Musim")
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt='g')
    plt.title('Heatmap Jumlah Peminjaman Sepeda berdasarkan Cuaca dan Musim')
    plt.xlabel('Cuaca (Weathersit)')
    plt.ylabel('Musim (Season)')
    # Menampilkan plot pada dashboard Streamlit
    st.pyplot(plt)
    
    st.write("- Visualisasi Total Peminjaman Berdasarkan Musim")
    # Membuat DataFrame untuk visualisasi
    season_data = day_df[['season', 'casual', 'registered', 'cnt']]
    # Menghitung total peminjaman untuk setiap musim
    season_total = season_data.groupby('season').sum()
    # Membuat bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=season_total.index, y='cnt', data=season_total, palette='viridis')
    plt.title('Total Peminjaman Sepeda Berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel('Total Peminjaman Sepeda')
    # Menampilkan plot pada dashboard Streamlit
    st.pyplot(plt)
    
    st.write("- Visualisasi Total Peminjaman Berdasarkan Cuaca")
    # Membuat DataFrame untuk visualisasi
    weather_data = day_df[['weathersit', 'casual', 'registered', 'cnt']]
    # Menghitung total peminjaman untuk setiap jenis cuaca
    weather_total = weather_data.groupby('weathersit').sum()
    # Membuat bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=weather_total.index, y='cnt', data=weather_total, palette='coolwarm')
    plt.title('Total Peminjaman Sepeda Berdasarkan Cuaca')
    plt.xlabel('Cuaca')
    plt.ylabel('Total Peminjaman Sepeda')
    # Menampilkan plot pada dashboard Streamlit
    st.pyplot(plt)
    
    st.write("- Visualisasi Pengaruh Cuaca dan Musim terhadap Peminjaman Sepeda")
    # Membuat DataFrame untuk visualisasi
    combined_data = day_df[['season', 'weathersit', 'workingday', 'cnt']]
    # Mendefinisikan urutan cuaca untuk memastikan plot yang benar
    weather_order = [1, 2, 3]
    # Membuat bar plot dengan facet grid
    plt.figure(figsize=(15, 10))
    g = sns.FacetGrid(combined_data, col='workingday', row='season', margin_titles=True)
    g.map(sns.barplot, 'weathersit', 'cnt', order=weather_order, palette='coolwarm')
    # Menyesuaikan tata letak dan judul
    g.set_axis_labels('Cuaca', 'Total Peminjaman Sepeda')
    g.set_titles(col_template='{col_name} - Hari Kerja', row_template='{row_name} - Musim')
    plt.suptitle('Pengaruh Cuaca dan Musim terhadap Peminjaman Sepeda', size=16, y=1.02)
    # Menampilkan plot pada dashboard Streamlit
    st.pyplot(plt)
    
    st.write("- Grafik Time Series Jumlah Peminjaman Sepeda berdasarkan Cuaca dan Musim")
    # Membuat DataFrame untuk visualisasi
    time_series_data = day_df.pivot_table(index='dteday', columns=['season', 'weathersit'], values='cnt', aggfunc='sum')
    # Membuat plot time series
    plt.figure(figsize=(16, 8))
    time_series_data.plot(figsize=(16, 8))
    plt.title('Grafik Time Series Jumlah Peminjaman Sepeda berdasarkan Cuaca dan Musim')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Peminjaman Sepeda')
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    # Menampilkan plot pada dashboard Streamlit
    st.pyplot(plt)
    
    st.title('Pertanyaan 3')
    st.text('Berapa persentase kenaikan atau penurunan dari penggunaan sepeda berdasarkan peminjam yang terdaftar dan tidak terdaftar setiap bulannya?')
    # Membuat dataframe baru yang berisi informasi bulanan
    monthly_data = day_df.groupby(['mnth']).agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()
    # Membuat plot bar chart
    plt.figure(figsize=(14, 8))
    bar_width = 0.4
    bar_positions = range(len(monthly_data))
    plt.bar(bar_positions, monthly_data['casual'], width=bar_width, label='Casual', color='blue', alpha=0.7)
    plt.bar([pos + bar_width for pos in bar_positions], monthly_data['registered'], width=bar_width, label='Registered', color='orange', alpha=0.7)
    plt.title('Perbandingan Peminjaman Sepeda Casual dan Registered Setiap Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Peminjaman Sepeda')
    plt.xticks([pos + bar_width / 2 for pos in bar_positions], monthly_data['mnth'])
    plt.legend()
    # Menampilkan plot pada dashboard Streamlit
    st.pyplot(plt)
    
    # Membuat dataframe baru yang berisi informasi bulanan
    monthly_data = day_df.groupby(['mnth']).agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()

    # Menghitung persentase kenaikan atau penurunan setiap bulan
    monthly_data['casual_percentage_change'] = monthly_data['casual'].pct_change() * 100
    monthly_data['registered_percentage_change'] = monthly_data['registered'].pct_change() * 100

    # Merubah format persentase
    monthly_data['casual_percentage_change'] = monthly_data['casual_percentage_change'].map("{:.2f}%".format)
    monthly_data['registered_percentage_change'] = monthly_data['registered_percentage_change'].map("{:.2f}%".format)

    # Menampilkan hasil menggunakan Streamlit
    st.table(monthly_data[['mnth', 'casual_percentage_change', 'registered_percentage_change']])
    
with tab4:
    st.header("Conclusion")
    st.markdown(
    ### Explore Data day_df
    """
    - Conclusion Pertanyaan 1
    >Berdasarkan hasil data yang didapatkan dapat diketahui bahwa pada hari libur, mayoritas peminjaman sepeda terjadi sangat tinggi cenderung dianggap sebagai kegiatan rekreasi atau hobi.
    """
    
    ### Explore Data day_df
    """
    - Conclusion Pertanyaan 2
    > Berdasarkan hasil data yang didapatkan dapat diketahui bahwa cuaca dan musim memiliki peran dalam memengaruhi tingkat peminjaman sepeda. Faktor-faktor ini dapat menjadi pertimbangan penting dalam pengelolaan sistem peminjaman sepeda, dan mungkin dapat digunakan untuk merancang strategi pemasaran atau penyesuaian layanan berdasarkan kondisi cuaca dan musim tertentu.
    """
    
    ### Explore Data day_df
    """
    - Conclusion Pertanyaan 3
    > Berdasarkan hasil data yang didapatkan dapat diketahui bahwa Pengguna casual cenderung mengalami fluktuasi yang lebih besar dari bulan ke bulan, dengan kenaikan dan penurunan yang signifikan, sedangkan pengguna registered, meskipun mengalami variasi, menunjukkan kenaikan yang lebih konsisten dan penurunan yang lebih terbatas dibandingkan pengguna casual.
    """
    )