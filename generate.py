import math, os, json, sys
from random import randint, random
from PIL import Image, ImageDraw, ImageFilter

# Load the config file

configPath = 'config.json';

if (len(sys.argv) > 1):
    configPath = sys.argv[1];

if (not os.path.exists(configPath)):
    print(f'Config file \'{configPath}\' not found.');
    exit();

with open(configPath, 'r') as file:
    config = json.load(file)['generate'];

n = config['nImages'] or 1000;

imgW = config['imgResolution'][0] or 100;
imgH = config['imgResolution'][1] or 100;

centerX = imgW / 2;
centerY = imgH / 2;

baseColor = (0, 0, 0);
pointColor = (255, 255, 255);

labelsPath = config['labelsPath'] or 'data/labels.txt';
outputPath = config['outputPath'] or 'data';

imageFormat = config['imageFormat'] or 'png';

blurRadius = config['blurRadius'] or 2;
percentInMitois = config['percentInMitois'] or 0.5;
nonUniformnessMinMax = config['nonUniformnessMinMax'] or [0, 20];
configShape = config['shape'] or 'radom';

minNChromosomes = config['minNChromosomes'] or 0;
maxNChromosomesDivisor = config['maxNChromosomesDivisor'] or 2;

minChromosomeLength = config['minChromosomeLength'] or 3;
maxChromosomeLengthDivisor = config['maxChromosomeLengthDivisor'] or 5;

minChromosomeWidth = config['minChromosomeWidth'] or 10;
maxChromosomeWidthDivisor = config['maxChromosomeWidthDivisor'] or 20;

minNPoints = config['minNPoints'] or 0;
maxNPointsDivisor = config['maxNPointsDivisor'] or 20;

verbose = config['verbose'] or True;

if (not os.path.exists(outputPath)):
    os.mkdir(outputPath);
    print(f'Output path \'{outputPath}\' does not exist. It has been created.');

# Remove an existing labels file so that we don't append to it
if (os.path.exists(labelsPath)):
    os.remove(labelsPath);
    print('An existing labels file was found. It has been removed.');

def saveImage(i, points, inMitosis):
    img = Image.new('RGB', (imgW, imgH), baseColor);
    draw = ImageDraw.Draw(img);

    for point in points:
        draw.rounded_rectangle([point[0] - 1, point[1] - 1, point[0] + 1, point[1] + 1], fill=pointColor, radius=1);

    img = img.filter(ImageFilter.GaussianBlur(radius=blurRadius));
    img.save(f'{outputPath}/{i}.{imageFormat}', imageFormat.upper());

    with open(labelsPath, 'a') as file:
        file.write(f'{i}.{imageFormat} {inMitosis}\n');

def randomPointInCircle(x, y, r):
    randTheta = getRandomAngle();
    randR = math.sqrt(random()) * r;

    genX = x + randR * math.cos(randTheta);
    genY = y + randR * math.sin(randTheta);

    return (genX, genY);

def randomPointInEllipse(x, y, r1, r2):
    genX, genY = randomPointInCircle(x, y, r1);

    return (genX, genY * r2 / r1);

def randomPointInRotatedEllipse(x, y, r1, r2, rot):
    randTheta = getRandomAngle();
    randR = math.sqrt(random()) * r1;

    genX = x + randR * math.cos(rot + randTheta);
    genY = y + randR * math.sin(rot + randTheta) * r2 / r1;

    dx = genX - x;
    dy = genY - y;

    genX = x + dx * math.cos(rot) - dy * math.sin(rot);
    genY = y + dx * math.sin(rot) + dy * math.cos(rot);

    return (genX, genY);

def randomPointInNonUniformEllipse(x, y, r1, r2, nonUniformness):
    randTheta = getRandomAngle();
    randR = math.sqrt(random()) * (r1 + randint(0, nonUniformness));

    genX = x + randR * math.cos(randTheta);
    genY = y + randR * math.sin(randTheta) * r2 / r1;

    return (genX, genY);

def randomPointInNonUniformRotatedEllipse(x, y, r1, r2, rot, nonUniformness):
    randTheta = getRandomAngle();
    randR = math.sqrt(random()) * (r1 + randint(0, nonUniformness));

    genX = x + randR * math.cos(rot + randTheta);
    genY = y + randR * math.sin(rot + randTheta) * r2 / r1;

    dx = genX - x;
    dy = genY - y;

    genX = x + dx * math.cos(rot) - dy * math.sin(rot);
    genY = y + dx * math.sin(rot) + dy * math.cos(rot);

    return (genX, genY);

shapes = ['circle', 'ellipse'];

def getRandomShape():  
    return shapes[randint(0, len(shapes) - 1)];

def getRandomAngle():
    return random() * 360;

for i in range(n):
    inMitosis = random() < percentInMitois;
    rotation = getRandomAngle();
    nonUniformness = randint(nonUniformnessMinMax[0], nonUniformnessMinMax[1]);
    shape = configShape == 'random' and getRandomShape() or configShape;

    if (inMitosis):
        chromosomes = [];
        nChromosomes = randint(minNChromosomes, imgW / maxNChromosomesDivisor);

        for j in range(nChromosomes):
            chromosomePoints = [];

            chromosomeLength = randint(minChromosomeLength, imgW / maxChromosomeLengthDivisor);
            chromosomeWidth = randint(minChromosomeWidth, imgH / maxChromosomeWidthDivisor);
            chromosomeRotation = getRandomAngle();

            chromosomePosition = shape == 'ellipse' and randomPointInNonUniformRotatedEllipse(centerX, centerY, imgW / 4, imgW / 2, rotation, nonUniformness) or shape == 'circle' and randomPointInCircle(centerX, centerY, imgW / 4);

            for k in range(chromosomeLength):
                for l in range(chromosomeWidth):
                    chromosomePoints.append(
                        (chromosomePosition[0] + 
                            k * 
                            math.cos(chromosomeRotation) + 
                            l * 
                            math.cos(chromosomeRotation + math.pi / 2), 
                            
                        chromosomePosition[1] + 
                            k * 
                            math.sin(chromosomeRotation) + 
                            l * 
                            math.sin(chromosomeRotation + math.pi / 2))
                    );

            chromosomes.append(chromosomePoints);

        points = [];

        for chromosome in chromosomes:
            for point in chromosome:
                points.append(point);
    else:
        points = [];
        nPoints = randint(minNPoints, imgW * imgH / maxNPointsDivisor);

        for j in range(nPoints):
            pointPosition = shape == 'ellipse' and randomPointInNonUniformRotatedEllipse(centerX, centerY, imgW / 4, imgW / 2, rotation, nonUniformness) or shape == 'circle' and randomPointInCircle(centerX, centerY, imgW / 4);
            points.append(pointPosition);

    saveImage(i, points, inMitosis);
    
    if (verbose):
        print(f'Generated {i}.png');