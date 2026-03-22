# Fabric Quality Control System

A comprehensive web-based application for automated fabric defect detection and quality monitoring using computer vision and AI technologies.

## 🚀 Features

### Core Functionality
- **Real-time Defect Detection**: Live webcam inspection using YOLOv8 models for instant fabric quality analysis
- **Image Upload Analysis**: Upload fabric images for batch processing and defect identification
- **Multi-user Authentication**: Secure login system with role-based access (Admin/User)
- **Admin Dashboard**: User management, inspection history, and system monitoring
- **Model Performance Metrics**: Detailed analytics on detection accuracy and performance
- **Fabric Assistant**: AI-powered chatbot with voice interaction for fabric-related queries

### Advanced Features
- **PDF Report Generation**: Automated inspection reports with defect details and recommendations
- **Heatmap Visualization**: Visual representation of defect distribution
- **Email Notifications**: Send inspection reports via email
- **QR Code Generation**: For easy access to inspection results
- **Voice Commands**: Speech recognition and text-to-speech capabilities
- **Database Integration**: SQLite-based storage for inspections and user data

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: YOLOv8 (Ultralytics), OpenAI GPT
- **Computer Vision**: OpenCV, PIL
- **Real-time Processing**: WebRTC, AV
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib
- **Reporting**: ReportLab
- **Database**: SQLite
- **Voice Features**: SpeechRecognition, gTTS, Streamlit Mic Recorder

## 📋 Prerequisites

- Python 3.10
- System packages: `libgl1`, `libglib2.0-0t64` (for OpenCV)

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sowndarya-J/fabric-qc-system.git
   cd fabric-qc-system
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies** (Ubuntu/Debian):
   ```bash
   sudo apt-get update
   sudo apt-get install libgl1-mesa-glx libglib2.0-0
   ```

## 🚀 Running the Application

### Local Development
```bash
./start.sh
```
Or manually:
```bash
streamlit run Home.py --server.port 8501 --server.address 0.0.0.0
```

### Production Deployment
Set the `PORT` environment variable for the desired port:
```bash
PORT=8501 ./start.sh
```

## 📁 Project Structure

```
fabric-qc-system/
├── app.py                 # Main application entry point
├── Home.py                # Home page with navigation
├── theme.py               # Dark theme configuration
├── utils.py               # Utility functions and database operations
├── users.json             # User credentials and roles
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version specification
├── packages.txt          # System dependencies
├── start.sh              # Startup script
├── best.pt               # Trained YOLO model weights
├── yolov8n.pt            # YOLOv8 nano model
├── results.csv           # Inspection results data
├── saved_inspections/    # Directory for saved inspection images
└── pages/
    ├── 1_Login.py        # Login page
    ├── 2_Webcam_Realtime.py  # Real-time webcam detection
    ├── 3_Image_Upload.py     # Image upload and analysis
    ├── 4_Admin_Dashboard.py  # Admin management interface
    ├── 5_Model_Metrics.py    # Model performance dashboard
    └── 7_Fabric_Assistant.py  # AI assistant with chat and voice
```

## 🔐 User Management

### Default Users
- **Admin**: Username: `admin`, Password: `admin123` (Role: admin)
- **User**: Username: `user`, Password: `user123` (Role: user)

### Adding New Users
Admins can add new users through the Admin Dashboard interface.

## 🤖 AI Features

### Fabric Assistant
- Powered by OpenAI GPT
- Voice input/output capabilities
- Fabric defect analysis and recommendations
- Quality control guidance

### Defect Detection Model
- YOLOv8-based object detection
- Pre-trained on fabric defect datasets
- Real-time processing capabilities
- Configurable confidence thresholds

## 📊 Data & Model Training

### Dataset
- Custom fabric defect dataset with annotated images
- Includes various defect types: holes, stains, tears, discoloration
- Images captured under different lighting conditions
- Annotated with bounding boxes for supervised learning

### Model Training
- **Base Model**: YOLOv8 nano (yolov8n.pt) for lightweight inference
- **Custom Model**: Fine-tuned weights (best.pt) trained on fabric-specific data
- Training performed using Ultralytics YOLOv8 framework
- Optimized for fabric inspection use case

## 📊 Data Storage

- **SQLite Database**: `fabric_inspections.db`
  - Stores inspection records
  - User session data
  - Defect statistics

- **File Storage**: `saved_inspections/`
  - Inspection images
  - Generated reports

## 🔧 Configuration

### Model Configuration
- Model weights: `best.pt` (custom trained) or `yolov8n.pt` (pre-trained)
- Confidence threshold: Adjustable via slider (0.0-1.0)

### Email Configuration
Configure SMTP settings in `utils.py` for email notifications.

## 📈 Performance Metrics

- Detection accuracy
- Processing speed (FPS)
- False positive/negative rates
- Defect severity classification

## 🐛 Troubleshooting

### Common Issues
1. **OpenCV Import Error**: Install system dependencies
   ```bash
   sudo apt-get install libgl1-mesa-glx libglib2.0-0
   ```

2. **WebRTC Issues**: Ensure HTTPS in production or allow camera permissions

3. **Model Loading Errors**: Verify model files exist and are not corrupted

4. **Voice Features**: Check microphone permissions and internet connection for OpenAI API

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- Streamlit community
- OpenAI for GPT integration
- Computer vision libraries ecosystem

## 📞 Support

For support and questions, please open an issue on the GitHub repository.</content>
<filePath">/Users/kavinkumar/Kavin/Project/Sownd/fabric-qc-system/README.md