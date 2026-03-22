# Collecting Sample Fabric Images - Complete Guide

This guide walks you through collecting fabric defect images for training your YOLO model.

## Equipment Needed

### Essential
- **Camera**: Smartphone camera is sufficient (12MP+) or DSLR
- **Lighting**: Bright natural light or LED lights
- **White Background**: White paper, cloth, or table surface
- **Ruler/Scale**: For reference (optional but helpful)
- **Storage Device**: USB drive or cloud storage

### Optional (for better quality)
- Phone tripod ($10-20)
- LED ring light ($15-30)
- Fabric samples with known defects
- Backlight setup
- Macro lens attachment

## Step 1: Source Fabric Samples

### Option A: Synthetic Defects (Easiest for Testing)
Create artificial defects for controlled training:
- Use white/light colored fabric (easier to see defects)
- Create holes with scissors (various sizes: small, medium, large)
- Make tears/rips
- Apply stains (coffee, ink, dye)
- Create discoloration with markers
- Weave pattern disruptions with needle and thread

```
Example defects to create:
├── Hole (diameter: 2mm, 5mm, 10mm, 20mm)
├── Tear (length: 1cm-10cm, direction: horizontal/vertical/diagonal)
├── Stain (size: 1cm², 5cm², 10cm²)
├── Discoloration (area: 2cm², 5cm², 10cm²)
└── Weaving defect (pattern disruptions)
```

### Option B: Real Samples
Collect from actual sources:
- **Manufacturing**: Contact local textile mills for rejected samples
- **Clothing stores**: Ask for damaged/unsellable samples
- **Online**: Purchase sample packs from fabric suppliers
- **Donations**: Ask tailors or garment factories for scrap fabric

### Option C: Hybrid Approach (Recommended)
- Start with 50% real defects + 50% synthetic defects
- Mix different fabric types and colors
- Gradually add more real data from manufacturing

## Step 2: Photography Setup

### Lighting Setup

**Best Setup: Natural Window Light**
```
Window (Light Source)
    ↓
---------
│ Fabric │
│ Sample │
---------
    ↓
Camera
```

**Alternative: LED Setup**
```
LED Light (Front)
    ↓
---------
│ Fabric │
│ Sample │
---------
    ↓
Camera

LED Light (Back) - Optional for backlighting
```

### Camera Settings

**For Smartphone**
1. Use default camera app
2. Set to highest resolution
3. Use portrait/detail mode if available
4. Avoid digital zoom (use physical positioning)
5. Enable grid for alignment
6. Turn off flash (use light sources instead)

**For DSLR**
- ISO: 200-400 (low for better quality)
- Aperture: f/5.6 - f/8.0 (good depth of field)
- Shutter Speed: 1/125 - 1/250
- Format: RAW or high-quality JPEG

### Positioning

**Good Angle** (45 degrees to fabric plane):
```
      Camera
         /
        /45°
----------- (Fabric)
```

**Also Good** (Perpendicular/Overhead):
```
Camera
  ↓
--------- (Fabric)
```

**Avoid** (Too shallow angle):
```
Camera ----→ (Fabric) - Creates distortion
```

## Step 3: Image Capture Protocol

### Checklist for Each Image

- [ ] Fabric is well-lit
- [ ] Entire defect is visible in frame
- [ ] White/neutral background
- [ ] No shadows on critical areas
- [ ] Image is sharp (not blurry)
- [ ] Defect is clearly visible
- [ ] Scale reference if helpful
- [ ] File saved with clear naming

### Capture Each Defect Multiple Ways

**For Every Defect, Take:**
1. Close-up view (defect fills 30-50% of image)
2. Medium view (defect fills 10-30% of image)
3. Wide view (defect fills 5-10% of image)
4. Different angles (if applicable)
5. Different lighting conditions

**Example Series:**
```
Hole_small_close_light1.jpg
Hole_small_close_light2.jpg
Hole_small_medium_light1.jpg
Hole_small_wide_light1.jpg
Hole_small_angle45_light1.jpg
```

### Batch Number Guidelines

For each defect type and size combination:

| Defect Type | Total Quantity | Variations |
|------------|---|---|
| Hole (small 2mm) | 30 images | 3 angles × 2 sizes × 5 lighting |
| Hole (medium 5mm) | 30 images | 3 angles × 2 sizes × 5 lighting |
| Hole (large 10mm+) | 30 images | 3 angles × 2 sizes × 5 lighting |
| Tear (small) | 25 images | Random orientations |
| Tear (large) | 25 images | Random orientations |
| Stain (light) | 25 images | Various positions |
| Stain (dark) | 25 images | Various positions |
| Discoloration | 20 images | Size variations |
| Weaving defect | 20 images | Pattern variations |
| **Perfect fabric** (no defects) | 50 images | Various types/colors |
| **Total** | **~280 images** | Diverse dataset |

## Step 4: File Organization

### Naming Convention

Use descriptive names:
```
{defect_type}_{size}_{angle}_{lighting}_{iteration}.jpg

Examples:
hole_small_close_bright_01.jpg
tear_medium_wide_dim_05.jpg
stain_large_overhead_natural_03.jpg
perfect_white_01.jpg
discoloration_medium_angle45_02.jpg
```

### Folder Structure During Collection

