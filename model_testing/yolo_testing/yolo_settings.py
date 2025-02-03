# © 2024 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Update YOLO settings, such as the directory to save runs to.

from ultralytics import settings

# Print old settings
print(settings)

# Update directories (Windows)
settings.update({"datasets_dir": "E:\\datasets",  
                 "runs_dir": "E:\\yr3_fyp_object_detection\\model_testing\\detection_output\\runs", 
                 "weights_dir": "E:\\yr3_fyp_object_detection\\model_testing\\detection_output\\runs"
                })

# Print new settings
print(settings)

