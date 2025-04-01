# Notes on testing_data/ directory
The testing_data/ directory must be created and contains the datasets used for testing the model. Each dataset is stored in a separate subdirectory.

## Pre-requisites
Imnstall: 
Install: `pip install aac-metrics`

## Directory structure
The various files should be retrieved according to the list in the next section.
```
testing_data/
├── conceptual_captions/
│   └── CC_Validate.tsv
├── text_caps/
│   ├── TextCaps_0.1_val.json (15,508 captions)
│   ├── TextCaps_0.1_train.json (109,765 captions)
└── dir/
    ├── 
    ├── 
    └── 
```

## Where to find the datasets
- [Conceptual Captions Download](https://ai.google.com/research/ConceptualCaptions/download) - 'Validation split' == 'CC_Validate.tsv'
- [TextCaps Download](https://textvqa.org/textcaps/download/)
