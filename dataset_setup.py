#!/usr/bin/env python3
"""
Script to create and manage fabric defect dataset structure.
Run this script to set up your dataset folder automatically.
"""

import os
import shutil
from pathlib import Path
import random

def create_dataset_structure(dataset_path="fabric_dataset"):
    """Create the complete dataset folder structure."""
    
    base = Path(dataset_path)
    
    # Create main directories
    folders = [
        base / "images" / "train",
        base / "images" / "valid",
        base / "images" / "test",
        base / "labels" / "train",
        base / "labels" / "valid",
        base / "labels" / "test",
        base / "raw_images",  # For storing unsorted images
    ]
    
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {folder}")
    
    # Create data.yaml
    data_yaml = base / "data.yaml"
    yaml_content = """# Fabric Defect Dataset
path: ./fabric_dataset
train: images/train
val: images/valid
test: images/test

# Number of classes
nc: 5

# Class names
names: ['hole', 'stain', 'tear', 'discoloration', 'weaving_defect']
"""
    
    with open(data_yaml, 'w') as f:
        f.write(yaml_content)
    print(f"✓ Created: {data_yaml}")
    
    # Create README
    readme = base / "README.md"
    readme_content = """# Fabric Defect Dataset

## Structure
- `raw_images/`: Place your photographed fabric images here before annotation
- `images/train/`: Annotated training images (70%)
- `images/valid/`: Validation images (20%)
- `images/test/`: Test images (10%)
- `labels/train/`, `labels/valid/`, `labels/test/`: Corresponding YOLO annotation files

## Workflow

1. Place raw fabric images in `raw_images/` folder
2. Run `split_dataset.py` to organize into train/valid/test
3. Use LabelImg to annotate images (see `../setup_annotation_tools.md`)
4. Ensure `.txt` annotation files are in corresponding `labels/` folders
5. Run training script

## Defect Classes
- **hole**: Physical holes or tears in fabric
- **stain**: Discoloration or spots
- **tear**: Ripped or damaged areas
- **discoloration**: Color variations or fading
- **weaving_defect**: Issues in fabric weaving pattern
"""
    
    with open(readme, 'w') as f:
        f.write(readme_content)
    print(f"✓ Created: {readme}")
    
    print(f"\n✅ Dataset structure created in '{dataset_path}/'")
    print(f"\nNext steps:")
    print(f"1. Place raw fabric images in '{dataset_path}/raw_images/'")
    print(f"2. Run: python split_dataset.py")
    print(f"3. Annotate images using LabelImg")

def split_dataset(dataset_path="fabric_dataset", train_ratio=0.7, valid_ratio=0.2):
    """
    Split images from raw_images folder into train/valid/test.
    
    Args:
        dataset_path: Path to dataset directory
        train_ratio: Proportion for training (default 0.7)
        valid_ratio: Proportion for validation (default 0.2)
    """
    
    base = Path(dataset_path)
    raw_dir = base / "raw_images"
    
    if not raw_dir.exists():
        print(f"❌ Error: {raw_dir} not found!")
        return
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    images = [f for f in raw_dir.iterdir() 
              if f.suffix in image_extensions]
    
    if not images:
        print(f"❌ No images found in {raw_dir}")
        return
    
    print(f"Found {len(images)} images")
    
    # Shuffle and split
    random.shuffle(images)
    
    train_count = int(len(images) * train_ratio)
    valid_count = int(len(images) * valid_ratio)
    
    train_images = images[:train_count]
    valid_images = images[train_count:train_count + valid_count]
    test_images = images[train_count + valid_count:]
    
    # Copy to respective folders
    dest_folders = {
        'train': (base / 'images' / 'train', train_images),
        'valid': (base / 'images' / 'valid', valid_images),
        'test': (base / 'images' / 'test', test_images),
    }
    
    for split, (dest_dir, img_list) in dest_folders.items():
        for img in img_list:
            shutil.copy2(img, dest_dir / img.name)
        print(f"✓ Copied {len(img_list)} images to {split}")
    
    print(f"\n✅ Dataset split complete!")
    print(f"Training: {len(train_images)} images")
    print(f"Validation: {len(valid_images)} images")
    print(f"Test: {len(test_images)} images")

def verify_dataset(dataset_path="fabric_dataset"):
    """Verify dataset structure is correct."""
    
    base = Path(dataset_path)
    
    print("🔍 Verifying dataset structure...\n")
    
    all_ok = True
    
    # Check images and labels
    for split in ['train', 'valid', 'test']:
        img_dir = base / 'images' / split
        label_dir = base / 'labels' / split
        
        if not img_dir.exists():
            print(f"❌ Missing: {img_dir}")
            all_ok = False
            continue
        
        if not label_dir.exists():
            print(f"⚠️  Missing: {label_dir}")
        
        img_count = len([f for f in img_dir.iterdir() 
                        if f.suffix in {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}])
        label_count = len([f for f in label_dir.iterdir() if f.suffix == '.txt'])
        
        print(f"📁 {split}:")
        print(f"   Images: {img_count}")
        print(f"   Labels: {label_count}")
        
        if img_count > 0 and label_count == 0:
            print(f"   ⚠️  WARNING: No annotations found! Please annotate images.")
        elif img_count > label_count:
            print(f"   ⚠️  WARNING: {img_count - label_count} images missing annotations")
        elif img_count == label_count and img_count > 0:
            print(f"   ✓ All images annotated")
    
    # Check data.yaml
    yaml_file = base / 'data.yaml'
    if yaml_file.exists():
        print(f"\n✓ data.yaml exists")
    else:
        print(f"\n❌ data.yaml not found!")
        all_ok = False
    
    if all_ok:
        print(f"\n✅ Dataset structure looks good!")
    else:
        print(f"\n⚠️  Please fix the issues above")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        dataset_path = sys.argv[2] if len(sys.argv) > 2 else "fabric_dataset"
        
        if command == "create":
            create_dataset_structure(dataset_path)
        elif command == "split":
            split_dataset(dataset_path)
        elif command == "verify":
            verify_dataset(dataset_path)
        else:
            print(f"Unknown command: {command}")
    else:
        # Default: create structure
        create_dataset_structure()
        print("\nTo split images into train/valid/test:")
        print("  python dataset_setup.py split fabric_dataset")
        print("\nTo verify dataset structure:")
        print("  python dataset_setup.py verify fabric_dataset")
