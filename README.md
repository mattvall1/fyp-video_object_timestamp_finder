# COMP1682 Final Year Project
## Retrieving objects from short videos using text descriptions
### University of Greenwich - Computer Science BSc

**Note:** The full paper will be included with this repository, after the final submission has been graded. This is to avoid plagiarism issues for markers.

## Abstract (from poster presentation)
This project investigates retrieving objects from 
short video clips using text descriptions generated 
via an image captioning model. By exploring models 
such as CLIP, BLIP, and Florence2, this project aims 
to develop a user-friendly software package that 
pinpoints exact timestamps where specified objects 
appear in a video. The approach involves analysing 
image captioning algorithms, optimising 
performance via a key framing technique, and 
integrating search and language processing. Results 
show effective timestamp retrieval despite 
computational challenges, demonstrating feasibility 
on consumer-grade hardware and paving the way 
for future improvements.

## Main program running instructions
**Note:** This program has been developed (almost) entirely on macOS 15+, I cannot guarantee that it will run on other operating systems. Python 3.12.* must be used.
1. Navigate to the `app/` directory and open a terminal.
2. Run `pip install -r requirements.txt` to install the required packages.
   1. Retrieve all NLTK files: `python -m nltk.downloader all`
3. Run `python main.py` to start the program.

## References
```bibtex
@misc{sidorov2020textcapsdatasetimagecaptioning,
    title={TextCaps: a Dataset for Image Captioning with Reading Comprehension}, 
    author={Oleksii Sidorov and Ronghang Hu and Marcus Rohrbach and Amanpreet Singh},
    year={2020},
    eprint={2003.12462},
    archivePrefix={arXiv},
    primaryClass={cs.CV},
    url={https://arxiv.org/abs/2003.12462}, 
}
@inproceedings{Ghatak2016KEYFRAMEEU,
    title={KEY-FRAME EXTRACTION USING THRESHOLD TECHNIQUE},
    author={Sanjoy Ghatak},
    year={2016},
    url={https://api.semanticscholar.org/CorpusID:34413484}
}
@misc{xiao2023florence2advancingunifiedrepresentation,
    title={Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks}, 
    author={Bin Xiao and Haiping Wu and Weijian Xu and Xiyang Dai and Houdong Hu and Yumao Lu and Michael Zeng and Ce Liu and Lu Yuan},
    year={2023},
    eprint={2311.06242},
    archivePrefix={arXiv},
    primaryClass={cs.CV},
    url={https://arxiv.org/abs/2311.06242}, 
}
```

