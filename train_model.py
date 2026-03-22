#!/usr/bin/env python3
"""
Script to train YOLO model on fabric defect dataset.
Place this in your project root directory.
"""

from ultralytics import YOLO
import os
from pathlib import Path

def train_model(
    data_yaml="fabric_dataset/data.yaml",
    model_name="yolov8n",
    epochs=100,
    batch_size=16,
    imgsz=640,
    device=0,  # GPU device (0 for first GPU, "cpu" for CPU)
    project="runs/detect",
    name="fabric_defect_v1"
):
    """
    Train YOLO model on fabric defect dataset.
    
    Args:
        data_yaml: Path to data.yaml file
        model_name: YOLO model size (yolov8n, yolov8s, yolov8m, yolov8l, yolov8x)
        epochs: Number of training epochs
        batch_size: Batch size (reduce if out of memory)
        imgsz: Image size for training
        device: GPU device or "cpu"
        project: Output project directory
        name: Run name
    """
    
    print("=" * 60)
    print("YOLO Model Training for Fabric Defect Detection")
    print("=" * 60)
    
    # Check if data.yaml exists
    if not os.path.exists(data_yaml):
        print(f"❌ Error: {data_yaml} not found!")
        print("Please ensure your dataset is correctly structured.")
        return False
    
    print(f"\n📁 Dataset config: {data_yaml}")
    
    # Load model
    print(f"\n🔄 Loading {model_name} model...")
    try:
        model = YOLO(f'{model_name}.pt')
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print(f"Downloading {model_name}.pt...")
        model = YOLO(f'{model_name}.pt')
    
    # Training configuration
    print(f"\n⚙️  Training Configuration:")
    print(f"   Model: {model_name}")
    print(f"   Epochs: {epochs}")
    print(f"   Batch Size: {batch_size}")
    print(f"   Image Size: {imgsz}x{imgsz}")
    print(f"   Device: {device}")
    
    # Train
    print(f"\n🚀 Starting training...")
    print("-" * 60)
    
    try:
        results = model.train(
            data=data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch_size,
            device=device,
            patience=20,  # Early stopping patience
            save=True,
            project=project,
            name=name,
            # Optional parameters
            augment=True,  # Data augmentation
            flipud=0.5,    # Flip up-down
            fliplr=0.5,    # Flip left-right
            mosaic=1.0,    # Mosaic augmentation
            cache=False,   # Cache images
            verbose=True,
        )
        
        print("-" * 60)
        print(f"\n✅ Training completed!")
        
        # Model location
        best_model = Path(project) / name / "weights" / "best.pt"
        print(f"\n📌 Best model saved at: {best_model}")
        
        # Results location
        results_file = Path(project) / name / "results.csv"
        if results_file.exists():
            print(f"📊 Training results saved at: {results_file}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        return False

def validate_model(weights_path="runs/detect/fabric_defect_v1/weights/best.pt"):
    """Validate trained model on test set."""
    
    print("\n" + "=" * 60)
    print("Model Validation")
    print("=" * 60)
    
    if not os.path.exists(weights_path):
        print(f"❌ Model weights not found: {weights_path}")
        return
    
    print(f"📦 Loading model: {weights_path}")
    model = YOLO(weights_path)
    
    print(f"🔍 Validating on test set...")
    metrics = model.val()
    
    print(f"\n✅ Validation Results:")
    print(f"   mAP50: {metrics.box.map50:.3f}")
    print(f"   mAP50-95: {metrics.box.map:.3f}")
    print(f"   Precision: {metrics.box.mp:.3f}")
    print(f"   Recall: {metrics.box.mr:.3f}")

def export_model(
    weights_path="runs/detect/fabric_defect_v1/weights/best.pt",
    export_formats=["onnx", "tflite"]
):
    """Export trained model to different formats."""
    
    print("\n" + "=" * 60)
    print("Model Export")
    print("=" * 60)
    
    if not os.path.exists(weights_path):
        print(f"❌ Model weights not found: {weights_path}")
        return
    
    print(f"📦 Loading model: {weights_path}")
    model = YOLO(weights_path)
    
    for fmt in export_formats:
        try:
            print(f"🔄 Exporting to {fmt.upper()}...")
            model.export(format=fmt)
            print(f"✓ Exported to {fmt.upper()}")
        except Exception as e:
            print(f"✗ Failed to export to {fmt}: {e}")
    
    print(f"\n✅ Export completed!")

def quick_test(
    weights_path="runs/detect/fabric_defect_v1/weights/best.pt",
    test_image_path=None
):
    """Quick test on a single image."""
    
    if not os.path.exists(weights_path):
        print(f"❌ Model weights not found: {weights_path}")
        return
    
    if not test_image_path:
        print("Please provide a test image path")
        return
    
    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found: {test_image_path}")
        return
    
    print(f"🚀 Testing model on: {test_image_path}")
    model = YOLO(weights_path)
    
    results = model.predict(source=test_image_path, conf=0.25)
    
    for result in results:
        print(f"\n✅ Detection results:")
        print(f"   Boxes: {len(result.boxes)}")
        for i, box in enumerate(result.boxes):
            print(f"   Box {i+1}: Class {int(box.cls)}, Confidence {box.conf:.3f}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train YOLO model for fabric defect detection")
    parser.add_argument("--mode", default="train", 
                       choices=["train", "validate", "export", "test"],
                       help="Operation mode")
    parser.add_argument("--data", default="fabric_dataset/data.yaml",
                       help="Path to data.yaml")
    parser.add_argument("--model", default="yolov8n",
                       help="YOLO model size (n/s/m/l/x)")
    parser.add_argument("--epochs", type=int, default=100,
                       help="Number of epochs")
    parser.add_argument("--batch", type=int, default=16,
                       help="Batch size")
    parser.add_argument("--imgsz", type=int, default=640,
                       help="Image size")
    parser.add_argument("--device", default=0,
                       help="Device (0 for GPU, 'cpu' for CPU)")
    parser.add_argument("--weights", default="runs/detect/fabric_defect_v1/weights/best.pt",
                       help="Path to trained weights")
    parser.add_argument("--test-image", help="Test image path")
    
    args = parser.parse_args()
    
    if args.mode == "train":
        train_model(
            data_yaml=args.data,
            model_name=args.model,
            epochs=args.epochs,
            batch_size=args.batch,
            imgsz=args.imgsz,
            device=args.device
        )
    elif args.mode == "validate":
        validate_model(args.weights)
    elif args.mode == "export":
        export_model(args.weights)
    elif args.mode == "test":
        quick_test(args.weights, args.test_image)
