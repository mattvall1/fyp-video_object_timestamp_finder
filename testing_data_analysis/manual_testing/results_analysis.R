# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Analyse the data from the manual testing of captioning algorithms

# Load the required libraries
library(data.table)
library(ggplot2)

# First import the CSV data into a data frame
results_df <- fread("results.csv")

# Split the data into separate data frames for each model
results_openclip <- results_df[model_name == "OpenCLIP"]
results_blip <- results_df[model_name == "SalesForceBLIP"]
results_florence <- results_df[model_name == "Florence2"]

# Print the data frames to check the data
print(results_openclip)
print(results_blip)
print(results_florence)



# Average the time_taken for each model (+ Save to CSV) - To compare speedd of the models
avg_time_df <- data.frame(
  model_name = c("OpenCLIP", "SalesForceBLIP", "Florence2"),
  avg_time = c(round(mean(results_openclip$time_taken), 2), round(mean(results_blip$time_taken), 2), round(mean(results_florence$time_taken), 2))
)
fwrite(avg_time_df, "output/avg_time_per_image_by_model.csv")

# Create bar plot
png("output/avg_time_per_image_by_model.png", width = 1000, height = 1000, res = 100)
ggplot(avg_time_df, aes(x = model_name, y = avg_time, fill = model_name)) +
  # First, create horizontal lines (Remember: this needs asjusting dependant on data entered)
  geom_hline(yintercept = seq(0, 5.5, by = 0.5), color = "#E2EAF2", linetype = "dashed") +
  # Add bars
  geom_bar(position='dodge', stat = "identity") +
  # Add nice colours
  scale_fill_manual(values = c("SalesForceBLIP" = "#6F87ED", "Florence2" = "#AA6FED", "OpenCLIP" = "#58D4EF")) +
  # Force y-axis to start at 0 and add a small margin
  scale_y_continuous(expand = expansion(mult = c(0, 0.05)), limits = c(0, NA)) +
  # Add labels
  labs(title = "Average Processing Time for Each Model", x = "Model Name", y = "Average Time (seconds)") +
  theme_classic() +
  # Theme adjustments
  theme(
   text = element_text(family = "Noto Serif"),
   legend.position = "none",
   plot.title = element_text(size = 24, face = "bold", hjust = 0.6),
   axis.title = element_text(size = 14),
  )
dev.off()



# Compare average caption length (+ Save to CSV) - To compare verbosity of the models
avg_caption_length_df <- data.frame(
  model_name = c("OpenCLIP", "SalesForceBLIP", "Florence2"),
  avg_caption_length = c(round(mean(nchar(results_openclip$model_output)), 2), round(mean(nchar(results_blip$model_output)), 2), round(mean(nchar(results_florence$model_output)), 2))
)
fwrite(avg_caption_length_df, "output/avg_caption_length_by_model.csv")

# Create bar plot
png("output/avg_caption_length_by_model.png", width = 1000, height = 1000, res = 100)
ggplot(avg_caption_length_df, aes(x = model_name, y = avg_caption_length, fill = model_name)) +
  # First, create horizontal lines (Remember: this needs asjusting dependant on data entered)
  geom_hline(yintercept = seq(0, 500, by = 25), color = "#E2EAF2", linetype = "dashed") +
  # Add bars
  geom_bar(position='dodge', stat = "identity") +
  # Add nice colours
  scale_fill_manual(values = c("SalesForceBLIP" = "#6F87ED", "Florence2" = "#AA6FED", "OpenCLIP" = "#58D4EF")) +
  # Force y-axis to start at 0 and add a small margin
  scale_y_continuous(expand = expansion(mult = c(0, 0.05)), limits = c(0, NA)) +
  # Add labels
  labs(title = "Average Caption Length for Each Model", x = "Model Name", y = "Average Caption Length (characters)") +
  theme_classic() +
  # Theme adjustments
  theme(
   text = element_text(family = "Noto Serif"),
   legend.position = "none",
   plot.title = element_text(size = 24, face = "bold", hjust = 0.6),
   axis.title = element_text(size = 14),
  )
dev.off()

