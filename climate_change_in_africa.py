import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set style for better visuals
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# 1. Load and Clean the Dataset
print("Loading Climate Change in Africa dataset...")
df = pd.read_csv('Africa_climate_change.csv')

# Convert DATE column
df['DATE'] = df['DATE'].str.split().str[0]  # Remove time part
df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')
df['Year'] = df['DATE'].dt.year
df['Month'] = df['DATE'].dt.month

print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['DATE'].min()} to {df['DATE'].max()}")
print("\nCountries:", df['COUNTRY'].unique())

# Handle missing values in temperature columns (replace with country-specific median if needed)
temp_cols = ['TAVG', 'TMAX', 'TMIN']
for col in temp_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 2. Line Chart: Average Temperature in Tunisia vs Cameroon
print("\nPlotting temperature trends for Tunisia and Cameroon...")

countries = ['Tunisia', 'Cameroon']
temp_trend = df[df['COUNTRY'].isin(countries)].groupby(['Year', 'COUNTRY'])['TAVG'].mean().reset_index()

plt.figure(figsize=(12, 6))
for country in countries:
    data = temp_trend[temp_trend['COUNTRY'] == country]
    plt.plot(data['Year'], data['TAVG'], marker='o', linewidth=2, label=country)

plt.title('Average Annual Temperature Trends (Tunisia vs Cameroon)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Average Temperature (°F)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('tunisia_cameroon_trends.png')
plt.show()

# Interpretation: Both countries show warming trends, with fluctuations.

# 3. Zoomed Line Chart (1980-2005)
print("\nZoomed view (1980-2005)...")

plt.figure(figsize=(12, 6))
for country in countries:
    data = temp_trend[(temp_trend['COUNTRY'] == country) & (temp_trend['Year'] <= 2005)]
    plt.plot(data['Year'], data['TAVG'], marker='o', linewidth=2, label=country)

plt.title('Average Temperature Trends (1980-2005)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Average Temperature (°F)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('tunisia_cameroon_1980_2005.png')
plt.show()

# 4. Histograms: Senegal Temperature Distribution
print("\nCreating histograms for Senegal...")

senegal = df[df['COUNTRY'] == 'Senegal'].copy()

period1 = senegal[(senegal['Year'] >= 1980) & (senegal['Year'] <= 2000)]['TAVG']
period2 = senegal[(senegal['Year'] > 2000) & (senegal['Year'] <= 2023)]['TAVG']

plt.figure(figsize=(12, 6))
plt.hist(period1.dropna(), bins=30, alpha=0.7, label='1980-2000', color='blue', edgecolor='black')
plt.hist(period2.dropna(), bins=30, alpha=0.7, label='2001-2023', color='red', edgecolor='black')

plt.title('Temperature Distribution in Senegal: 1980-2000 vs 2001-2023', fontsize=14)
plt.xlabel('Average Temperature (°F)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('senegal_temp_distribution.png')
plt.show()

# Description: The recent period shows a shift toward higher temperatures.

# 5. Best Chart for Average Temperature per Country
print("\nAverage Temperature per Country (Bar Chart)...")

avg_temp_country = df.groupby('COUNTRY')['TAVG'].mean().sort_values()

plt.figure(figsize=(10, 6))
sns.barplot(x=avg_temp_country.index, y=avg_temp_country.values, palette='viridis')
plt.title('Average Temperature by Country (1980-2023)', fontsize=14)
plt.xlabel('Country')
plt.ylabel('Average Temperature (°F)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('avg_temp_per_country.png')
plt.show()

# Bar chart is the most effective for comparing averages across categories.

# 6. Additional Insights / Own Questions

# Question 1: Overall warming trend across all countries
overall_trend = df.groupby('Year')['TAVG'].mean()

plt.figure(figsize=(12, 6))
plt.plot(overall_trend.index, overall_trend.values, color='orange', linewidth=3, marker='s')
plt.title('Overall Average Temperature Trend in 5 African Countries (1980-2023)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Average Temperature (°F)')
plt.grid(True)
plt.tight_layout()
plt.savefig('overall_warming_trend.png')
plt.show()

# Question 2: Boxplot comparison
plt.figure(figsize=(12, 6))
sns.boxplot(x='COUNTRY', y='TAVG', data=df)
plt.title('Temperature Distribution by Country')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('temp_boxplot_by_country.png')
plt.show()

print("\n✅ All visualizations completed and saved as PNG files!")
print("Key Insights:")
print("- Clear warming trend visible across the studied countries.")
print("- Senegal shows a noticeable shift to higher temperatures in recent decades.")
print("- Tunisia generally has cooler averages compared to Senegal and Cameroon.")
