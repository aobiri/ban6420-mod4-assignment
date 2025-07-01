import zipfile
import os
import pandas as pd
from datetime import date, datetime
import shutil
import matplotlib.pyplot as plt


# Function to unzip the file
def unzip_and_rename(zfn, ofn):
    print(f"Unzipping {zfn} to {ofn}...")
    with zipfile.ZipFile(zfn, 'r') as zip_ref:
        try:
            if os.path.exists(ofn) and os.path.isdir(ofn):
                # Loop through all items inside the folder
                for item in os.listdir(ofn):
                    item_path = os.path.join(ofn, item)
                    # Remove files
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    # Remove subfolders
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
            else:
                os.makedirs(ofn)
            # Extract all files from the Zip to the output folder
            zip_ref.extractall(ofn)
        except Exception as e:
            print(f"Error extracting zip file: {e}")
            exit(1)

# Function to clean the data
def clean_data(file_path):
    print("================ DATA CLEANING ========================")
    print(f"====== Cleaning data from {file_path}...")

    # Load the CSV file
    df = pd.read_csv(file_path)

    # Check if the file is empty
    print(f"Columns that have missing values:\n {df.isnull().any()}") # Columns that have missing values
    print(f"\n Summary of Null Values in Each Column:\n {df.isnull().sum()}")  # Count of null values in each column

    ### Data Cleaning Process
    #df = df.dropna(subset=['type', 'title', 'director']) # Remove records with no type, title, and director
    # df.dropna(inplace=True)  # Remove rows with missing values
    df = df.dropna(how='all')  # Remove rows where all elements are NaN
    df.columns = [col.strip() for col in df.columns]  # Strip whitespace from column names
    # Fill columns with missing values
    df.fillna({
        'director': 'Unknown',
        'cast': 'Unknown',
        'country': 'Unknown',
        'date_added': date.today().strftime("%B %d, %Y"), # Fill with today's date
        'rating': df['rating'].mode()[0],  # Fill with the most common rating
    }, inplace=True)

    # Save the cleaned CSV back to a file
    cleaned_file_path = file_path.replace('.csv', '_cleaned.csv')
    df.to_csv(cleaned_file_path, index=False)
    print(f"====== Cleaned CSV saved as -> {cleaned_file_path}")

# This function can be used for further data exploration and analysis
def data_exploration(file_path):
    print("\n================ DATA EXPLORATION ========================\n")
    try:
        df = pd.read_csv(file_path)
        # Basic exploration
        #print(f'\n First few rows: \n {df.head()}')             # View first few rows
        print(f"\n Data Types: \n {df.info()}")             # Data types, nulls
        print(f"Summary Stats: \n {df.describe()}")         # Summary stats
        print(f"\n Movie Types Summary: \n{df['type'].value_counts()}")  # Frequency of movie types
        #print(df['Salary'].mean())   # Average salary
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        exit(1) # Exit code if there is no file or if it is not readable

# Function to create visualization for most watched genres
def visualize_most_watched_genres(file_path):
    try:
        df = pd.read_csv(file_path)
        genre_counts = df['type'].value_counts()  # Count occurrences of each genre
        plt.figure(figsize=(10, 6))
        genre_counts.plot(kind='bar', color='skyblue')
        plt.title('Most Watched Genres')
        plt.xlabel('Genres')
        plt.ylabel('Number of Movies/Shows')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error visualizing data from {file_path}: {e}")

# Function to create visualization for ratings distribution
def visualize_ratings_distribution(file_path):
    try:
        df = pd.read_csv(file_path)
        plt.figure(figsize=(10, 6))
        df['rating'].value_counts().sort_index().plot(kind='bar', color='lightgreen')
        plt.title('Ratings Distribution')
        plt.xlabel('Ratings')
        plt.ylabel('Number of Movies/Shows')
        plt.xticks(rotation=45)
        plt.tight_layout()
        #plt.savefig("ratings_dist.png") # Save the plot as an image for later use
        plt.show()
    except Exception as e:
        print(f"Error visualizing ratings from {file_path}: {e}")


if __name__ == '__main__':
    # ------- DATA PREPARATION -----------
    print("\n================ DATA PREPARATION ========================\n")
    print("Starting Netflix Data Processing...")
    # Initialize the variables for the zip file and output folder
    zip_file_name = 'netflix_data.zip'
    output_folder_name = 'Netflix_shows_movies'
    # Check if the zip file exists
    if not os.path.exists(zip_file_name):
        print(f"Error: {zip_file_name} does not exist.")
        exit(1) # No need to continue the script if the zip file is not found
    # Call the function to unzip and rename the file
    unzip_and_rename(zip_file_name, output_folder_name)
    print(f"Unzipped {zip_file_name} to {output_folder_name}")

    # ------- DATA CLEANING -----------
    for file in os.listdir(output_folder_name):
        if file.endswith('.csv'):
            clean_data(os.path.join(output_folder_name, file))

    # ------- DATA EXPLORATION -----------
    for file in os.listdir(output_folder_name):
        if file.endswith('_cleaned.csv'):
            data_exploration(os.path.join(output_folder_name, file))

    # ------- DATA VISUALIZATION -----------
    print("\n================ DATA VISUALIZATION ========================\n")
    for file in os.listdir(output_folder_name):
        if file.endswith('_cleaned.csv'):
            visualize_most_watched_genres(os.path.join(output_folder_name, file))
            visualize_ratings_distribution(os.path.join(output_folder_name, file))