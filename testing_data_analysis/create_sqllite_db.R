# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Create SQLite database from CSV file for easy querying and analysis in R.

# Load the required libraries
library(RSQLite)
library(readr)

# Set paths
csv_file_path <- "model_results.csv"
sqlite_db_path <- "model_results.db"

# Read the CSV file into a data frame
results_csv_df <- read_csv(csv_file_path)

# Convert headings to lowercase
results_csv_df <- setNames(results_csv_df, tolower(names(results_csv_df)))

# Connect to the SQLite database (it will be created if it doesn't exist)
results_db <- dbConnect(SQLite(), dbname = sqlite_db_path)

# Automatically write the data frame to the SQLite database. CSV headers will be used as column names.
dbWriteTable(results_db, "results", results_csv_df, overwrite = TRUE)

# Close the database connection
dbDisconnect(results_db)
