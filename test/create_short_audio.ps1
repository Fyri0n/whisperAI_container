# Generate a very short audio file for testing
# This script creates a simple audio file with a short message

Add-Type -AssemblyName System.Speech
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synthesizer.Rate = 0  # Normal speaking rate
$synthesizer.Volume = 100  # Maximum volume

# Create a temporary path for the audio file
$audioFilePath = Join-Path $PWD "short_test.wav"

# Text to synthesize - much shorter than before
$textToSpeak = "Hello, world. Testing WhisperAI."

# Generate the audio file
$synthesizer.SetOutputToWaveFile($audioFilePath)
$synthesizer.Speak($textToSpeak)
$synthesizer.SetOutputToNull()
$synthesizer.Dispose()

Write-Host "Created short test audio file at: $audioFilePath"
