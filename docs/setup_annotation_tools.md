# Annotation Tools Setup Guide

Guide to install and use annotation tools for creating your fabric defect dataset.

## Option 1: LabelImg (Recommended for Beginners)

### Installation

#### macOS
```bash
# Using pip
pip install labelImg

# Or using Homebrew
brew install labelimg
```

#### Linux (Ubuntu/Debian)
```bash
pip install labelImg
```

#### Windows
```bash
pip install labelImg
```

### Running LabelImg

```bash
labelImg
```

This opens the GUI application.

### How to Use LabelImg

1. **Open Directory**: Click `Open Dir` and select your `fabric_dataset/images/train/` folder
2. **Create New Label**: In settings, define your defect classes (hole, stain, tear, discoloration, weaving_defect)
3. **Draw Rectangles**: 
   - Click and drag to create bounding boxes around defects
   - Select the class from dropdown
4. **Save Annotations**: Press `Ctrl+S` to save as YOLO format
5. **Next Image**: Press `D` or click next to move to next image
6. **Keyboard Shortcuts**:
   - `A`: Previous image
   - `D`: Next image
   - `Ctrl+S`: Save
   - `Delete`: Delete selected box
   - `Space`: Mark as done

### YOLO Format Configuration

Before starting, set annotation format to YOLO:
1. Go to `View` menu
2. Select `Auto Save Mode`
3. Choose `YOLO` as output format

Each annotated image will have a `.txt` file with same name containing defect coordinates.

## Option 2: Roboflow (Cloud-Based)

### Setup

1. Visit [https://roboflow.com/](https://roboflow.com/)
2. Create free account
3. Create new project "Fabric Defect Detection"
4. Select task type: "Object Detection"

### Upload Images

1. Click "Upload"
2. Drag and drop your fabric images
3. Auto-orient images
4. Click "Save"

### Annotate

1. Images appear in queue
2. Draw boxes around defects
3. Select class from dropdown
4. Save each annotation

### Export

1. Click "Generate"
2. Select "YOLO v8" format
3. Download dataset
4. Extract to your `fabric_dataset/` folder

### Benefits
- Cloud storage (no local storage needed)
- Easier collaboration
- Auto-augmentation available
- Free tier available

## Option 3: CVAT (Open Source)

### Installation (Docker Required)

```bash
# Clone CVAT
git clone https://github.com/opencv/cvat

cd cvat

# Start with Docker Compose
docker-compose up -d
```

### Access

Open browser: `http://localhost:8080`

### Create Task

1. Click "Create new task"
2. Upload images
3. Select "Object detection"
4. Define labels (hole, stain, tear, etc.)

### Annotate

1. Open task
2. Draw rectangles around defects
3. Save annotations
4. Export as YOLO format

## Quick Start Script for macOS/Linux

```bash
#!/bin/bash

# Install annotation tool
pip install labelImg

# Create dataset structure
mkdir -p fabric_dataset/{images/{train,valid,test},labels/{train,valid,test}}

# Create data.yaml
cat > fabric_dataset/data.yaml << EOF
train: ./images/train
valid: ./images/valid
test: ./images/test

nc: 5
names: ['hole', 'stain', 'tear', 'discoloration', 'weaving_defect']
EOF

# Start LabelImg
echo "Created folder structure. Starting LabelImg..."
labelImg fabric_dataset/images/train
```

Save this as `setup_dataset.sh` and run:
```bash
chmod +x setup_dataset.sh
./setup_dataset.sh
```

## Recommended Workflow

1. **Collect Images**: Place ~200-500 raw fabric images
2. **Split Dataset**: 70% train, 20% valid, 10% test
3. **Annotate**: Use LabelImg for ~100-200 images first
4. **Train Model**: See if results are good
5. **Add More**: If accuracy is low, collect and annotate more images
6. **Iterate**: Improve dataset quality based on training results

## Tips for Accurate Annotations

- **Tight Boxes**: Draw boxes close to defect edges, not too loose
- **Complete Coverage**: Make sure entire defect is inside box
- **Consistent Classes**: Use same class name for similar defects
- **No Overlaps**: Minimize overlapping boxes when possible
- **Clear Images**: Skip blurry or unclear images

## Common Problems

**Problem**: LabelImg won't start
**Solution**: 
```bash
pip install --upgrade labelImg
```

**Problem**: Can't find images
**Solution**: Click `Open Dir` and navigate to `fabric_dataset/images/train/`

**Problem**: YOLO format files not created
**Solution**: Ensure LabelImg is set to YOLO format in View menu

## Next Steps

After annotating 200+ images:
1. Split them into train/valid/test folders
2. Ensure labels are in corresponding `labels/` folders
3. Create `data.yaml` file
4. Run training script (see `docs/dataset_creation_guide.md`)
