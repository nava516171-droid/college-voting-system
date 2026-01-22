import React, { useState, useRef, useEffect } from "react";
import * as faceapi from "face-api.js";
import * as tf from "@tensorflow/tfjs";
import "@tensorflow/tfjs-backend-webgl";
import { api } from "../api";
import "../styles/FaceCapturePage.css";

function FaceCapturePage({ onFaceSuccess, userEmail, token }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [blinkCount, setBlinkCount] = useState(0);
  const [faceCaptured, setFaceCaptured] = useState(false);
  const [status, setStatus] = useState("Loading face detection models...");
  const [modelLoaded, setModelLoaded] = useState(false);

  // Check camera API support on mount
  useEffect(() => {
    console.log("=== FACE CAPTURE PAGE INITIALIZED ===");
    console.log("Checking camera API support...");
    
    const hasCameraAPI = 
      (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === "function") ||
      navigator.webkitGetUserMedia ||
      navigator.mozGetUserMedia ||
      navigator.getUserMedia;
    
    console.log("Camera API Support:", {
      mediaDevices: !!navigator.mediaDevices,
      getUserMedia: !!navigator.getUserMedia,
      webkitGetUserMedia: !!navigator.webkitGetUserMedia,
      mozGetUserMedia: !!navigator.mozGetUserMedia,
      hasAnyAPI: !!hasCameraAPI,
      protocol: window.location.protocol,
      userAgent: navigator.userAgent
    });
    
    if (!hasCameraAPI) {
      console.error("No camera API available on this browser!");
      setError(
        "❌ CAMERA NOT SUPPORTED\n\n" +
        "Your browser does not support camera access.\n\n" +
        "Supported browsers:\n" +
        "- Chrome/Chromium\n" +
        "- Firefox\n" +
        "- Safari 11+\n" +
        "- Edge\n\n" +
        "Your browser: " + navigator.userAgent.substring(0, 100)
      );
      setLoading(false);
    }
  }, []);

  // Load face detection models
  useEffect(() => {
    const loadModels = async () => {
      try {
        // Set up TensorFlow backend
        console.log("Setting up TensorFlow backend...");
        await tf.setBackend("webgl");
        await tf.ready();
        console.log("✓ TensorFlow backend ready:", tf.getBackend());
        
        setStatus("Loading face detection models...");
        console.log("Starting to load models from CDN...");
        
        const MODEL_URL = "https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/";
        
        try {
          console.log("Loading tinyFaceDetector...");
          await faceapi.nets.tinyFaceDetector.load(MODEL_URL);
          console.log("✓ tinyFaceDetector loaded");
          setStatus("Loading face landmarks...");
        } catch (e) {
          console.error("Error loading tinyFaceDetector:", e);
          throw new Error("Failed to load face detector: " + e.message);
        }
        
        try {
          console.log("Loading faceLandmark68Net...");
          await faceapi.nets.faceLandmark68Net.load(MODEL_URL);
          console.log("✓ faceLandmark68Net loaded");
          setStatus("Loading face expressions...");
        } catch (e) {
          console.error("Error loading faceLandmark68Net:", e);
          throw new Error("Failed to load landmarks: " + e.message);
        }
        
        try {
          console.log("Loading faceExpressionNet...");
          await faceapi.nets.faceExpressionNet.load(MODEL_URL);
          console.log("✓ faceExpressionNet loaded");
        } catch (e) {
          console.error("Error loading faceExpressionNet:", e);
          throw new Error("Failed to load expressions: " + e.message);
        }
        
        setModelLoaded(true);
        setStatus("Models loaded. Initializing camera...");
        console.log("All models loaded successfully");
      } catch (err) {
        console.error("Model loading error:", err);
        setError("Failed to load face detection models: " + err.message + ". Please check your internet connection and try again.");
        setLoading(false);
      }
    };

    loadModels();
  }, []);

  // Start video stream
  useEffect(() => {
    if (!modelLoaded) return;

    const startVideo = async () => {
      try {
        console.log("Requesting camera access...");
        console.log("navigator object:", navigator);
        console.log("navigator.mediaDevices:", navigator.mediaDevices);
        console.log("navigator.webkitGetUserMedia:", navigator.webkitGetUserMedia);
        console.log("navigator.mozGetUserMedia:", navigator.mozGetUserMedia);
        console.log("navigator.getUserMedia:", navigator.getUserMedia);
        console.log("window.location.protocol:", window.location.protocol);
        setStatus("Requesting camera access...");
        
        let stream = null;
        
        // Try modern API first
        if (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === "function") {
          console.log("Using modern mediaDevices API");
          try {
            const constraints = {
              video: { 
                width: { ideal: 640 }, 
                height: { ideal: 480 },
                facingMode: "user"
              },
              audio: false
            };
            
            console.log("Getting camera stream with constraints:", constraints);
            stream = await navigator.mediaDevices.getUserMedia(constraints);
            console.log("✓ Camera access granted via mediaDevices");
          } catch (modernErr) {
            console.error("Modern API failed:", modernErr);
            console.log("Trying fallback APIs...");
            throw modernErr;
          }
        } 
        // Try webkit fallback (Safari, older Chrome)
        else if (navigator.webkitGetUserMedia) {
          console.log("Using webkit getUserMedia API");
          stream = await new Promise((resolve, reject) => {
            navigator.webkitGetUserMedia(
              { video: true, audio: false },
              resolve,
              reject
            );
          });
          console.log("✓ Camera access granted via webkit API");
        }
        // Try moz fallback (Firefox)
        else if (navigator.mozGetUserMedia) {
          console.log("Using moz getUserMedia API");
          stream = await new Promise((resolve, reject) => {
            navigator.mozGetUserMedia(
              { video: true, audio: false },
              resolve,
              reject
            );
          });
          console.log("✓ Camera access granted via moz API");
        }
        // Try generic fallback
        else if (navigator.getUserMedia) {
          console.log("Using generic getUserMedia API");
          stream = await new Promise((resolve, reject) => {
            navigator.getUserMedia(
              { video: true, audio: false },
              resolve,
              reject
            );
          });
          console.log("✓ Camera access granted via generic API");
        } 
        // No API available
        else {
          const debugInfo = {
            hasMediaDevices: !!navigator.mediaDevices,
            hasGetUserMedia: !!navigator.getUserMedia,
            hasWebKit: !!navigator.webkitGetUserMedia,
            hasMoz: !!navigator.mozGetUserMedia,
            protocol: window.location.protocol,
            userAgent: navigator.userAgent
          };
          
          throw new Error(
            "Camera API not available in your browser.\n\n" +
            "Debug: " + JSON.stringify(debugInfo, null, 2) + "\n\n" +
            "Possible causes:\n" +
            "1. Browser doesn't support camera access\n" +
            "2. Phone security settings blocking camera\n" +
            "3. HTTPS may be required (on some phones)\n" +
            "4. Camera permissions not granted\n\n" +
            "Try:\n" +
            "- Chrome or Firefox mobile\n" +
            "- Check phone camera permissions in Settings\n" +
            "- Refresh and try again\n" +
            "- Use a different browser"
          );
        }
        
        if (videoRef.current && stream) {
          videoRef.current.srcObject = stream;
          
          // Wait for video to be ready
          videoRef.current.onloadedmetadata = () => {
            console.log("✓ Video stream ready, resolution:", videoRef.current.videoWidth, "x", videoRef.current.videoHeight);
            setStatus("Camera ready. Please blink once to capture your face.");
            setLoading(false);
          };
          
          videoRef.current.onerror = (err) => {
            console.error("Video element error:", err);
            setError("Error loading video stream: " + (err?.message || "Unknown error"));
            setLoading(false);
          };
          
          // Timeout if video doesn't load
          setTimeout(() => {
            if (videoRef.current && !videoRef.current.videoWidth) {
              console.error("Video stream loaded but no frames received");
              setError("Video stream loaded but no camera frames received. Try refreshing.");
              setLoading(false);
            }
          }, 3000);
        }
      } catch (err) {
        console.error("Camera error:", err);
        console.error("Error name:", err.name);
        console.error("Error message:", err.message);
        console.error("Error stack:", err.stack);
        
        let errorMessage = "Camera access error";
        
        if (err.message && err.message.includes("Camera API not available")) {
          errorMessage = err.message;
        } else if (err.message && err.message.includes("undefined")) {
          errorMessage = "❌ CAMERA API NOT FOUND\n\nThe camera API is not available in your browser.\n\nThis typically means:\n1. Browser doesn't expose camera access\n2. Phone is in restricted mode\n3. HTTPS is required\n\nTry:\n- Chrome or Firefox mobile\n- Restart browser\n- Check if URL is http:// or https://\n- Allow camera permissions in phone settings";
        } else if (err.name === "NotAllowedError" || err.message?.includes("Permission")) {
          errorMessage = "❌ CAMERA PERMISSION DENIED\n\nPlease:\n1. Go to phone Settings\n2. Find app permissions\n3. Grant camera permission to this browser\n4. Close and reopen the page\n5. Try a different browser if it still fails";
        } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError" || err.message?.includes("No camera")) {
          errorMessage = "❌ NO CAMERA FOUND\n\nYour device either:\n- Has no camera\n- Camera is disabled in settings\n- Camera is in use by another app\n\nCheck your phone settings and close other camera apps.";
        } else if (err.name === "NotReadableError" || err.message?.includes("already in use")) {
          errorMessage = "❌ CAMERA ALREADY IN USE\n\nAnother app is using the camera.\n\nClose:\n- Video call apps (Zoom, Teams)\n- Camera app\n- Other video apps\n\nThen refresh this page.";
        } else if (err.name === "SecurityError" || err.message?.includes("Security")) {
          errorMessage = "❌ SECURITY ERROR\n\nCamera access is blocked by security policy.\n\nTry:\n- Using HTTPS (if available)\n- Different browser (Chrome or Firefox)\n- Check phone security settings\n- Allow camera in privacy settings";
        } else if (err.name === "TypeError" || err.message?.includes("TypeError")) {
          errorMessage = "❌ BROWSER COMPATIBILITY ERROR\n\nYour browser may not fully support camera access.\n\nTry:\n- Chrome or Firefox (latest version)\n- Updating your browser\n- Using a different device\n- Check browser compatibility";
        }
        
        setError(errorMessage + "\n\nDebug: " + (err.message || err.name || "Unknown error"));
        setLoading(false);
      }
    };

    startVideo();

    return () => {
      const video = videoRef.current;
      if (video && video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, [modelLoaded]);

  // Detect face and eye blinks
  useEffect(() => {
    if (!modelLoaded || !videoRef.current) return;

    let previousEyeOpenState = true;
    let blinks = 0;
    let detectionInterval;
    let isCapturing = false;
    let lastBlinkTime = 0;
    const BLINK_COOLDOWN = 200; // milliseconds between blinks

    const detectFace = async () => {
      try {
        if (isCapturing) return; // Prevent multiple captures
        
        // Check if video is ready
        const video = videoRef.current;
        if (!video || !video.videoWidth || !video.videoHeight) {
          return; // Video not ready yet
        }
        
        // Try with progressively lower thresholds if face not detected
        let detections = [];
        const thresholds = [0.15, 0.1, 0.05]; // Progressive thresholds (more lenient)
        
        for (let threshold of thresholds) {
          try {
            const options = new faceapi.TinyFaceDetectorOptions({
              inputSize: 416,
              scoreThreshold: threshold
            });
            detections = await faceapi
              .detectAllFaces(video, options)
              .withFaceLandmarks()
              .withFaceExpressions();
            
            if (detections.length > 0) break; // Face found, exit loop
          } catch (detectionErr) {
            console.log(`Detection failed at threshold ${threshold}:`, detectionErr.message);
            continue; // Try next threshold
          }
        }

        if (detections.length === 0) {
          setStatus("Waiting for face... Please position your face clearly. Adjust lighting if needed.");
          return;
        }

        const detection = detections[0];
        const landmarks = detection.landmarks;

        // Calculate eye aspect ratio to detect blinks
        const leftEye = landmarks.getLeftEye();
        const rightEye = landmarks.getRightEye();
        
        if (!leftEye || !rightEye || leftEye.length < 4 || rightEye.length < 4) {
          // Don't return error if eyes can't be detected - just skip blink detection for this frame
          return;
        }

        // Calculate more accurate eye aspect ratio
        const leftEyeAR = 
          (getDistance(leftEye[1], leftEye[5]) + getDistance(leftEye[2], leftEye[4])) /
          (2 * getDistance(leftEye[0], leftEye[3]));
          
        const rightEyeAR = 
          (getDistance(rightEye[1], rightEye[5]) + getDistance(rightEye[2], rightEye[4])) /
          (2 * getDistance(rightEye[0], rightEye[3]));

        const eyeAspectRatio = (leftEyeAR + rightEyeAR) / 2;
        const currentTime = Date.now();

        // If eye aspect ratio is low, eyes are closed (blink detected)
        // Use more lenient threshold and add cooldown to prevent multiple counts
        if (eyeAspectRatio < 0.25 && previousEyeOpenState && (currentTime - lastBlinkTime) > BLINK_COOLDOWN) {
          blinks++;
          setBlinkCount(blinks);
          previousEyeOpenState = false;
          lastBlinkTime = currentTime;
          console.log("Blink detected! Count:", blinks);

          if (blinks === 1) {
            // One blink detected, capture face
            isCapturing = true;
            await captureFace(detection);
            setBlinkCount(0);
            blinks = 0;
            isCapturing = false;
          }
        } else if (eyeAspectRatio > 0.35) {
          previousEyeOpenState = true;
        }

        // Draw detection on canvas for visual feedback
        const canvas = canvasRef.current;
        if (canvas) {
          canvas.width = videoRef.current.videoWidth;
          canvas.height = videoRef.current.videoHeight;
          const ctx = canvas.getContext("2d");

          // Draw face box
          const box = detection.detection.box;
          ctx.strokeStyle = "#00ff00";
          ctx.lineWidth = 2;
          ctx.strokeRect(box.x, box.y, box.width, box.height);

          // Draw landmarks
          ctx.fillStyle = "#00ff00";
          landmarks.positions.forEach(point => {
            ctx.beginPath();
            ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
            ctx.fill();
          });

          // Draw status text
          ctx.fillStyle = "#fff";
          ctx.font = "16px Arial";
          ctx.fillText(`Blinks: ${blinks}/2`, 10, 30);
        }
      } catch (err) {
        console.error("Face detection error:", err);
      }
    };

    detectionInterval = setInterval(detectFace, 100);

    return () => clearInterval(detectionInterval);
  }, [modelLoaded]); // captureFace is defined within this effect, no external dependency

  const getDistance = (point1, point2) => {
    const dx = point1.x - point2.x;
    const dy = point1.y - point2.y;
    return Math.sqrt(dx * dx + dy * dy);
  };

  const captureFace = async (detection) => {
    try {
      setStatus("Face captured! Uploading...");
      setFaceCaptured(true);

      const video = videoRef.current;
      if (!video) {
        throw new Error("Video not available");
      }

      // Get face detection box for cropping
      const box = detection.detection.box;
      
      // Add padding around detected face (20% on each side)
      const padding = 0.2;
      const x = Math.max(0, box.x - box.width * padding);
      const y = Math.max(0, box.y - box.height * padding);
      const width = Math.min(video.videoWidth - x, box.width * (1 + padding * 2));
      const height = Math.min(video.videoHeight - y, box.height * (1 + padding * 2));

      // Create canvas with cropped face region
      const tempCanvas = document.createElement("canvas");
      tempCanvas.width = width;
      tempCanvas.height = height;
      const ctx = tempCanvas.getContext("2d");
      
      // Draw the cropped video frame focusing on face
      ctx.drawImage(
        video,
        x, y, width, height,  // Source region
        0, 0, width, height   // Destination in canvas
      );
      
      // Use higher quality JPEG (0.98) for better face detection
      const imageData = tempCanvas.toDataURL("image/jpeg", 0.98);
      if (!imageData || !imageData.includes(",")) {
        throw new Error("Failed to capture video frame");
      }

      const base64Image = imageData.split(",")[1];
      if (!base64Image) {
        throw new Error("Invalid base64 image data");
      }

      console.log("Captured face image size:", base64Image.length, "bytes");
      console.log("Face region:", { x, y, width, height });

      // Send to backend
      const response = await api.registerFace(base64Image, token);

      if (response.message || response.status === "success") {
        setStatus("✓ Face successfully captured! Moving to OTP verification...");
        setTimeout(() => {
          onFaceSuccess();
        }, 2000);
      } else {
        setError(response.detail || "Failed to register face");
        setFaceCaptured(false);
        setStatus("Please try again. Blink twice to capture.");
      }
    } catch (err) {
      console.error("Face capture error:", err);
      setError("Error uploading face: " + (err.message || "Unknown error"));
      setFaceCaptured(false);
      setStatus("Please try again. Blink twice to capture.");
    }
  };

  return (
    <div className="face-capture-container">
      <div className="face-capture-card">
        <h2>👤 Face Authentication</h2>
        <p className="face-subtitle">Blink twice to capture your face</p>

        {error && <div className="face-error">{error}</div>}

        <div className="camera-wrapper">
          {loading && (
            <div className="face-loading">
              <div className="spinner"></div>
              <p>{status}</p>
            </div>
          )}
          <video
            ref={videoRef}
            autoPlay
            muted
            playsInline
            className={`face-video ${faceCaptured ? "captured" : ""}`}
          />
          <canvas ref={canvasRef} className="face-canvas" />
        </div>

        <div className="face-info">
          <p className="blink-counter">
            👁️ Blinks Detected: <span className="blink-count">{blinkCount}/1</span>
          </p>
          <p className="face-status">{status}</p>
        </div>

        <div className="face-instructions">
          <h4>Instructions:</h4>
          <ul>
            <li>Position your face clearly in front of the camera</li>
            <li>Make sure the camera can see your full face</li>
            <li>Blink your eyes once to capture your face</li>
            <li>Ensure good lighting for best results</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default FaceCapturePage;