```
fabric_dataset/
└── raw_images/
    ├── hole_small/
    │   ├── hole_small_01.jpg
    │   ├── hole_small_02.jpg
    │   └── ...
    ├── hole_medium/
    ├── hole_large/
    ├── tear_small/
    ├── tear_large/
    ├── stain_light/
    ├── stain_dark/
    ├── discoloration/
    ├── weaving_defect/
    └── perfect/
```

## Step 5: Quality Standards

### Accept ✓
- [ ] Sharp, in-focus images
- [ ] Defect clearly visible
- [ ] Entire defect in frame
- [ ] Good lighting (no harsh shadows)
- [ ] Neutral background
- [ ] Proper exposure (not too bright/dark)
- [ ] Resolution: 640x640 minimum

### Reject ✗
- [ ] Blurry or out of focus
- [ ] Defect partially outside frame
- [ ] Harsh shadows on defect
- [ ] Poor lighting (too dark)
- [ ] Over-exposed (washed out)
- [ ] Cluttered background
- [ ] Multiple unrelated defects

## Step 6: Lighting Variations

Capture diverse lighting for robust model:

**Variation 1: Bright Natural Light**
- By window, direct sunlight
- High contrast shadows

**Variation 2: Soft Natural Light**
- Diffused window light (cloudy day)
- Soft shadows

**Variation 3: LED Front Light**
- Even illumination
- Controlled shadows

**Variation 4: LED Back Light + Front Light**
- Rim lighting effect
- Better edge definition

**Variation 5: Low Light**
- Dimly lit condition
- High ISO/longer exposure

## Step 7: Quick Capture Workflow

```bash
Day 1: Setup & Lighting
├── Arrange fabric samples
├── Test lighting angles
├── Take test shots
└── Adjust settings

Day 2-3: Systematic Capture
├── Hole defects (24 images per hole type)
├── Tear defects
├── Stain defects
└── Session 1: Control

Day 4-5: Continuation
├── Discoloration
├── Weaving defects
├── Perfect samples (50+ images)
└── Session 2: Variations

Day 6: Quality Check
├── Review all 280+ images
├── Delete blurry/poor quality
├── Organize into folders
└── Backup to storage
```

## Step 8: Batch Processing for Collection

### Python Helper Script

```python
# Check image quality before annotation
from PIL import Image
from pathlib import Path
import os

def check_image_quality(image_path):
    """Check if image meets quality standards."""
    img = Image.open(image_path)
    width, height = img.size
    
    issues = []
    
    # Check resolution
    if width < 640 or height < 640:
        issues.append(f"Low resolution: {width}x{height}")
    
    # Check aspect ratio (should be roughly square)
    ratio = width / height if height > 0 else 0
    if ratio < 0.8 or ratio > 1.2:
        issues.append(f"Unusual aspect ratio: {ratio:.2f}")
    
    return len(issues) == 0, issues

# Check all images
image_dir = Path("fabric_dataset/raw_images")
for img_file in image_dir.glob("**/*.jpg"):
    is_good, issues = check_image_quality(str(img_file))
    if not is_good:
        print(f"⚠️  {img_file.name}: {', '.join(issues)}")
```

## Step 9: Uploading & Organizing

### Transfer to Computer

```bash
# Create organized structure
python dataset_setup.py create fabric_dataset

# Copy raw images
cp ~/Pictures/fabric_photos/* fabric_dataset/raw_images/

# Split into train/valid/test
python dataset_setup.py split fabric_dataset

# Verify structure
python dataset_setup.py verify fabric_dataset
```

## Step 10: Backup & Storage

### Create Backups

```bash
# Backup to USB
cp -r fabric_dataset/ /Volumes/USB_Drive/

# Backup to cloud (if available)
# Upload to Google Drive, OneDrive, or Dropbox
```

## Common Issues & Solutions

### Problem: Images Too Dark
**Solution**: Add more lighting or increase smartphone brightness settings

### Problem: Blurry Images
**Solution**: Hold phone steady (use tripod), increase light, avoid digital zoom

### Problem: Defect Not Clear
**Solution**: Move closer, adjust angle, add backlighting

### Problem: Too Much Shadow
**Solution**: Use diffused light, add fill light (reflector or second light source)

### Problem: Background Distracting
**Solution**: Use plain white/neutral background, ensure clean fabric surface

## Data Collection Checklist

- [ ] Equipment ready (camera, lights, background)
- [ ] Fabric samples sourced and defects created
- [ ] Folder structure created
- [ ] Test images taken and reviewed
- [ ] Photography settings optimized
- [ ] Systematic capture session completed
- [ ] ~280+ images collected
- [ ] Quality review done (no blurry/bad images)
- [ ] Images organized by defect type
- [ ] Files backed up
- [ ] Ready for annotation with LabelImg!

## Tips for Success

1. **Start Small**: Collect 50-100 images first, train model, see results
2. **Iterate**: Add more diverse images based on model performance
3. **Document**: Note lighting/angle info for reproducible quality
4. **Backup**: Always keep copies of original images
5. **Organize**: Use consistent naming to avoid confusion during annotation
6. **Quality Over Quantity**: 100 perfect images > 500 poor quality images
7. **Diverse Angles**: Different perspectives improve model generalization