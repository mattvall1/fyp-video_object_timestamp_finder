-- © 2025 Matthew Vallance. All rights reserved.
-- COMP1682 Final Year Project.
-- Purpose: Simple SQL queries to check connection (when using DataSpell IDE) and to test the database.

-- Basic statistics about the table
SELECT COUNT(*) AS total_rows, MAX(timestamp) - MIN(timestamp) AS total_time_taken_s FROM model_results;

-- Get BLEU scores for each model
SELECT model, AVG(score) AS bleu FROM model_results WHERE metric = 'BLEU' GROUP BY model;

-- Get METEOR scores for each model
SELECT model, AVG(score) AS meteor FROM model_results WHERE metric = 'METEOR' GROUP BY model;

-- Get ROUGE-1 scores for each model
SELECT model, AVG(score) AS rouge_1 FROM model_results WHERE metric = 'ROUGE-1' GROUP BY model;

-- Get ROUGE-2 scores for each model
SELECT model, AVG(score) AS rouge_2 FROM model_results WHERE metric = 'ROUGE-2' GROUP BY model;

-- Get ROUGE-L scores for each model
SELECT model, AVG(score) AS rouge_l FROM model_results WHERE metric = 'ROUGE-L' GROUP BY model;

-- Get count of failed URLs
SELECT COUNT(url) AS failed_urls FROM failed_urls;

-- Get count of other errors
SELECT COUNT(timestamp) AS other_errors FROM other_errors;