📁 New Files Created:
1. setup_annotation_tools.md
Complete guide to install and use annotation tools:

LabelImg (easiest for Mac/Linux)
Roboflow (cloud-based, no installation needed)
CVAT (open-source, Docker-based)
Quick start scripts and keyboard shortcuts
2. dataset_setup.py
Python utility script to manage dataset automatically:
# Create folder structure
python dataset_setup.py create fabric_dataset

# Split images into train/valid/test (70/20/10)
python dataset_setup.py split fabric_dataset

# Verify dataset integrity
python dataset_setup.py verify fabric_dataset

3. train_model.py
Complete training script with multiple options:
# Train new model (easiest)
python train_model.py --mode train --epochs 100

# Validate trained model
python train_model.py --mode validate

# Export model to ONNX/TFLite
python train_model.py --mode export

# Quick test on single image
python train_model.py --mode test --test-image path/to/image.jpg

🚀 Complete Workflow:
1.Create dataset structure:
python dataset_setup.py create fabric_dataset

2.Collect fabric images and place in fabric_dataset/raw_images/

3.Split into train/valid/test:
python dataset_setup.py split fabric_dataset

4.Annotate images using LabelImg:
labelImg fabric_dataset/images/train

5.Train model:
python train_model.py --mode train --epochs 100

6.Your trained model will be saved to runs/detect/fabric_defect_v1/weights/best.pt

7.Replace in project:
cp runs/detect/fabric_defect_v1/weights/best.pt ./best.pt


8.Python tool to help manage collected images:
# Scan all images and check quality
python collect_images.py scan

# Create organized folder structure
python collect_images.py organize

# Rename images with consistent naming
python collect_images.py rename hole_small hole_s

# Copy only good quality images
python collect_images.py copy

# Generate summary report
python collect_images.py summary

Complete Workflow Summary:
1️⃣  Collect Images
   └─ Read: docs/image_collection_guide.md
   └─ Create defects or find real samples
   └─ Take ~280 diverse photos
   └─ Save to: fabric_dataset/raw_images/

2️⃣  Quality Check
   └─ Run: python collect_images.py scan
   └─ Removes blurry/poor images

3️⃣  Organize
   └─ Run: python collect_images.py organize
   └─ Creates folder structure by defect type
   └─ Manually move images into folders

4️⃣  Annotate
   └─ Run: labelImg fabric_dataset/images/train
   └─ Draw boxes around defects
   └─ Save annotations

5️⃣  Train Model
   └─ Run: python train_model.py --mode train --epochs 100
   └─ Model saved to: runs/detect/fabric_defect_v1/weights/best.pt

6️⃣  Deploy
   └─ Copy trained model to project
   └─ Run application with new model