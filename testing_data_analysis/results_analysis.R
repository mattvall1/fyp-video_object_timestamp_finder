# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Analyse the data from the testing of captioning algorithms

# Load the required libraries
library(data.table)
library(RSQLite)

# Set DB path
sqlite_db_path <- "model_results.db"

# Open SQLLite connection
db_conn <- dbConnect(RSQLite::SQLite(), sqlite_db_path)

# We know there is only one table in the database
# First, get some statistics about the table
summary <- dbGetQuery(db_conn, "SELECT COUNT(*) AS total_rows, MAX(timestamp) - MIN(timestamp) AS total_time_taken_s FROM results")

# Create a summary table
summary_table <- data.table(
  TotalRows = summary$total_rows,
  TimeTakenHours = summary$total_time_taken_s/60/60 # Convert seconds to hours
)

# Print the summary table
print(summary_table)
