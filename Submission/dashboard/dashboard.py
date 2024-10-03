import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 

sns.set(style='dark')

dashboard_df = pd.read_csv("cleaned_days.csv")
dashboard_df.head()

# Kolom 'dteday' pada cleaned_days berubah kembali menjadi object, maka perlu diubah kembali menjadi datetime
dashboard_df['dteday'] = pd.to_datetime(dashboard_df['dteday'])

# Mengubah nama judul kolom
dashboard_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan


dashboard_df['year'] = dashboard_df['year'].map({
    0: 2011, 1: 2012
    })
dashboard_df['month'] = dashboard_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
dashboard_df['season'] = dashboard_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
    })
dashboard_df['weekday'] = dashboard_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
    })

# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = df.groupby(by=['month', 'year']).agg({
        'count': 'sum'
    }).reset_index()
    monthly_rent_df['month'] = pd.Categorical(
        monthly_rent_df['month'], categories=ordered_months, ordered=True
    )
    return monthly_rent_df


# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

min_date = dashboard_df["dateday"].min()
max_date = dashboard_df["dateday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = dashboard_df[(dashboard_df['dateday'] >= str(start_date)) & (dashboard_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)

# Membuat judul
st.header('Bike Rental Dashboard 🚲')

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value= daily_rent_total)


# Membuat jumlah penyewaan bulanan dari 2 tahun terakhir
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(12, 6))

# Plot garis untuk tahun 2011
ax.plot(
    monthly_rent_df[monthly_rent_df['year'] == 2011]['month'],
    monthly_rent_df[monthly_rent_df['year'] == 2011]['count'],
    marker='o', 
    linewidth=2,
    color='tab:blue',
    label='2011'
)

# Plot garis untuk tahun 2012
ax.plot(
    monthly_rent_df[monthly_rent_df['year'] == 2012]['month'],
    monthly_rent_df[monthly_rent_df['year'] == 2012]['count'],
    marker='o', 
    linewidth=2,
    color='tab:red',
    label='2012'
)

# Menambahkan label untuk setiap titik di garis tahun 2011
for index, row in monthly_rent_df[monthly_rent_df['year'] == 2011].iterrows():
    ax.text(row['month'], row['count'] + 1, str(int(row['count'])), ha='center', va='bottom', fontsize=12, color='blue')

# Menambahkan label untuk setiap titik di garis tahun 2012
for index, row in monthly_rent_df[monthly_rent_df['year'] == 2012].iterrows():
    ax.text(row['month'], row['count'] + 1, str(int(row['count'])), ha='center', va='bottom', fontsize=12, color='red')

ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=20)
ax.legend(title="Tahun", loc="lower right")

st.pyplot(fig)

st.subheader('Rentals Based on Workingday, Holiday, and Weekday')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 18))

# Plot berdasarkan workingday
colors1 = ["tab:blue", "tab:orange"]
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_rent_df,
    palette=colors1,
    ax=axes[0]
)

for index, row in enumerate(workingday_rent_df['count']):
    axes[0].text(index, row + 100, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_xticklabels(['registered', 'casual'])
axes[0].set_title('Number of Rents based on Workingday')
axes[0].set_ylabel('Rentals Count')
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Plot berdasarkan holiday
colors2 = ["tab:blue", "tab:orange"]
sns.barplot(
    x='holiday',
    y='count',
    data=holiday_rent_df,
    palette=colors2,
    ax=axes[1]
)

for index, row in enumerate(holiday_rent_df['count']):
    axes[1].text(index, row + 100, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_xticklabels(['registered', 'casual'])
axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel('Rentals Count')
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Plot berdasarkan weekday
colors3 = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
weekday_rent_df['weekday'] = pd.Categorical(
    weekday_rent_df['weekday'], categories=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], ordered=True)
sns.barplot(
    x='weekday',
    y='count',
    data=weekday_rent_df,
    palette=colors3,
    ax=axes[2]
)

for index, row in enumerate(weekday_rent_df['count']):
    axes[2].text(index, row + 100, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Weekday')
axes[2].set_ylabel('Rentals Count')
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

# Menampilkan semua plot sekaligus
st.pyplot(fig)

st.caption('Copyright (c) Kresna Pebriawan 2024')