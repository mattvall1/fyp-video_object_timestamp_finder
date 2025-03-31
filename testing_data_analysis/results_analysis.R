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

}

