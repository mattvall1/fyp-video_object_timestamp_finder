from ultralytics import settings

# Print settings
print(settings)

# Update settings for Windows 11
# settings.update({"datasets_dir": "D:\\local_development\\datasets"})
settings.update({"datasets_dir": "D:\\local_development\\datasets"})
settings.update({"weights_dir": "D:\\local_development\\object_detection_outputs\\weights"})
settings.update({"runs_dir": "D:\\local_development\\object_detection_outputs\\runs"})

# Reset settings to default values
# settings.reset()