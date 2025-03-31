# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Analyse the data from the testing of captioning algorithms

# Load the required libraries
library(data.table)
library(RSQLite)

# Set DB path
sqlite_db_path <- "testing_results.db"

# Open SQLLite connection
db_conn <- dbConnect(RSQLite::SQLite(), sqlite_db_path)

# First, get some statistics about the table
results_summary <- dbGetQuery(db_conn, "SELECT COUNT(*) AS total_rows, MAX(timestamp) - MIN(timestamp) AS total_time_taken_s FROM model_results")

# Get BLEU scores for each model
bleu_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS bleu FROM model_results WHERE metric = 'BLEU' GROUP BY model")
print(bleu_scores)

# Get METEOR scores for each model
meteor_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS meteor FROM model_results WHERE metric = 'METEOR' GROUP BY model")
print(meteor_scores)

# Get ROUGE-1 scores for each model
rouge_1_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS rouge_1 FROM model_results WHERE metric = 'ROUGE-1' GROUP BY model")
print(rouge_1_scores)

# Get ROUGE-2 scores for each model
rouge_2_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS rouge_2 FROM model_results WHERE metric = 'ROUGE-2' GROUP BY model")
print(rouge_2_scores)

# Get ROUGE-L scores for each model
rouge_l_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS rouge_l FROM model_results WHERE metric = 'ROUGE-L' GROUP BY model")
print(rouge_l_scores)

# Get count of failed URLs
failed_urls <- dbGetQuery(db_conn, "SELECT COUNT(url) AS failed_urls FROM failed_urls")

# Get count of other errors
other_errors <- dbGetQuery(db_conn, "SELECT COUNT(timestamp) AS other_errors FROM other_errors")

# Close the database connection as we now have all the data we need
dbDisconnect(db_conn)

# Create a summary table
summary_table <- data.table(
  TotalRows = results_summary$total_rows,
  MissingURLs = failed_urls$failed_urls,
  OtherErrors = other_errors$other_errors,
  TimeTakenHours = results_summary$total_time_taken_s/60/60 # Convert seconds to hours
)

# Print summary table
print(summary_table)

