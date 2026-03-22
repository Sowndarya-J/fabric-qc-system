#!/usr/bin/env python3
"""
Image collection helper script.
Helps verify image quality and organize collected fabric defect images.
"""

import os
import shutil
from pathlib import Path
from PIL import Image
import json
from datetime import datetime

class ImageCollectionHelper:
    """Helper class for managing image collection."""
    
    def __init__(self, raw_image_dir="fabric_dataset/raw_images"):
        self.raw_dir = Path(raw_image_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
    
    def check_image_quality(self, image_path):
        """
        Check if image meets quality standards.
        
        Returns:
            (is_good, issues_list)
        """
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            issues = []
            
            # Check resolution
            if width < 640 or height < 640:
                issues.append(f"Low resolution: {width}x{height} (need 640x640+)")
            
            # Check aspect ratio (should be roughly square)
            ratio = width / height if height > 0 else 0
            if ratio < 0.7 or ratio > 1.3:
                issues.append(f"Bad aspect ratio: {ratio:.2f}:1 (need ~1:1)")
            
            # Check file size
            file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
            if file_size_mb < 0.1:
                issues.append(f"File too small: {file_size_mb:.2f}MB (corrupted?)")
            
            # Check if image is mostly white/blank
            img_array = img.convert('L')  # Convert to grayscale
            brightness = sum(img_array.getdata()) / (width * height)
            if brightness > 250:
                issues.append(f"Image too bright/blank (brightness: {brightness:.0f}/255)")
            
            is_good = len(issues) == 0
            return is_good, issues
            
        except Exception as e:
            return False, [str(e)]
    
    def scan_images(self):
        """Scan all images in raw_images directory."""
        
        if not self.raw_dir.exists():
            print(f"❌ Directory not found: {self.raw_dir}")
            return
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
        image_files = [f for f in self.raw_dir.rglob('*') 
                      if f.suffix in image_extensions]
        
        if not image_files:
            print(f"❌ No images found in {self.raw_dir}")
            return
        
        print(f"🔍 Scanning {len(image_files)} images...")
        print("=" * 70)
        
        good_images = []
        bad_images = []
        
        for i, img_path in enumerate(image_files, 1):
            is_good, issues = self.check_image_quality(str(img_path))
            
            rel_path = img_path.relative_to(self.raw_dir)
            
            if is_good:
                good_images.append(img_path)
                print(f"✓ [{i:3d}] {rel_path}")
            else:
                bad_images.append((img_path, issues))
                print(f"✗ [{i:3d}] {rel_path}")
                for issue in issues:
                    print(f"        └─ {issue}")
        
        print("=" * 70)
        print(f"\n📊 Summary:")
        print(f"   Good images: {len(good_images)}/{len(image_files)}")
        print(f"   Bad images: {len(bad_images)}/{len(image_files)}")
        print(f"   Quality: {len(good_images)/len(image_files)*100:.1f}%")
        
        if bad_images:
            print(f"\n⚠️  Issues found:")
            for img_path, issues in bad_images[:5]:  # Show first 5
                print(f"   - {img_path.name}: {', '.join(issues)}")
            if len(bad_images) > 5:
                print(f"   ... and {len(bad_images)-5} more")
        
        return good_images, bad_images
    
    def organize_by_type(self):
        """Help user organize images by defect type."""
        
        print("\n📁 Image Organization Helper")
        print("=" * 70)
        
        defect_types = [
            'hole_small',
            'hole_medium', 
            'hole_large',
            'tear_small',
            'tear_large',
            'stain_light',
            'stain_dark',
            'discoloration',
            'weaving_defect',
            'perfect'
        ]
        
        print("Available defect types:")
        for i, dtype in enumerate(defect_types, 1):
            print(f"  {i}. {dtype}")
        
        print("\nCreating folder structure...")
        for dtype in defect_types:
            folder = self.raw_dir / dtype
            folder.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {folder.name}")
        
        print(f"\n💡 Tip: Move your images into these folders based on defect type")
        print(f"   Then run 'python collect_images.py validate' to check quality")
    
    def generate_summary(self, output_file="image_collection_summary.json"):
        """Generate summary of collected images."""
        
        good_images, bad_images = self.scan_images()
        
        if good_images is None:
            return
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_images": len(good_images) + len(bad_images),
            "good_images": len(good_images),
            "bad_images": len(bad_images),
            "quality_percentage": len(good_images) / (len(good_images) + len(bad_images)) * 100,
            "images": {
                "good": [str(p.relative_to(self.raw_dir)) for p in good_images],
                "bad": [
                    {
                        "path": str(p.relative_to(self.raw_dir)),
                        "issues": issues
                    }
                    for p, issues in bad_images
                ]
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Summary saved to {output_file}")
        return summary
    
    def rename_images(self, folder_name, prefix):
        """Rename images with consistent naming."""
        
        folder = self.raw_dir / folder_name
        if not folder.exists():
            print(f"❌ Folder not found: {folder}")
            return
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
        images = sorted([f for f in folder.iterdir() 
                        if f.suffix in image_extensions])
        
        print(f"Renaming {len(images)} images in {folder_name}...")
        
        for i, img_path in enumerate(images, 1):
            new_name = f"{prefix}_{i:03d}{img_path.suffix}"
            new_path = folder / new_name
            
            if new_path != img_path:
                img_path.rename(new_path)
                print(f"  ✓ {img_path.name} → {new_name}")
        
        print(f"✅ Renamed {len(images)} images")
    
    def copy_good_images(self, destination="fabric_dataset/selected_images"):
        """Copy only good quality images to a separate folder."""
        
        good_images, _ = self.scan_images()
        
        if good_images is None:
            return
        
        dest_dir = Path(destination)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nCopying {len(good_images)} good images to {destination}...")
        
        for img_path in good_images:
            shutil.copy2(img_path, dest_dir / img_path.name)
        
        print(f"✅ Copied {len(good_images)} images")

def print_menu():
    """Print interactive menu."""
    print("\n" + "=" * 70)
    print("Image Collection Helper")
    print("=" * 70)
    print("1. Scan images and check quality")
    print("2. Create folder structure for organization")
    print("3. Rename images (batch rename)")
    print("4. Copy only good quality images")
    print("5. Generate collection summary")
    print("0. Exit")
    print("=" * 70)

if __name__ == "__main__":
    import sys
    
    helper = ImageCollectionHelper()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "scan":
            helper.scan_images()
        elif command == "organize":
            helper.organize_by_type()
        elif command == "rename":
            if len(sys.argv) >= 4:
                folder = sys.argv[2]
                prefix = sys.argv[3]
                helper.rename_images(folder, prefix)
            else:
                print("Usage: python collect_images.py rename <folder> <prefix>")
                print("Example: python collect_images.py rename hole_small hole_s")
        elif command == "copy":
            helper.copy_good_images()
        elif command == "summary":
            helper.generate_summary()
        else:
            print(f"Unknown command: {command}")
    else:
        # Interactive mode
        while True:
            print_menu()
            choice = input("Select option: ").strip()
            
            if choice == "1":
                helper.scan_images()
            elif choice == "2":
                helper.organize_by_type()
            elif choice == "3":
                folder = input("Folder name (e.g., hole_small): ").strip()
                prefix = input("Prefix (e.g., hole_s): ").strip()
                helper.rename_images(folder, prefix)
            elif choice == "4":
                helper.copy_good_images()
            elif choice == "5":
                helper.generate_summary()
            elif choice == "0":
                print("Goodbye! 👋")
                break
            else:
                print("Invalid option. Please try again.")
