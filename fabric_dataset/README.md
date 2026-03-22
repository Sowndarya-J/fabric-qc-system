# Fabric Defect Dataset

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
