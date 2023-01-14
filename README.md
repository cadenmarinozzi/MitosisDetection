# MitosisDetection

A CNN and generation algorithm to calculate the mitotic index of a set of cell data

# Installation

## Local Installation

```bash
# Download the repository to your local machine:
git clone https://github.com/nekumelon/MitosisDetection.git

# Change directory to the repository:
cd MitosisDetection

# Install the requirements:
pip install -r requirements.txt
```

# Usage

## Local Usage

```bash
# Generate the training data:
python generate.py <config file>

# Run the CNN:
python main.py <config file>
```

# Configuration

A configuration file is used to configure the program. The default configuration file is located at `config.json`. The configuration file is a JSON file, and the following options are available:

```json
{
  "generate": { # Configuration for the generation of training data
    "nImages": 1000, # The number of images to generate
    "imgResolution": [100, 100], # The resolution of the images
    "outputPath": "data", # The path to the output directory
    "labelsPath": "data/labels.txt", # The path to the labels file
    "imageFormat": "png", # The format of the images
    "blurRadius": 2, # The radius of the gaussian blurapplied to the images
    "percentInMitois": 0.5, # The percentage of images that should be in mitosis (between 0 and 1)
    "nonUniformnessMinMax": [0, 20], # The minimum and maximum values for the non-uniformness of the cells. The higher the value, the less uniform the shape of the cells will be
    "shape": "random", # The shape of the cells
    "minChromosomeLength": 3, # The minimum length of the chromosomes
    "maxChromosomeLengthDivisor": 5, # The maximum length of the chromosomes is the image width divided by this value
    "minChromosomeWidth": 2, # The minimum width of the chromosomes
    "maxChromosomeWidthDivisor": 20, # The maximum width of the chromosomes is the image width divided by this value
    "minNPoints": 0, # The minimum number of points in the chromosomes
    "maxNPointsDivisor": 20, # The maximum number of points in the chromosomes is the image width divided by this value
    "minNChromosomes": 0, # The minimum number of chromosomes
    "maxNChromosomesDivisor": 2, # The maximum number of chromosomes is the image width divided by this value
    "verbose": true # Whether or not to print the progress of the generation
  },
  "train": {
    "inputPath": "data", # The path to the input directory
    "labelsPath": "data/labels.txt", # The path to the labels file
    "imageFormat": "png", # The format of the images
    "imgResolution": [100, 100], # The resolution of the images
    "nEpochs": 20, # The number of epochs to train for, higher values will result in more accurate results, but will take longer to train
    "testPath": "data" # The path to the test directory
  }
}
```

# License

You can view the license [here](LICENSE)

# Author

Created by [@nekumelon](https://github.com/nekumelon)
