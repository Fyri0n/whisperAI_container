from flask import Flask, request, jsonify, abort
from tempfile import NamedTemporaryFile
import whisper, torch
import os

class WhisperAPI:
    # List of valid models that can be used
    VALID_MODELS = ["tiny", "base", "small", "medium", "large"]
    
    def __init__(self, initial_model="base"):
        # Print CUDA availability info for debugging
        print(f"CUDA is available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"Number of CUDA devices: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"Device {i}: {torch.cuda.get_device_name(i)}")
        else:
            print("No CUDA devices available.")
            print("PyTorch built with CUDA: ", torch.backends.cudnn.is_available())
            
        # Set device (GPU or CPU) - force CUDA if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Track current model name
        self.current_model_name = initial_model if initial_model in self.VALID_MODELS else "base"
        
        # Load the initial model
        self.model = self.load_model(self.current_model_name)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.setup_routes()
    
    def load_model(self, model_name):
        """Load a Whisper model by name with error handling"""
        try:
            return whisper.load_model(model_name, device=self.device)
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            # If loading fails and it's not already base, try loading base as fallback
            if model_name != "base":
                print("Falling back to base model")
                return whisper.load_model("base", device=self.device)
            return None
    
    def setup_routes(self):
        """Set up Flask routes"""
        self.app.route("/")(self.health)
        self.app.route("/whisper", methods=["POST"])(self.transcribe)
        self.app.route("/model", methods=["GET", "POST"])(self.manage_model)
    
    def health(self):
        """Health check endpoint that also returns model info"""
        return jsonify({
            "status": "ok",
            "device": self.device,
            "current_model": self.current_model_name
        }), 200
    
    def transcribe(self):
        """Endpoint to transcribe audio files"""
        if "file" not in request.files:
            abort(400, description="Missing 'file' form field.")

        f = request.files["file"]
        with NamedTemporaryFile(suffix=os.path.splitext(f.filename)[1], delete=False) as tmp:
            f.save(tmp.name)
        try:
            res = self.model.transcribe(tmp.name)
            return jsonify({
                "filename": f.filename, 
                "text": res["text"],
                "model": self.current_model_name
            })
        finally:
            os.remove(tmp.name)
    
    def manage_model(self):
        """Endpoint to get or change the current model"""
        # GET request returns current model info
        if request.method == "GET":
            return jsonify({
                "current_model": self.current_model_name,
                "available_models": self.VALID_MODELS,
                "device": self.device
            })
        
        # POST request changes the model
        data = request.get_json()
        if not data or "model" not in data:
            abort(400, description="Missing 'model' field in JSON body")
        
        requested_model = data["model"]
        if requested_model not in self.VALID_MODELS:
            return jsonify({
                "error": f"Invalid model name. Choose from: {', '.join(self.VALID_MODELS)}",
                "current_model": self.current_model_name
            }), 400
        
        # Don't reload if it's the same model
        if requested_model == self.current_model_name:
            return jsonify({
                "message": f"Model already set to {requested_model}",
                "current_model": self.current_model_name
            })
        
        # Try to load the new model
        new_model = self.load_model(requested_model)
        if new_model is None:
            return jsonify({
                "error": f"Failed to load model: {requested_model}",
                "current_model": self.current_model_name
            }), 500
        
        # Update model and model name
        self.model = new_model
        self.current_model_name = requested_model
        
        return jsonify({
            "message": f"Model changed to {self.current_model_name}",
            "current_model": self.current_model_name
        })
    
    def run(self, host="0.0.0.0", port=5000):
        """Run the Flask application"""
        self.app.run(host=host, port=port)


# Create and run the application when this file is executed directly
if __name__ == "__main__":
    whisper_api = WhisperAPI()
    whisper_api.run()

