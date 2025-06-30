#!/usr/bin/env python
import requests
import os
import time

print("Testing WhisperAI transcription service...")

# Path to the test audio file
audio_file_path = os.path.join(os.getcwd(), "test\short_test.wav")

if not os.path.exists(audio_file_path):
    print(f"Error: Test audio file not found at {audio_file_path}")
    exit(1)

# First test the health endpoint
print("Testing health endpoint...")
try:
    response = requests.get("http://localhost:5000/")
    print(f"Health endpoint response: {response.text}")
except Exception as e:
    print(f"Error accessing health endpoint: {str(e)}")
    exit(1)

# Now test the transcription endpoint
print("\nTesting transcription endpoint...")
print(f"Sending file: {audio_file_path}")

# Prepare the file for upload
files = {
    'file': (os.path.basename(audio_file_path), open(audio_file_path, 'rb'), 'audio/wav')
}

try:
    # Set a longer timeout (60 seconds)
    start_time = time.time()
    print("Sending request to transcription endpoint...")
    response = requests.post("http://localhost:5000/whisper", files=files, timeout=60)
    elapsed_time = time.time() - start_time
    
    print(f"Request completed in {elapsed_time:.2f} seconds")
    
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        print("\nTranscription Result:")
        print(f"Filename: {result.get('filename', 'unknown')}")
        print(f"Text: {result.get('text', 'No transcription available')}")
    else:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
except requests.exceptions.Timeout:
    print("Error: Request timed out after 60 seconds")
except Exception as e:
    print(f"Error occurred while testing the service: {str(e)}")
finally:
    # Make sure the file is closed
    files['file'][1].close()

print("\nTest completed.")
