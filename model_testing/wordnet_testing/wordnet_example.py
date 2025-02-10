# Setup: pip install wn
#        python -m wn download oewn:2024  # The Open English WordNet 2024
# Docs: https://wn.readthedocs.io/en/latest/guides/basic.html
# wn package GitHub: https://github.com/goodmami/wn
# WordNet 2024: https://github.com/globalwordnet/english-wordnet

import wn
import os

# Define a Wordnet object
en = wn.Wordnet(os.path.join('model_testing', 'wordnet', 'english-wordnet-2024.xml'))

# Get the first synset for 'car' as a noun
car_ss = en.synsets('car', pos='n')[0]

# Print example
print(car_ss.definition())
