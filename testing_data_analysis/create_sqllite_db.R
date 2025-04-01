# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Create SQLite database from CSV file for easy querying and analysis in R.

# Load the required libraries
library(RSQLite)
library(readr)

# Set paths
csv_file_paths <- list("results/auto_results.csv",
					   "results/failed_urls.csv",
					   "results/other_errors.csv")
sqlite_db_path <- "testing_results.db"

# Connect to the SQLite database (it will be created if it doesn't exist)
results_db <- dbConnect(SQLite(), dbname = sqlite_db_path)

# Loop through each CSV file path and write it to the SQLite database
for (csv_file_path in csv_file_paths) {
  # Read the CSV file into a data frame
  results_csv_df <- read_csv(csv_file_path)

  # Convert headings to lowercase (and replace spaces with underscores)
  results_csv_df <- setNames(results_csv_df, gsub(" ", "_", tolower(names(results_csv_df))))

  # Get the table name from the CSV file name
  table_name <- gsub("\\.csv$", "", basename(csv_file_path))

  # Automatically write the data frame to the SQLite database. CSV headers will be used as column names.
  dbWriteTable(results_db, table_name, results_csv_df, overwrite = TRUE)
}

# Close the database connection
dbDisconnect(results_db)
