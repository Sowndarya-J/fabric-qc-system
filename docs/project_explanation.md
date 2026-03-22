# Fabric QC System Project Explanation

This document explains each module in the Fabric Quality Control System project, including where it is used, why it was chosen, and how it functions. This is designed to help new freshers understand the project structure and purpose.

## Core Application Files

### Home.py
**Where**: Root directory  
**Why**: This is the main entry point of the application, providing navigation to all other pages.  
**How**: It uses Streamlit's option_menu to create a horizontal navigation bar with icons for each page. It applies a dark theme and handles user login status display. The file loads different page files dynamically based on the selected menu option.

### app.py
**Where**: Root directory  
**Why**: This serves as an alternative main application file that combines login functionality with real-time webcam detection.  
**How**: It handles user authentication, admin user management, and sets up the webcam streaming interface using WebRTC. It loads the YOLO model and processes video frames for defect detection in real-time.

### theme.py
**Where**: Root directory  
**Why**: To provide a consistent dark theme across the entire application.  
**How**: It contains CSS styles that are injected into Streamlit pages using st.markdown with unsafe_allow_html. This creates a uniform dark color scheme for better user experience.

## Page Modules (in pages/ directory)

### 1_Login.py
**Where**: pages/ directory  
**Why**: To authenticate users before they can access the system's features.  
**How**: It displays a login form where users enter username and password. It checks credentials against the users.json file and sets session state variables for logged-in status and user role.

### 2_Webcam_Realtime.py
**Where**: pages/ directory  
**Why**: To perform live fabric inspection using the device's camera.  
**How**: It uses WebRTC streaming to capture video from the webcam, processes frames with the YOLO model at specified intervals, detects defects, and displays results in real-time with bounding boxes and confidence scores.

### 3_Image_Upload.py
**Where**: pages/ directory  
**Why**: To analyze uploaded fabric images for defects in batch processing.  
**How**: Users can upload multiple images, which are then processed by the YOLO model. It generates detection results, heatmaps, and allows saving inspection data to the database.

### 4_Admin_Dashboard.py
**Where**: pages/ directory  
**Why**: To provide administrative functions like user management and system monitoring.  
**How**: It displays user lists, allows adding/deleting users, shows inspection statistics, and provides system overview metrics for administrators.

### 5_Model_Metrics.py
**Where**: pages/ directory  
**Why**: To monitor and analyze the performance of the defect detection model.  
**How**: It loads inspection results from the database and CSV files, calculates metrics like accuracy, precision, and displays charts showing model performance over time.

### 7_Fabric_Assistant.py
**Where**: pages/ directory  
**Why**: To provide AI-powered assistance for fabric-related queries and quality control guidance.  
**How**: It integrates with OpenAI's GPT model to answer questions about fabrics and defects. It includes voice input/output capabilities using speech recognition and text-to-speech libraries.

## Utility and Data Files

### utils.py
**Where**: Root directory  
**Why**: To centralize common functions used across the application.  
**How**: It contains functions for user management (load/save users), database operations (SQLite for inspections), model loading (YOLO), image processing, PDF report generation, email sending, and various helper functions like severity calculation and defect recommendations.

### users.json
**Where**: Root directory  
**Why**: To store user credentials and roles securely.  
**How**: It contains a JSON object with usernames as keys and objects containing password hashes and roles as values. This file is loaded by utils.py functions for authentication.

### results.csv
**Where**: Root directory  
**Why**: To store inspection results in a simple, readable format for analysis.  
**How**: It contains CSV data with columns for inspection details like date, defect counts, confidence scores, etc. This is used by the Model Metrics page for performance analysis.

## Model and Training Files

### best.pt
**Where**: Root directory  
**Why**: This is the custom-trained YOLO model weights file optimized for fabric defect detection.  
**How**: It was created by training the YOLOv8 model on a dataset of fabric images with annotated defects. The model is loaded by the get_model() function in utils.py and used for inference on new images.

### yolov8n.pt
**Where**: Root directory  
**Why**: This is the pre-trained YOLOv8 nano model provided by Ultralytics as a starting point.  
**How**: It contains weights pre-trained on the COCO dataset. It can be used as a fallback or for transfer learning when training the custom model. The application can switch between this and best.pt based on configuration.

## Configuration and Deployment Files

### requirements.txt
**Where**: Root directory  
**Why**: To specify all Python dependencies needed to run the application.  
**How**: It lists package names with versions. When pip install -r requirements.txt is run, it installs all necessary libraries like Streamlit, OpenCV, Ultralytics, etc.

### runtime.txt
**Where**: Root directory  
**Why**: To specify the Python version for deployment platforms like Heroku.  
**How**: It contains a single line like "python-3.10" telling the platform which Python version to use.

### packages.txt
**Where**: Root directory  
**Why**: To specify system-level dependencies for deployment.  
**How**: It lists packages like build-essential that need to be installed at the system level before Python packages.

### start.sh
**Where**: Root directory  
**Why**: To provide a simple startup script for running the application.  
**How**: It's a shell script that sets environment variables and runs the Streamlit command to start the server.

## Data Storage

### saved_inspections/ directory
**Where**: Root directory  
**Why**: To store images and reports from inspections for record-keeping.  
**How**: When inspections are performed, detected images with bounding boxes and generated PDF reports are saved here with unique filenames based on timestamps.

### fabric_inspections.db (created automatically)
**Where**: Root directory (created by utils.py)  
**Why**: To store structured inspection data in a relational database.  
**How**: SQLite database created by init_db() function, containing tables for inspections with fields like ID, user, timestamp, defect counts, etc.

## Dataset Information

**Where**: Not stored in the repository (too large), but referenced in training  
**Why**: The model needs training data to learn defect patterns  
**How**: A dataset of fabric images with defects was collected and annotated with bounding boxes. This dataset was used to train the YOLOv8 model to create best.pt. The dataset typically includes various fabric types with common defects like holes, stains, tears, etc.

## YOLOv8 Model Details

**Where**: Implemented through ultralytics library and model files  
**Why**: YOLO (You Only Look Once) is chosen for real-time object detection with high accuracy  
**How**: The ultralytics library provides the YOLOv8 implementation. The nano version (yolov8n) is lightweight for faster inference. The model processes images, outputs bounding boxes with confidence scores for detected defects, and classifies defect types.