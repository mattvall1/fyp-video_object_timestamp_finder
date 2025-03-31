-- © 2025 Matthew Vallance. All rights reserved.
-- COMP1682 Final Year Project.
-- Purpose: Simple SQL queries to check connection

-- Get the average score for the 'BLEU' metric for OpenCLIP model
SELECT AVG(score) FROM results WHERE Metric == 'BLEU' AND Model == 'OpenCLIP';


