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

EDA is used to summarize the sales data and allows us gain a deeper understanding of the dataset retrieved from the CoinMarketCap API. It answers key questions such as:

 - Which cryptocurrencies are leading in terms of market capitalization and trading volume?

 - How do price movements vary across different time frames?

 - Which coins have shown the highest volatility or consistent growth?

 - Are there correlations between volume, market cap, and price changes?

 - How does the performance of altcoins compare to that of major coins like Bitcoin and Ethereum?

 - Are there emerging coins or sectors gaining traction in the market?


### Data Analysis

Cumulative sum of weekly sales for each store:

     SELECT Store, Date, Weekly_Sales,
	    SUM(Weekly_Sales) OVER(
	    PARTITION BY Store
	    ORDER BY Date) AS Cumulative_Weekly_Sales
     FROM walmart_sales
     ORDER BY Store, Date;





### Data Visualization





### Results/Findings

After careful analysis, the results are as follows:

  


### Recommendations

Based on analysis above, here are some recommended actions to take:





### Limitations


