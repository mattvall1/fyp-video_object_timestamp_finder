# File to test the complexity of an image

# Load the necessary libraries
library(jpeg)

# Function to calculate the complexity of an image
image_complexity <- function(image_path) {
  # Read the image
  img <- readJPEG(image_path)

  # Convert the image to grayscale
  img_gray <- 0.2989 * img[,,1] + 0.5870 * img[,,2] + 0.1140 * img[,,3]

  # Calculate the complexity of the image
  complexity <- var(as.vector(img_gray))

  return(complexity)
}

image_complexity('testing_images/many_cats.jpg')

