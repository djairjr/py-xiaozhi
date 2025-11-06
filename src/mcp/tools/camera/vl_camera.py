"""
VL camera implementation using Zhipu AI.
"""

import base64

import cv2
from openai import OpenAI

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger

from .base_camera import BaseCamera

logger = get_logger(__name__)


class VLCamera(BaseCamera):
    """Zhipu AI camera implementation."""

    _instance = None

    def __init__(self):
        """Initialize the Zhipu AI camera."""
        super().__init__()
        config = ConfigManager.get_instance()

        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=config.get_config("CAMERA.VLapi_key"),
            base_url=config.get_config(
                "CAMERA.Local_VL_url",
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            ),
        )
        self.model = config.get_config("CAMERA.models", "glm-4v-plus")
        logger.info(f"VL Camera initialized with model: {self.model}")

    @classmethod
    def get_instance(cls):
        """Get a singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def capture(self) -> bool:
        """Capture image."""
        try:
            logger.info("Accessing camera...")

            # Try turning on the camera
            cap = cv2.VideoCapture(self.camera_index)
            if not cap.isOpened():
                logger.error(f"Cannot open camera at index {self.camera_index}")
                return False

            # Set camera parameters
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)

            # read image
            ret, frame = cap.read()
            cap.release()

            if not ret:
                logger.error("Failed to capture image")
                return False

            # Get original image size
            height, width = frame.shape[:2]

            # Calculate the scaling so that the longest side is 320
            max_dim = max(height, width)
            scale = 320 / max_dim if max_dim > 320 else 1.0

            # Scale image proportionally
            if scale < 1.0:
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame = cv2.resize(
                    frame, (new_width, new_height), interpolation=cv2.INTER_AREA
                )

            # Directly encode images to JPEG byte streams
            success, jpeg_data = cv2.imencode(".jpg", frame)

            if not success:
                logger.error("Failed to encode image to JPEG")
                return False

            # Save byte data
            self.set_jpeg_data(jpeg_data.tobytes())
            logger.info(
                f"Image captured successfully (size: {self.jpeg_data['len']} bytes)"
            )
            return True

        except Exception as e:
            logger.error(f"Exception during capture: {e}")
            return False

    def analyze(self, question: str) -> str:
        """Use Chipu AI to analyze images."""
        try:
            if not self.jpeg_data["buf"]:
                return '{"success": false, "message": "Camera buffer is empty"}'

            # Convert image to Base64
            image_base64 = base64.b64encode(self.jpeg_data["buf"]).decode("utf-8")

            # Prepare message
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                question
                                if question
                                else "What scene is depicted in the picture? Please describe in detail."
                            ),
                        },
                    ],
                },
            ]

            # Send request
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                modalities=["text"],
                stream=True,
                stream_options={"include_usage": True},
            )

            # Collect responses
            result = ""
            for chunk in completion:
                if chunk.choices:
                    result += chunk.choices[0].delta.content or ""

            # Log response
            logger.info(f"VL analysis completed, question={question}")
            return f'{{"success": true, "text": "{result}"}}'

        except Exception as e:
            error_msg = f"Failed to analyze image with VL: {str(e)}"
            logger.error(error_msg)
            return f'{{"success": false, "message": "{error_msg}"}}'
