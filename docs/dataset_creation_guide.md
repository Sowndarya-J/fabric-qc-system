# How to Create a Fabric Defect Dataset for YOLO Training

This guide explains how to create your own fabric defect dataset to train a custom YOLO model for the Fabric QC System.

## Step 1: Data Collection

### What You Need
- Fabric samples with various defects
- Camera or smartphone for capturing images
- Good lighting setup

### Types of Defects to Collect
- Holes/tears
- Stains
- Discoloration
- Weaving defects
- Foreign particles
- Print defects

### Image Requirements
- **Resolution**: At least 640x640 pixels (higher is better)
- **Format**: JPG or PNG
- **Quantity**: Minimum 100-200 images per defect class
- **Variety**: Different fabric types, colors, lighting conditions

### Collection Tips
1. Capture images at multiple angles
2. Include both defective and defect-free samples
3. Vary distance from camera (close-up and overview shots)
4. Use different lighting conditions
5. Include various fabric textures and colors

## Step 2: Dataset Organization

Create this folder structure in your project:

```
fabric_dataset/
├── images/
│   ├── train/     # 70% of images
│   ├── valid/     # 20% of images
│   └── test/      # 10% of images
├── labels/
│   ├── train/     # YOLO annotation files
│   ├── valid/
│   └── test/
└── data.yaml      # Dataset configuration
```

## Step 3: Image Annotation

### Tools Needed
- **LabelImg**: Free annotation tool for YOLO
- **Roboflow**: Online annotation platform
- **CVAT**: Open-source annotation tool

### Installation (LabelImg)
```bash
pip install labelImg
labelImg
```

### Annotation Process
1. Open LabelImg
2. Load images from `images/train/` folder
3. Draw rectangles around defects
4. Label each defect with class names like:
   - hole
   - stain
   - tear
   - discoloration
   - weaving_defect

### YOLO Format
Each annotation file (.txt) corresponds to an image (.jpg) with same name:

```
# Format: class_id x_center y_center width height (normalized 0-1)
0 0.5 0.3 0.2 0.1    # class 0, center at 50%,30%, 20% width, 10% height
1 0.7 0.8 0.15 0.05  # another defect
```

## Step 4: Create Dataset Configuration

Create `data.yaml` file:

```yaml
# fabric_dataset/data.yaml
train: ./images/train
valid: ./images/valid
test: ./images/test

# Number of classes
nc: 5

# Class names
names: ['hole', 'stain', 'tear', 'discoloration', 'weaving_defect']
```

## Step 5: Split Dataset

Move 70% images to `train/`, 20% to `valid/`, 10% to `test/` folders.

Corresponding annotation files must go to matching `labels/` subfolders.

## Step 6: Train the Model

### Install Ultralytics
```bash
pip install ultralytics
```

### Training Command
```bash
from ultralytics import YOLO

# Load pre-trained model
model = YOLO('yolov8n.pt')

# Train on your dataset
model.train(
    data='fabric_dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='fabric_defect_detector'
)
```

### Alternative CLI Training
```bash
yolo train data=fabric_dataset/data.yaml model=yolov8n.pt epochs=100 imgsz=640
```

## Step 7: Evaluate and Export

### Validation
```python
# Validate trained model
model.val()
```

### Export for Deployment
```python
# Export to different formats
model.export(format='onnx')  # For faster inference
model.export(format='tflite') # For mobile deployment
```

## Step 8: Integration

Replace the `best.pt` file in your project with your newly trained model:

```bash
cp runs/detect/fabric_defect_detector/weights/best.pt /path/to/your/project/
```

## Tips for Better Results

1. **Class Balance**: Ensure similar number of samples per defect type
2. **Data Augmentation**: YOLO automatically augments data during training
3. **Image Quality**: Use high-resolution, well-lit images
4. **Annotation Accuracy**: Precise bounding boxes are crucial
5. **Iterative Training**: Train multiple times with improved datasets

## Common Issues

- **Low mAP**: Check annotation quality and class balance
- **Overfitting**: Add more varied training data
- **Poor Detection**: Ensure proper lighting and image quality

## Resources

- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [LabelImg GitHub](https://github.com/heartexlabs/labelImg)
- [Roboflow](https://roboflow.com/) - Online annotation platform