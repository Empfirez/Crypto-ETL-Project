# Cryptocurrency ETL project



## Table of Contents
- [Project Overview](#project-overview)
- [Data Sources](#data-sources)
- [Tools](#tools)
- [Data Cleaning/Preparation](#data-cleaningpreparation)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Data Analysis](#data-analysis)
- [Data Visualization](#data-visualization)
- [Results/Findings](#resultsfindings)
- [Recommendations](#recommendations)
- [Limitations](#limitations)





### Project Overview
This data analysis project aims showcase the extraction of cryptocurrency data through the CoinMarketCap API and subsequently transform the extracted data using Pandas. The cleaned dataset can then be saved as a csv file to be loaded into SQL Server/
Microsoft Power BI for data visualization. However, Plotly is used to visualize the cleaned data for the purpose of this project due to its compatibility with Pandas.



### Data Sources

The primary data source used for this analysis is the CoinMarketCap API which is not only free to use, but also provides comprehensive coverage of key metrics such as price, volume, market capitalization, circulating supply, and percent change across multiple time frames. Not only that, it also provides well-documented endpoints, making it developer-friendly and easy to integrate as well as generous rate limits on the free tier, allowing for frequent and consistent data retrieval during the analysis.


### Tools

- Python(Programming Language)

- Jupyter Notebook/VSCode(Development Environment)
  
- Pandas(Data Cleaning)

- Requests/HTTP Client(API Calls)
  
- Plotly/Seaborn(Data Visualization)




### Data Cleaning/Preparation

In the data preparation phase of the project, we performed the following tasks:

API Data Retrieval: Retrieved real-time and historical cryptocurrency data using the CoinMarketCap API, including listings, metadata, price, market cap, volume, and percent changes.

Automated Data Retrieval: Automated the data retrieval process to obtain historical cryptocurrency data over a span of time.

Missing Values Handling: Checked for any missing or null values in key fields such as name, id and price.

Deduplication: Removed any duplicate entries resulting from overlapping API pulls or pagination handling.

Column Dropping: Dropped columns that are not integral to the analysis process.

Data Type Correction: Ensured consistency in data types such as float for price and volume fields and integer for rank.

Date Conversion: Converted string-based datetime fields (e.g., date_added, last_updated) into datetime objects for time-based analysis.

String Conversion: Converted stringifies lists in tags column to real lists using ast.literal_eval() function.

Filtering & Selection: Filtered out stablecoins, meme coins, low-volume coins, or entries with incomplete data based on specific thresholds to improve analysis quality.

Caching or Rate Limiting Management: Implemented time delays or caching to respect CoinMarketCap API rate limits and avoid exceeding the limit given.


### Exploratory Data Analysis

EDA is used to summarize the data and allows us to gain a deeper understanding of the dataset retrieved from the CoinMarketCap API. It answers key questions such as:

 - Which cryptocurrencies are leading in terms of market capitalization and trading volume?

 - Which coins have shown the highest volatility or consistent growth?

 - Are there correlations between volume, market cap, and price changes?

 - How does the performance of altcoins compare to that of major coins like Bitcoin and Ethereum?

 - Are there emerging coins or sectors gaining traction in the market?


### Data Analysis

During the analysis phase, the following steps were taken to process and explore the cryptocurrency data:

1. The tags column in all datasets (listings_df, all_data_df, and hist_df) was originally in string format. These strings were converted into Python lists using ast.literal_eval() to enable easier filtering and analysis.

	#### Converting tags column to actual list
	```python
	listings_df['tags'] = listings_df['tags'].apply(
	    lambda x: ast.literal_eval(x) if pd.notna(x) and x.startswith('[') else []
	)

 	all_data_df['tags'] = all_data_df['tags'].apply(
	    lambda x: ast.literal_eval(x) if pd.notna(x) and x.startswith('[') else []
	)
	
 	hist_df['tags'] = hist_df['tags'].apply(
	    lambda x: ast.literal_eval(x) if pd.notna(x) and x.startswith('[') else []
	)


2. Date-related columns such as date_added, last_updated, and last_updated.1 were converted from strings to datetime objects using pd.to_datetime() to facilitate time-based filtering, sorting, and visualization.
   
	#### Converting date column to datetime object
 	```python
	date_cols = ['date_added', 'last_updated', 'last_updated.1' ]
	for column in date_cols:
	    if column in listings_df.columns:
	        listings_df[column] = pd.to_datetime(listings_df[column])
	    else:
	        print(f"Column '{column}' not found in DataFrame.")
	listings_df.dtypes


3. Specific coins were located using both index-based access and conditional filtering to extract their data for inspection or comparison.
   
 	 #### Locating name of the coin with index number 4256
  	 ```python
	listings_df.loc[4256,'name']
	coin = listings_df.loc[listings_df['name'] == 'SmartMesh']


4. A new DataFrame was created to isolate coins that experienced a positive price change over the last 90 days. Further filtering was applied to remove coins associated with specific tags and exclude entries with empty tag lists to focus on well-categorized projects
	#### Listing only coins with positive change in the last 90 days and exlcude coins with specific tags/empty tag list
	```python
 	positive_90_days_df = listings_df[listings_df['percent_change_90d']>0].sort_values(by='percent_change_90d', ascending=False)
	exclude_list=['memes','base-ecosystem']
	positive_90_days_df = positive_90_days_df[~positive_90_days_df['tags'].apply(lambda x: any(tag in exclude_list for tag in x))]
	positive_90_days_df = positive_90_days_df[listings_df['tags'].apply(len) > 0]


5. The top 10 coins by market dominance were extracted, and their combined dominance was calculated. If their total was less than 100%, a new entry labeled "Remaining" was added to represent the combined dominance of all other cryptocurrencies.
	#### Listing the market dominance of top 10 coins and calculating the remaining market dominance %
	```python	
	top_10_market_dominance = top_10_df[['name','market_cap_dominance','symbol']]
	if top_10_market_dominance['market_cap_dominance'].sum() < 100:
	    top_10_market_dominance = pd.concat([
	        top_10_market_dominance,
	        pd.DataFrame([{'name':'Remaining','market_cap_dominance': 100 - top_10_market_dominance['market_cap_dominance'].sum()}])
	    ])

 
6. For a selected coin, short-term trends were analyzed by computing 15-minute rolling averages for near-term smoothing as well as a 30-minute rolling averages for a broader trend perspective.
	####  Adding new moving average columns and calculating 15/30mins moving average
	```python
	coin='Bitcoin'
	rolling_avg_15m_df = hist_df[hist_df['name'] == coin].copy()
	rolling_avg_30m_df = rolling_avg_15m_df.copy()
	rolling_avg_15m_df['rolling_average'] = rolling_avg_15m_df['price'].rolling(window=3).mean()
	rolling_avg_30m_df['rolling_average'] = rolling_avg_30m_df['price'].rolling(window=6).mean()


7. The top 10 tags were identified and average growth % within 90 days was calculated for each tag .
	####  Identifying top 10 sectors and calculating growth %
	```python
	all_tags = list(chain.from_iterable(listings_df['tags']))
	tag_counts = Counter(all_tags)
	top_10_tags_list = tag_counts.most_common(10)
	top_10_tags = [tag for tag, _ in top_10_tags_list]
	top_10_tags_df = listings_df[listings_df['tags'].apply(lambda tags: any(tag in top_10_tags for tag in tags))]
	tag_growth = defaultdict(list)
	for _, row in top_10_tags_df.iterrows():
	    for tag in row['tags']:
	        if tag in top_10_tags:
	            tag_growth[tag].append(row['percent_change_90d'])
	avg_growth_per_tag = {tag: sum(values) / len(values) for tag, values in tag_growth.items()}
	sorted_avg_growth = sorted(avg_growth_per_tag.items(), key=lambda x: x[1], reverse=True)


### Data Visualization

#### Top 10 crytocurrencies by 24h trading volume(USD)
![image](https://github.com/user-attachments/assets/9a90f93b-6a29-4bb8-9197-61f87420d9ce)


#### Market cap dominance
![image](https://github.com/user-attachments/assets/90696f79-a2c7-4098-85ea-f05afc9cd00c)


#### Percent change heatmap
![image](https://github.com/user-attachments/assets/7f14e483-a45d-47b1-bea3-2c4d9649b493)


#### Percent change over time
![image](https://github.com/user-attachments/assets/c7e821e2-1bcb-43f9-a7c9-ecd3052a399c)


#### Volume vs Price analysis
![image](https://github.com/user-attachments/assets/700c5b25-5409-4b72-a2d8-187dbed6fd26)


#### 15 minutes moving average
![image](https://github.com/user-attachments/assets/51aa316b-8fbd-4be3-b283-d0b311006988)


#### Correlation heatmap
![image](https://github.com/user-attachments/assets/90addfee-060c-4238-967f-d8a38177e2d5)


#### Percent growth in 90 days for each sector
![image](https://github.com/user-attachments/assets/c2e1f6d4-296b-41e5-9768-6d7271b585a2)


### Results/Findings

After careful analysis, the results are as follows:
1. The top 3 cryptocurrencies with the highest market capitalization are Bitcoin with 63.3%, followed by Ethereum with 9.01% and Tether USDT with 4.53%.
2. The top 3 cryptocurrencies with the largest 24h trading volume are Tether USDT, Bitcoin and Dai respectively.
3. Cryptocurrencies like Trump Dinner, ShibaBitcoin and Huobi Token experienced the largest gains within the last 90 days while other tokens such as First Digital USD, Celo Dollar and Ethena USDe experienced the least gains.
4. Low R2 value shows that trading volume is not a strong predictor of price, other factors like market cap, supply, utility, speculation play much larger roles.
5. Bitcoin has a strong positive correlation with Solana, Monero and Sui while Ethereum has a strong positive correlation with Aave, Dogecoin and BNB. AiAkita shows a negative correlation with most coins.
6. Base-ecosystem sector experienced the largest growth of 16,121% in 90 days, followed by memes sector of 14,116% and bnb-chain-ecosystem of 4,555%.
7. Trump Dinner, Mint Token and Launch Coin on Believe are the top 3 performing coins that were only added in the last 180 days.


### Limitations






