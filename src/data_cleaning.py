"""
Data Cleaning and Preprocessing for Web Scraped Book Data
Task 2: Clean and preprocess raw dataset for analysis
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataCleaner:
    """Data cleaning and preprocessing class for book data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def load_data(self, csv_path: str) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded data from {csv_path}: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset"""
        logger.info("=== HANDLING MISSING VALUES ===")
        
        df_clean = df.copy()
        
        # Check for missing values
        missing_before = df_clean.isnull().sum().sum()
        logger.info(f"Total missing values before handling: {missing_before}")
        
        # Handle specific columns
        if 'description' in df_clean.columns:
            df_clean['description'] = df_clean['description'].fillna('No description available')
            logger.info("Filled missing descriptions")
        
        if 'rating' in df_clean.columns:
            mode_rating = df_clean['rating'].mode()[0] if not df_clean['rating'].mode().empty else 'No rating'
            df_clean['rating'] = df_clean['rating'].fillna(mode_rating)
            logger.info(f"Filled missing ratings with mode: {mode_rating}")
        
        # For numerical columns, fill with median
        numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df_clean[col].isnull().sum() > 0:
                median_val = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(median_val)
                logger.info(f"Filled missing values in {col} with median: {median_val}")
        
        # For categorical columns, fill with mode
        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col != 'description' and df_clean[col].isnull().sum() > 0:
                mode_val = df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown'
                df_clean[col] = df_clean[col].fillna(mode_val)
                logger.info(f"Filled missing values in {col} with mode: {mode_val}")
        
        missing_after = df_clean.isnull().sum().sum()
        logger.info(f"Total missing values after handling: {missing_after}")
        
        return df_clean
    
    def detect_outliers(self, df: pd.DataFrame) -> dict:
        """Detect outliers in numerical columns using IQR method"""
        logger.info("=== DETECTING OUTLIERS ===")
        
        outliers = {}
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            
            if outlier_count > 0:
                outliers[col] = {
                    'count': outlier_count,
                    'percentage': (outlier_count / len(df)) * 100,
                    'indices': df[outlier_mask].index.tolist()
                }
                logger.info(f"{col}: {outlier_count} outliers ({outlier_count/len(df)*100:.2f}%)")
        
        # Save outliers info
        with open('data/preprocessed/outliers_info.json', 'w') as f:
            json.dump(outliers, f, indent=4)
        
        return outliers
    
    def remove_outliers(self, df: pd.DataFrame, outliers: dict) -> pd.DataFrame:
        """Remove outliers from the dataset"""
        logger.info("=== REMOVING OUTLIERS ===")
        
        df_clean = df.copy()
        indices_to_remove = set()
        
        for col, info in outliers.items():
            indices_to_remove.update(info['indices'])
        
        before_count = len(df_clean)
        df_clean = df_clean.drop(list(indices_to_remove))
        after_count = len(df_clean)
        
        logger.info(f"Removed {before_count - after_count} rows containing outliers")
        logger.info(f"Dataset size after outlier removal: {after_count} rows")
        
        return df_clean
    
    def encode_categorical_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert categorical variables into numerical format"""
        logger.info("=== ENCODING CATEGORICAL VARIABLES ===")
        
        df_encoded = df.copy()
        
        # Label encoding for ordinal variables
        if 'rating' in df_encoded.columns:
            rating_mapping = {
                'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5,
                'No rating': 0
            }
            df_encoded['rating_encoded'] = df_encoded['rating'].map(rating_mapping).fillna(0)
            logger.info("Encoded rating column")
        
        # One-hot encoding for nominal variables
        categorical_cols = df_encoded.select_dtypes(include=['object']).columns
        categorical_cols = [col for col in categorical_cols if col not in ['title', 'description', 'url', 'rating']]
        
        for col in categorical_cols:
            if df_encoded[col].nunique() <= 10:  # Only encode if reasonable number of categories
                dummies = pd.get_dummies(df_encoded[col], prefix=col, drop_first=True)
                df_encoded = pd.concat([df_encoded, dummies], axis=1)
                logger.info(f"One-hot encoded {col} ({df_encoded[col].nunique()} categories)")
        
        return df_encoded
    
    def normalize_numerical_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize or standardize numerical data"""
        logger.info("=== NORMALIZING NUMERICAL DATA ===")
        
        df_normalized = df.copy()
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        # Remove columns that were just created from encoding
        numerical_cols = [col for col in numerical_cols if not col.endswith('_encoded') and not any(x in col for x in ['_', 'price'])]
        
        for col in numerical_cols:
            if col in df_normalized.columns and df_normalized[col].nunique() > 1:
                # Standard scaling (z-score normalization)
                df_normalized[col + '_standardized'] = (df_normalized[col] - df_normalized[col].mean()) / df_normalized[col].std()
                # Min-max scaling
                df_normalized[col + '_normalized'] = (df_normalized[col] - df_normalized[col].min()) / (df_normalized[col].max() - df_normalized[col].min())
                logger.info(f"Normalized {col}")
        
        return df_normalized
    
    def save_cleaned_data(self, df: pd.DataFrame, filename: str) -> None:
        """Save cleaned data to file"""
        try:
            if filename.endswith('.csv'):
                df.to_csv(filename, index=False)
            elif filename.endswith('.json'):
                df.to_json(filename, orient='records', indent=4)
            
            logger.info(f"Cleaned data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving cleaned data: {e}")

def main():
    """Main function to run data cleaning pipeline"""
    cleaner = DataCleaner()
    
    # Load raw data
    logger.info("Starting data cleaning process...")
    df = cleaner.load_data('data/raw/scraped_books.csv')
    
    if df is not None:
        # Handle missing values
        df_clean = cleaner.handle_missing_values(df)
        
        # Detect outliers
        outliers = cleaner.detect_outliers(df_clean)
        
        # Remove outliers
        df_clean = cleaner.remove_outliers(df_clean, outliers)
        
        # Encode categorical variables
        df_encoded = cleaner.encode_categorical_variables(df_clean)
        
        # Normalize numerical data
        df_normalized = cleaner.normalize_numerical_data(df_encoded)
        
        # Save cleaned data
        cleaner.save_cleaned_data(df_normalized, 'data/preprocessed/cleaned_books.csv')
        cleaner.save_cleaned_data(df_normalized, 'data/preprocessed/cleaned_books.json')
        
        logger.info("Data cleaning completed successfully!")
    else:
        logger.error("Failed to load data. Please check the file paths.")

if __name__ == "__main__":
    main()