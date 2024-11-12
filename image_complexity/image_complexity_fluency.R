# File to test the complexity of an image

# Load the necessary libraries
library(imagefluency)

# Load the image
testing_image <- img_read('testing_images/many_cats.jpg')

# Check complexity
img_complexity(testing_image, 'jpg')
