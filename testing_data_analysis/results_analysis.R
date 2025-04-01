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

# First, get some statistics about the results table
results_summary <- dbGetQuery(db_conn, "SELECT COUNT(*) AS total_rows, MAX(timestamp) - MIN(timestamp) AS total_time_taken_s FROM auto_results")

# Import the original summary table from the DB (some of this will match the results_summary table)
summary <- dbGetQuery(db_conn, "SELECT \"total_failed/non-existent_images\" AS total_failed, total_attempted_images FROM summary")

# Get BLEU scores for each model
bleu_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS bleu FROM auto_results WHERE metric = 'BLEU' GROUP BY model")
print(bleu_scores)

# Get METEOR scores for each model
meteor_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS meteor FROM auto_results WHERE metric = 'METEOR' GROUP BY model")
print(meteor_scores)

# Get ROUGE-1 scores for each model
rouge_1_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS rouge_1 FROM auto_results WHERE metric = 'ROUGE-1' GROUP BY model")
print(rouge_1_scores)

# Get ROUGE-2 scores for each model
rouge_2_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS rouge_2 FROM auto_results WHERE metric = 'ROUGE-2' GROUP BY model")
print(rouge_2_scores)

# Get ROUGE-L scores for each model
rouge_l_scores <- dbGetQuery(db_conn, "SELECT model, AVG(score) AS rouge_l FROM auto_results WHERE metric = 'ROUGE-L' GROUP BY model")
print(rouge_l_scores)

# Get count of failed URLs
failed_urls <- dbGetQuery(db_conn, "SELECT COUNT(url) AS failed_urls FROM failed_urls")

# Get count of other errors
other_errors <- dbGetQuery(db_conn, "SELECT COUNT(timestamp) AS other_errors FROM other_errors")

# Close the database connection as we now have all the data we need
dbDisconnect(db_conn)

# Create a summary table
summary_table <- data.table(
  TotalResults = results_summary$total_rows,
  TimeTakenHours = round(results_summary$total_time_taken_s/60/60, 2), # Convert seconds to hours
  TotalImagesAttempted = summary$total_attempted_images,
  TotalImagesAnalysed = summary$total_attempted_images - summary$total_failed,
  MissingImages = failed_urls$failed_urls,
  PercentageImagesFailed = round((summary$total_failed / summary$total_attempted_images) * 100, 2),
  OtherErrors = other_errors$other_errors
)

# Combine all metric scores into a single table
bleu_table <- data.table(model = bleu_scores$model, metric = "BLEU", score = round(bleu_scores$bleu, 4))
meteor_table <- data.table(model = meteor_scores$model, metric = "METEOR", score = round(meteor_scores$meteor, 4))
rouge1_table <- data.table(model = rouge_1_scores$model, metric = "ROUGE-1", score = round(rouge_1_scores$rouge_1, 4))
rouge2_table <- data.table(model = rouge_2_scores$model, metric = "ROUGE-2", score = round(rouge_2_scores$rouge_2, 4))
rougeL_table <- data.table(model = rouge_l_scores$model, metric = "ROUGE-L", score = round(rouge_l_scores$rouge_l, 4))

# Combine all metric dataframes into one using rbind
all_metrics <- rbindlist(list(bleu_table, meteor_table, rouge1_table, rouge2_table, rougeL_table))

# Order the combined table by model and metric
all_metrics <- all_metrics[order(model, metric)]

# Print tables
print(summary_table)
print(all_metrics)

# Save both tables to CSV files
fwrite(summary_table, "output/summary_table.csv")
fwrite(all_metrics, "output/all_metrics.csv")

# Create a pie chart of the summary (save as PNG)
png("output/summary_pie_chart.png", width = 1000, height = 1000)
pie(
  c(summary_table$TotalImagesAnalysed, summary_table$MissingImages),
  labels = c("Valid Images", "Missing Images"),
  main = "Summary of Testing Results",
  col = c("#5DE2E7", "#DF0101"),
  cex = 1.5, # Label size
  cex.main = 3 # Title size
)
dev.off()


