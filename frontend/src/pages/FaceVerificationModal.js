import React, { useState, useRef, useEffect } from "react";
import * as faceapi from "face-api.js";
import * as tf from "@tensorflow/tfjs";
import "@tensorflow/tfjs-backend-webgl";
import { api } from "../api";
import "../styles/FaceVerificationModal.css";

function FaceVerificationModal({ onVerificationSuccess, onCancel, token }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [blinkCount, setBlinkCount] = useState(0);
  const [status, setStatus] = useState("Loading face detection models...");
  const [modelLoaded, setModelLoaded] = useState(false);

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
          throw new Error("Failed to load face detector");
        }
        
        try {
          console.log("Loading faceLandmark68Net...");
          await faceapi.nets.faceLandmark68Net.load(MODEL_URL);
          console.log("✓ faceLandmark68Net loaded");
          setStatus("Loading face expressions...");
        } catch (e) {
          console.error("Error loading faceLandmark68Net:", e);
          throw new Error("Failed to load landmarks");
        }
        
        try {
          console.log("Loading faceExpressionNet...");
          await faceapi.nets.faceExpressionNet.load(MODEL_URL);
          console.log("✓ faceExpressionNet loaded");
        } catch (e) {
          console.error("Error loading faceExpressionNet:", e);
          throw new Error("Failed to load expressions");
        }
        
        setModelLoaded(true);
        setStatus("Models loaded. Initializing camera...");
        console.log("All models loaded successfully");
      } catch (err) {
        console.error("Model loading error:", err);
        setError("Failed to load face detection models. Please check your internet connection.");
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
        console.log("Requesting camera access for face verification...");
        setStatus("Requesting camera access...");
        
        let stream = null;
        
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
            throw modernErr;
          }
        } else if (navigator.webkitGetUserMedia) {
          console.log("Using webkit getUserMedia API");
          stream = await new Promise((resolve, reject) => {
            navigator.webkitGetUserMedia(
              { video: true, audio: false },
              resolve,
              reject
            );
          });
        } else if (navigator.mozGetUserMedia) {
          console.log("Using moz getUserMedia API");
          stream = await new Promise((resolve, reject) => {
            navigator.mozGetUserMedia(
              { video: true, audio: false },
              resolve,
              reject
            );
          });
        }
        
        if (videoRef.current && stream) {
          videoRef.current.srcObject = stream;
          
          videoRef.current.onloadedmetadata = () => {
            console.log("✓ Video stream ready, resolution:", videoRef.current.videoWidth, "x", videoRef.current.videoHeight);
            setStatus("Camera ready. Position your face and blink once to verify.");
            setLoading(false);
          };
          
          videoRef.current.onplay = () => {
            console.log("✓ Video started playing");
          };
          
          videoRef.current.onerror = (err) => {
            console.error("Video element error:", err);
            setError("Error loading video stream");
            setLoading(false);
          };
          
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
        
        let errorMessage = "Camera access error";
        
        if (err.name === "NotAllowedError" || err.message?.includes("Permission")) {
          errorMessage = "Camera permission denied. Please allow camera access.";
        } else if (err.name === "NotFoundError" || err.message?.includes("No camera")) {
          errorMessage = "No camera found or camera is in use by another app.";
        } else if (err.name === "NotReadableError") {
          errorMessage = "Camera is already in use. Close other apps using the camera.";
        }
        
        setError(errorMessage);
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
    const BLINK_COOLDOWN = 200;

    const captureFaceImage = async () => {
      try {
        setStatus("Capturing face...");
        const video = videoRef.current;
        
        if (!video || !video.videoWidth) {
          console.error("Video not ready for capture");
          setError("Video not ready. Please try again.");
          return;
        }

        const tempCanvas = document.createElement("canvas");
        tempCanvas.width = video.videoWidth;
        tempCanvas.height = video.videoHeight;
        const ctx = tempCanvas.getContext("2d");
        
        if (!ctx) {
          throw new Error("Failed to get canvas context");
        }
        
        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
        
        const imageData = tempCanvas.toDataURL("image/jpeg", 0.95);
        if (!imageData || !imageData.includes(",")) {
          throw new Error("Failed to capture video frame");
        }

        const base64Image = imageData.split(",")[1];
        if (!base64Image) {
          throw new Error("Invalid base64 image data");
        }

        console.log("Captured image size:", base64Image.length);
        setStatus("Sending face for verification...");

        // Call API to verify face
        try {
          const response = await api.verifyFaceForVoting(base64Image, token);
          console.log("Verification response:", response);

          if (response.verified || response.is_match || response.message) {
            setStatus("✓ Face verified successfully!");
            console.log("Face verified, calling success callback");
            setTimeout(() => {
              onVerificationSuccess();
            }, 1500);
          } else {
            setError("Face verification failed. Please try again.");
            setStatus("Camera ready. Position your face and blink once to verify.");
            isCapturing = false;
          }
        } catch (apiErr) {
          console.error("Face verification API error:", apiErr);
          const errorMsg = apiErr.message || "Unknown error";
          
          if (errorMsg.includes("Face not recognized")) {
            setError("Your face is not recognized. Please register your face first on the login page.");
          } else if (errorMsg.includes("does not match")) {
            setError("Your face does not match the registered face. Please try again.");
          } else if (errorMsg.includes("already voted")) {
            setError("You have already voted in this election.");
          } else if (errorMsg.includes("haven't registered")) {
            setError("You need to register your face first. Please go back and register.");
          } else {
            setError("Error verifying face: " + errorMsg);
          }
          
          setStatus("Camera ready. Position your face and blink once to verify.");
          isCapturing = false;
        }
      } catch (err) {
        console.error("Face capture error:", err);
        setError("Error capturing face: " + (err.message || "Unknown error"));
        setStatus("Camera ready. Position your face and blink once to verify.");
        isCapturing = false;
      }
    };

    const detectFace = async () => {
      try {
        if (isCapturing) {
          console.log("Already capturing, skipping detection");
          return;
        }
        
        const video = videoRef.current;
        if (!video || !video.videoWidth || !video.videoHeight) {
          console.log("Video not ready:", {
            hasVideo: !!video,
            videoWidth: video?.videoWidth,
            videoHeight: video?.videoHeight,
            readyState: video?.readyState,
            networkState: video?.networkState
          });
          return;
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
          console.log("No face detected in video");
          setStatus("Waiting for face... Please position your face clearly. Adjust lighting if needed.");
          return;
        }

        console.log("Face detected! Detections:", detections.length);

        const detection = detections[0];
        const landmarks = detection.landmarks;

        const leftEye = landmarks.getLeftEye();
        const rightEye = landmarks.getRightEye();
        
        if (!leftEye || !rightEye || leftEye.length < 4 || rightEye.length < 4) {
          // Don't return error if eyes can't be detected - just skip blink detection for this frame
          return;
        }

        const leftEyeAR = 
          (getDistance(leftEye[1], leftEye[5]) + getDistance(leftEye[2], leftEye[4])) /
          (2 * getDistance(leftEye[0], leftEye[3]));
          
        const rightEyeAR = 
          (getDistance(rightEye[1], rightEye[5]) + getDistance(rightEye[2], rightEye[4])) /
          (2 * getDistance(rightEye[0], rightEye[3]));

        const eyeAspectRatio = (leftEyeAR + rightEyeAR) / 2;
        const currentTime = Date.now();

        console.log("Eye Aspect Ratio:", eyeAspectRatio.toFixed(3), "Previous Open:", previousEyeOpenState, "Time since last blink:", currentTime - lastBlinkTime);

        if (eyeAspectRatio < 0.25 && previousEyeOpenState && (currentTime - lastBlinkTime) > BLINK_COOLDOWN) {
          blinks++;
          setBlinkCount(blinks);
          previousEyeOpenState = false;
          lastBlinkTime = currentTime;
          console.log("✓ Blink detected! Count:", blinks);

          if (blinks === 1) {
            console.log("Initiating face capture...");
            isCapturing = true;
            await captureFaceImage();
            // Don't reset here, let the capture function handle it
          }
        } else if (eyeAspectRatio > 0.35) {
          previousEyeOpenState = true;
        }

        // Draw detection on canvas
        const canvas = canvasRef.current;
        if (canvas && videoRef.current) {
          canvas.width = videoRef.current.videoWidth;
          canvas.height = videoRef.current.videoHeight;
          const ctx = canvas.getContext("2d");

          if (ctx) {
            // Clear canvas
            ctx.fillStyle = "rgba(0, 0, 0, 0)";
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const box = detection.detection.box;
            ctx.strokeStyle = "#00ff00";
            ctx.lineWidth = 2;
            ctx.strokeRect(box.x, box.y, box.width, box.height);

            ctx.fillStyle = "#00ff00";
            landmarks.positions.forEach(point => {
              ctx.beginPath();
              ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
              ctx.fill();
            });

            ctx.fillStyle = "#fff";
            ctx.font = "16px Arial";
            ctx.fillText(`Blinks: ${blinks}/1`, 10, 30);
          }
        }
      } catch (err) {
        console.error("Face detection error:", err);
        // Don't update status on every error to reduce spam
        if (err.message && !err.message.includes("Aborted")) {
          console.error("Detection error details:", err.message);
        }
      }
    };

    detectionInterval = setInterval(detectFace, 100);

    return () => clearInterval(detectionInterval);
  }, [modelLoaded, token, onVerificationSuccess]);

  const getDistance = (point1, point2) => {
    const dx = point1.x - point2.x;
    const dy = point1.y - point2.y;
    return Math.sqrt(dx * dx + dy * dy);
  };

  return (
    <div className="face-verification-overlay">
      <div className="face-verification-modal">
        <div className="face-verification-header">
          <h2>👤 Face Verification</h2>
          <button className="close-btn" onClick={onCancel} title="Cancel">
            ✕
          </button>
        </div>

        {error && <div className="verification-error">{error}</div>}

        <div className="verification-camera-wrapper">
          {loading && (
            <div className="verification-loading">
              <div className="verification-spinner"></div>
              <p>{status}</p>
            </div>
          )}
          <video
            ref={videoRef}
            autoPlay
            muted
            playsInline
            className="verification-video"
          />
          <canvas ref={canvasRef} className="verification-canvas" />
        </div>

        <div className="verification-info">
          <p className="verification-counter">
            👁️ Blinks: <span>{blinkCount}/1</span>
          </p>
          <p className="verification-status">{status}</p>
        </div>

        <div className="verification-instructions">
          <h4>Instructions:</h4>
          <ul>
            <li>Position your face clearly in the camera</li>
            <li>Ensure good lighting</li>
            <li>Blink once to verify your identity</li>
          </ul>
        </div>

        <button className="cancel-verification-btn" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </div>
  );
}

export default FaceVerificationModal;
