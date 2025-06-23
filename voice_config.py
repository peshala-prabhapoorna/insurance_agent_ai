from typing import List
import numpy as np
from numpy.typing import NDArray
import sounddevice as sd

from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    VoicePipeline,
    VoicePipelineConfig,
    TTSModelSettings
)


AudioBuffer = List[NDArray[np.int16]]

AUDIO_CONFIG = {
    "samplerate": 24000,
    "channels": 1,
    "dtype": "int16",
    "blocksize": 2400,
    "silence_threshold": 500,
    "silence_duration": 1.5,
    "min_speech_duration": 0.5,
}

insurance_tts_settings = TTSModelSettings(
    instructions=(
        "Personality: Professional, knowledgeable, and helpful insurance advisor"
        "Tone: Friendly, clear, and reassuring, making customers feel confident about their insurance choices"
        "Pronunciation: Clear and articulate, ensuring insurance terms are easily understood"
        "Tempo: Moderate pace with natural pauses, especially when explaining complex insurance concepts"
        "Emotion: Warm and supportive, conveying trust and expertise in insurance matters"
    )
)

class AudioStreamManager:
    """Context manager for handling audio streams"""
    def __init__(self, input_stream: sd.InputStream, output_stream: sd.OutputStream):
        self.input_stream = input_stream
        self.output_stream = output_stream


    async def __aenter__(self):
        try:
            self.input_stream.start()
            self.output_stream.start()
            return self
        except sd.PortAudioError as e:
            raise RuntimeError(f"Failed to start audio streams: {e}")


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.input_stream:
                self.input_stream.stop()
                self.input_stream.close()
            if self.output_stream:
                self.output_stream.stop()
                self.output_stream.close()
        except Exception as e:
            print(f"Warning: Error during audio stream cleanup: {e}")
