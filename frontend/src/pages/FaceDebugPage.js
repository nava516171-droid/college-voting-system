import React, { useState, useRef, useEffect } from "react";
import * as faceapi from "face-api.js";
import * as tf from "@tensorflow/tfjs";
import "@tensorflow/tfjs-backend-webgl";

function FaceDebugPage() {
  const [status, setStatus] = useState("Starting debug...");
  const [logs, setLogs] = useState([]);
  const videoRef = useRef(null);

  const addLog = (message) => {
    console.log(message);
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${message}`]);
  };

  useEffect(() => {
    const runDiagnostics = async () => {
      try {
        addLog("=== FACE DETECTION DIAGNOSTICS ===");
        addLog(`Browser: ${navigator.userAgent}`);
        addLog(`Platform: ${navigator.platform}`);
        
        // Setup TensorFlow backend
        addLog("Setting up TensorFlow backend...");
        try {
          await tf.setBackend("webgl");
          await tf.ready();
          addLog(`✓ TensorFlow.js backend ready: ${tf.getBackend()}`);
        } catch (tfError) {
          addLog(`⚠ WebGL backend setup warning: ${tfError.message}`);
          addLog("Falling back to CPU backend...");
          await tf.setBackend("cpu");
          await tf.ready();
          addLog(`✓ Fallback backend ready: ${tf.getBackend()}`);
        }
        
        // Check if face-api is loaded
        addLog(`face-api version: ${faceapi ? "Loaded" : "NOT loaded"}`);
        
        // Check if we have camera support
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          addLog("❌ Camera API NOT supported!");
          setStatus("Camera not supported");
          return;
        }
        addLog("✓ Camera API supported");

        // Check if we have tf.js
        if (typeof tf === 'undefined') {
          addLog("⚠ TensorFlow.js might not be loaded");
        } else {
          addLog("✓ TensorFlow.js loaded");
        }

        // Try to load models
        addLog("\nLoading face detection models...");
        const MODEL_URL = "https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/";
        
        try {
          addLog("Loading tinyFaceDetector model...");
          await faceapi.nets.tinyFaceDetector.load(MODEL_URL);
          addLog("✓ tinyFaceDetector loaded successfully");
        } catch (e) {
          addLog(`❌ Failed to load tinyFaceDetector: ${e.message}`);
          throw e;
        }

        try {
          addLog("Loading faceLandmark68Net model...");
          await faceapi.nets.faceLandmark68Net.load(MODEL_URL);
          addLog("✓ faceLandmark68Net loaded successfully");
        } catch (e) {
          addLog(`❌ Failed to load faceLandmark68Net: ${e.message}`);
          throw e;
        }

        try {
          addLog("Loading faceExpressionNet model...");
          await faceapi.nets.faceExpressionNet.load(MODEL_URL);
          addLog("✓ faceExpressionNet loaded successfully");
        } catch (e) {
          addLog(`⚠ Warning loading faceExpressionNet: ${e.message}`);
          // Don't throw, this is optional
        }

        addLog("\n✓ All essential models loaded!");

        // Try to access camera
        addLog("\nRequesting camera access...");
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user" }
        });
        addLog("✓ Camera access granted");

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.onloadedmetadata = () => {
            addLog(`✓ Video stream ready: ${videoRef.current.videoWidth}x${videoRef.current.videoHeight}`);
            
            // Test detection
            setTimeout(testDetection, 1000);
          };
        }

        setStatus("Setup complete. Testing face detection...");
      } catch (err) {
        addLog(`❌ Error: ${err.message}`);
        setStatus(`Error: ${err.message}`);
      }
    };

    const testDetection = async () => {
      try {
        if (!videoRef.current || !videoRef.current.srcObject) {
          addLog("❌ Video not available for detection");
          return;
        }

        addLog("\nTesting face detection...");
        const detections = await faceapi
          .detectAllFaces(videoRef.current, new faceapi.TinyFaceDetectorOptions())
          .withFaceLandmarks()
          .withFaceExpressions();

        if (detections.length === 0) {
          addLog("⚠ No faces detected in frame (this might be normal if no face is visible)");
        } else {
          addLog(`✓ Detected ${detections.length} face(s)`);
          detections.forEach((detection, i) => {
            addLog(`  Face ${i + 1}: confidence=${detection.detection.score.toFixed(2)}`);
          });
        }

        setStatus("✓ Face detection working!");
      } catch (err) {
        addLog(`❌ Detection error: ${err.message}`);
        setStatus(`Detection error: ${err.message}`);
      }
    };

    runDiagnostics();

    return () => {
      // Cleanup video stream
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "monospace", backgroundColor: "#1e1e1e", color: "#00ff00", minHeight: "100vh" }}>
      <h1>Face Detection Diagnostics</h1>
      <p>Status: {status}</p>
      
      <div style={{ marginTop: "20px", marginBottom: "20px" }}>
        <h3>Video Feed:</h3>
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          style={{
            width: "100%",
            maxWidth: "400px",
            border: "2px solid #00ff00",
            borderRadius: "5px"
          }}
        />
      </div>

      <div style={{
        backgroundColor: "#0d0d0d",
        border: "1px solid #00ff00",
        padding: "10px",
        borderRadius: "5px",
        maxHeight: "400px",
        overflowY: "auto",
        fontSize: "12px",
        lineHeight: "1.5"
      }}>
        <h3>Debug Logs:</h3>
        {logs.map((log, i) => (
          <div key={i}>{log}</div>
        ))}
      </div>

      <div style={{ marginTop: "20px", fontSize: "12px", color: "#888" }}>
        <p>If you see ❌ errors, that's what's preventing face detection from working on your phone.</p>
        <p>Make sure to:</p>
        <ul>
          <li>Allow camera access when prompted</li>
          <li>Check your internet connection (models are loaded from CDN)</li>
          <li>Try on a device with a working camera</li>
          <li>Use HTTPS if on a secure connection</li>
        </ul>
      </div>
    </div>
  );
}

export default FaceDebugPage;
