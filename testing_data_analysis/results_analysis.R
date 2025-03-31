# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Analyse the data from the testing of captioning algorithms

# Load the required libraries
library(data.table)

# Set the results path
results_path <- "model_results.csv"

# Read the results from the CSV file
results <- data.table::fread(results_path, data.table = FALSE)

# Check if data is loaded correctly
if(!is.null(results)) {
  cat("Data loaded successfully\n")

  # Display the total number of rows and columns
  cat("Total rows:", nrow(results), "\n")
  cat("Total columns:", ncol(results), "\n")

} else {
  cat("Failed to load data\n")
  stop("Data loading error")
}

# Extract and sum BLEU scores for OpenCLIP model
if("model" %in% colnames(results) && "metric" %in% colnames(results) && "score" %in% colnames(results)) {
  # Filter for OpenCLIP model and BLEU metric
  openclip_bleu <- results[results$model == "OpenCLIP" & results$metric == "BLEU", ]

  # Calculate total BLEU score
  total_bleu_score <- sum(openclip_bleu$score, na.rm = TRUE)

  # Display results
  cat("Total OpenCLIP BLEU score:", total_bleu_score, "\n")
  cat("Number of OpenCLIP BLEU scores:", nrow(openclip_bleu), "\n")
  cat("Average OpenCLIP BLEU score:", total_bleu_score / nrow(openclip_bleu), "\n")
} else {
  cat("Required columns not found in the dataset\n")
}
