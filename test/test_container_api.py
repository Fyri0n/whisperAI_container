#!/usr/bin/env python
import requests
import os
import time
import sys
import json

def test_whisper_api(base_url="http://192.168.0.120:32770"):
    """
    Test the WhisperAI API running in a Docker container
    
    Args:
        base_url: The base URL of the API (default: http://localhost:5001)
    """
    print(f"Testing WhisperAI API at {base_url}")
    
    # Test files paths
    test_dir = os.path.join(os.getcwd(), "test")
    short_test_path = os.path.join(test_dir, "short_test.wav")
    tim_curry_path = os.path.join(test_dir, "TimCurry.wav")
    
    # Check if test files exist
    print("\nChecking test files:")
    for file_path in [short_test_path, tim_curry_path]:
        if os.path.exists(file_path):
            print(f"✓ Found {os.path.basename(file_path)}")
        else:
            print(f"✗ Error: File not found at {file_path}")
            
    # 1. Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✓ Health endpoint response: {json.dumps(health_data, indent=2)}")
            print(f"  • API Status: {health_data.get('status')}")
            print(f"  • Device: {health_data.get('device')}")
            print(f"  • Current Model: {health_data.get('current_model')}")
        else:
            print(f"✗ Error: Health endpoint returned status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Error accessing health endpoint: {str(e)}")
        print("  Make sure the container is running and the port mapping is correct (5001:5000)")
        sys.exit(1)
    
    # 2. Test model endpoint (GET)
    print("\n2. Testing model information endpoint...")
    try:
        response = requests.get(f"{base_url}/model")
        if response.status_code == 200:
            model_data = response.json()
            print(f"✓ Model endpoint response: {json.dumps(model_data, indent=2)}")
            print(f"  • Current Model: {model_data.get('current_model')}")
            print(f"  • Available Models: {', '.join(model_data.get('available_models', []))}")
        else:
            print(f"✗ Error: Model endpoint returned status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Error accessing model endpoint: {str(e)}")
        sys.exit(1)
    
    # 3. Test transcription with short test file
    print("\n3. Testing transcription with short_test.wav...")
    test_transcription(base_url, short_test_path)
    
    # 4. Test transcription with TimCurry.wav (longer file)
    print("\n4. Testing transcription with TimCurry.wav...")
    test_transcription(base_url, tim_curry_path)
    
    # 5. Optional: Test model switching
    current_model = model_data.get('current_model')
    target_model = "tiny" if current_model != "tiny" else "base"
    
    print(f"\n5. Testing model switching from '{current_model}' to '{target_model}'...")
    try:
        response = requests.post(
            f"{base_url}/model", 
            json={"model": target_model}, 
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Model switch response: {json.dumps(result, indent=2)}")
            
            # Verify the model change
            verify_response = requests.get(f"{base_url}/model")
            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                if verify_data.get('current_model') == target_model:
                    print(f"✓ Successfully switched to model: {target_model}")
                else:
                    print(f"✗ Model didn't switch as expected. Current model: {verify_data.get('current_model')}")
        else:
            print(f"✗ Error: Model switch returned status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Error during model switching: {str(e)}")

    print("\nTest completed.")


def test_transcription(base_url, audio_file_path):
    """Test transcription of an audio file"""
    if not os.path.exists(audio_file_path):
        print(f"✗ Error: Test audio file not found at {audio_file_path}")
        return
    
    print(f"  Sending file: {os.path.basename(audio_file_path)}")
    
    # Prepare the file for upload
    files = {
        'file': (os.path.basename(audio_file_path), open(audio_file_path, 'rb'), 'audio/wav')
    }
    
    try:
        # Set a longer timeout (90 seconds)
        start_time = time.time()
        print("  Sending request to transcription endpoint...")
        response = requests.post(f"{base_url}/whisper", files=files, timeout=90)
        elapsed_time = time.time() - start_time
        
        print(f"  Request completed in {elapsed_time:.2f} seconds")
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            print("  ✓ Transcription Result:")
            print(f"    • Filename: {result.get('filename', 'unknown')}")
            print(f"    • Model: {result.get('model', 'unknown')}")
            print(f"    • Text: {result.get('text', 'No transcription available')}")
        else:
            print(f"  ✗ Error: Received status code {response.status_code}")
            print(response.text)
    except requests.exceptions.Timeout:
        print("  ✗ Error: Request timed out after 90 seconds")
    except Exception as e:
        print(f"  ✗ Error occurred while testing the service: {str(e)}")
    finally:
        # Make sure the file is closed
        files['file'][1].close()


if __name__ == "__main__":
    # Check if a custom URL was provided
    if len(sys.argv) > 1:
        test_whisper_api(sys.argv[1])
    else:
        test_whisper_api()
