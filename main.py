from PIL import Image
import tensorflow as tf, os, numpy as np, sys, json
from tensorflow.keras import layers, models
    
# Load the config file

configPath = 'config.json';

if (len(sys.argv) > 1):
    configPath = sys.argv[1];

if (not os.path.exists(configPath)):
    print(f'Config file \'{configPath}\' not found.');
    exit();

with open(configPath, 'r') as file:
    config = json.load(file)['train'];

labelsPath = config['labelsPath'] or 'data/labels.txt';

if (not os.path.exists(labelsPath)):
    print('Labels file not found.');
    exit();

inputPath = config['inputPath'] or 'data';

if (not os.path.exists(inputPath)):
    print('Input path not found.');
    exit();

testPath = config['testPath'] or 'data';

if (not os.path.exists(testPath)):
    print('Test path not found.');
    exit();

imageFormat = config['imageFormat'] or 'png';
imgResolution = config['imgResolution'] or [100, 100];

nEpochs = config['nEpochs'] or 20;

# Load training data
trainImages = [];
trainLabels = [];

# Load the labels
with open(labelsPath, 'r') as file:
    for line in file:
        # img = line.split(' ')[0];
        label = line.split(' ')[1][:-1];
        trainLabels.append(label == 'True' and [1] or [0]);

# Load the images
for file in os.listdir(inputPath):
    if (f'.{imageFormat}' not in file):
        continue;
        
    img = Image.open(f'{inputPath}/{file}');
    img = img.convert('L'); # Convert to grayscale
    img = np.array(img).tolist();
    trainImages.append(img);

trainImages = trainImages[:5];
trainLabels = trainLabels[:5];

imageDimensions = (imgResolution[0], imgResolution[1], 1); # 100x100xGrayscale

# No downsampling because the images are already small

# Create a sequential model that goes layer by layer
model = models.Sequential();

# Create a spacial convolutional layer as the first layer
# This layer will take in the input shape of the image
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=imageDimensions));

# Add another convolutional layer
model.add(layers.Conv2D(64, (3, 3), activation='relu'));

# Add another convolutional layer
model.add(layers.Conv2D(64, (3, 3), activation='relu'));

# Flatten the image into a 1D array for the dense layers
model.add(layers.Flatten());

# Add a dense layer with 64 neurons
model.add(layers.Dense(64, activation='relu'));

# Add a dense layer with 2 neurons
model.add(layers.Dense(2, activation='softmax'));

model.summary();

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy']);

# Train the model
model.fit(trainImages, trainLabels, epochs=nEpochs);

# Test the model to find the mitotic index

testImages = [];

for file in os.listdir(testPath):
    if (f'.{imageFormat}' not in file):
        continue;
        
    img = Image.open(f'{testPath}/{file}');
    img = img.convert('L');
    img = np.array(img);
    img = img.reshape(1, 100, 100, 1);
    testImages.append(img);

# Get the mitotic index by finding the number of mitotic images
# divided by the total number of images
mitoticIndex = 0;

for i in range(len(testImages)):
    prediction = model.predict(testImages[i])[0];

    if (prediction[0] > prediction[1]):
        mitoticIndex += 1;

mitoticIndex /= len(testImages);

print(f'Mitotic Index: {mitoticIndex}');