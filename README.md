# web-scraping

Data Collection and Web Scraping

## 📌 Overview

This project demonstrates a complete data science pipeline from web scraping to exploratory data analysis. It collects book data from books.toscrape.com, cleans and preprocesses the data, and performs comprehensive exploratory analysis to uncover insights.

## 📂 Project Structure

```bash
web-scraping/
├── .venv/                         # Virtual environment
├── data/
│   ├── raw/                       # Raw scraped data
│   │   ├── scraped_books.csv
│   │   └── scraped_books.json
│   └── preprocessed/              # Cleaned and processed data
│       ├── cleaned_books.csv
│       ├── cleaned_books.json
│       └── outliers_info.json
├── outputs/                       # Visualization outputs
│   ├── correlation_matrix.png
│   ├── price_analysis.png
│   ├── rating_distribution.png
│   ├── availability_pie.png
│   ├── price_vs_rating.png
│   └── price_vs_availability.png
├── notebooks/                     # Jupyter notebooks
│   └── eda_analysis.ipynb         # Task 3: EDA notebook
├── src/
│   ├── web_scraper.py             # Task 1: Web scraping script
│   └── data_cleaning.py           # Task 2: Data cleaning script
├── logs/                          # Application logs
│   └── scraping.log
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## 🚀 Project Tasks

## Task 1: Data Collection and Web Scraping

### Features

- **Robust Web Scraping**: Extracts book information including title, price, rating, availability, and description
- **Pagination Handling**: Automatically navigates through multiple pages
- **Error Handling**: Comprehensive error handling and logging
- **Respectful Scraping**: Includes delays between requests to avoid overwhelming the target website
- **Multiple Output Formats**: Saves data in both CSV and JSON formats

### Output

- data/raw/scraped_books.csv - Raw data in CSV format

- data/raw/scraped_books.json - Raw data in JSON format

## Task 2: Data Cleaning and Preprocessing

### Description: Clean and preprocess the raw dataset to make it suitable for analysis.

### Objectives Achieved:

✅ Missing Data Handling: Imputed missing values using appropriate strategies

✅ Outlier Detection: Identified and removed outliers using IQR method

✅ Categorical Encoding: Converted categorical variables using label encoding and one-hot encoding

✅ Data Normalization: Standardized numerical features using z-score and min-max scaling

### Output:

- data/preprocessed/cleaned_books.csv - Cleaned data in CSV format

- data/preprocessed/cleaned_books.json - Cleaned data in JSON format

- data/preprocessed/outliers_info.json - Outlier analysis report

## Task 3: Exploratory Data Analysis (EDA)

### Description: Perform comprehensive exploratory data analysis to understand the underlying structure and trends in the data.

### Objectives Achieved:

✅ Summary Statistics: Computed mean, median, variance, and distribution metrics

✅ Data Visualization: Created histograms, scatter plots, box plots, and correlation matrices

✅ Correlation Analysis: Identified relationships between numerical features

✅ Insight Report: Generated comprehensive summary of key findings

### Visualizations Created:

- Price Distribution - Histogram and box plot of book prices

- Rating Distribution - Bar chart of book ratings frequency

- Availability Analysis - Pie chart of stock availability

- Price vs Rating - Comparative analysis of pricing by rating

- Correlation Matrix - Heatmap of feature relationships

- Price vs Availability - Violin plot showing price distribution by stock status

## Output:

- outputs/ folder containing all visualizations

- Comprehensive insights report in the Jupyter notebook

## 🛠️ Setup & Installation

1.  **Clone the repository** (if applicable) or ensure you have the project structure locally.
2.  **Navigate to the project root directory** in your terminal.
3.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    ```
4.  **Activate the virtual environment**:
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
5.  **Install dependencies**:

    ```bash pip install -r requirements.txt

    ```

## 📊 Usage

1. Run Task 1: Web Scraping

   ```bash python src/web_scraper.py

   ```

2. Run Task 2: Data Cleaning

   ```bash python src/data_cleaning.py

   ```

3. Run Task 3: Exploratory Data Analysis

   ```bash jupyter notebook notebooks/eda_analysis.ipynb

   ```

## 🔧 Technologies Used

- Web Scraping: BeautifulSoup4, Requests

- Data Processing: Pandas, NumPy

- Data Cleaning: Scikit-learn

- Visualization: Matplotlib, Seaborn

- Analysis: SciPy, Jupyter Notebook

## 🎯 Next Steps

This cleaned and analyzed dataset is now ready for:

- Machine learning model development

- Price prediction algorithms

- Recommendation systems

- Inventory optimization analysis
