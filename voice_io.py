import asyncio

import numpy as np
from numpy.typing import NDArray
import sounddevice as sd
from agents import Agent, trace
from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline, VoicePipelineConfig

from voice_config import AudioBuffer, insurance_tts_settings, AUDIO_CONFIG, AudioStreamManager

async def continuous_voice_conversation(agent: Agent):
    """Run a continuous voice conversation with automatic voice detection"""

    voice_config = VoicePipelineConfig(
        tts_settings=insurance_tts_settings,
    )

    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(agent),
        config=voice_config
    )

    audio_queue: asyncio.Queue[NDArray[np.int16]] = asyncio.Queue()
    is_agent_speaking = False


    def audio_callback(indata: NDArray[np.int16], frames: int, time_info: dict, status: sd.CallbackFlags) -> None:
        """Callback for continuous audio input"""
        if status:
            print(f"Audio input status: {status}")
        if not is_agent_speaking: # Only record when agent isn't speaking
            audio_queue.put_nowait(indata.copy())


    input_stream = sd.InputStream(
        samplerate=AUDIO_CONFIG["samplerate"],
        channels=AUDIO_CONFIG["channels"],
        dtype=AUDIO_CONFIG["dtype"],
        callback=audio_callback,
        blocksize=AUDIO_CONFIG["blocksize"]
    )

    output_stream = sd.OutputStream(
        samplerate=AUDIO_CONFIG["samplerate"],
        channels=AUDIO_CONFIG["channels"],
        dtype=AUDIO_CONFIG["dtype"]
    )

    print("🎙️ Insurance Voice Assistant Ready!")
    print("Start speaking at any time. Say 'goodbye' to exit.")
    print("-" * 50)


    async with AudioStreamManager(input_stream, output_stream):
        silence_threshold = AUDIO_CONFIG["silence_threshold"]
        silence_duration = 0
        max_silence = AUDIO_CONFIG["silence_duration"]
        audio_buffer: AudioBuffer = []

        while True:
            try:
                chunk = await asyncio.wait_for(audio_queue.get(), timeout=0.1)
                
                if np.abs(chunk).mean() > silence_threshold:
                    audio_buffer.append(chunk)
                    silence_duration = 0
                elif audio_buffer:
                    silence_duration += 0.1
                    audio_buffer.append(chunk)
                    
                    if silence_duration >= max_silence:
                        try:
                            full_audio = np.concatenate(audio_buffer, axis=0)
                            
                            if len(full_audio) > AUDIO_CONFIG["samplerate"] * AUDIO_CONFIG["min_speech_duration"]:
                                print("\n🤔 Processing speech...")
                                
                                is_agent_speaking = True
                                
                                audio_input = AudioInput(buffer=full_audio)
                                
                                with trace("Insurance Voice Query"):
                                    result = await pipeline.run(audio_input)
                                    
                                    print("💬 Assistant responding...")
                                    async for event in result.stream():
                                        if event.type == "voice_stream_event_audio":
                                            output_stream.write(event.data)
                                        elif event.type == "voice_stream_event_transcript":
                                            print(f"   > {event.text}", end="", flush=True)
                                    
                                    print("\n")
                                
                        except Exception as e:
                            print(f"\n❌ Error processing speech: {e}")
                        finally:
                            is_agent_speaking = False
                            audio_buffer = []
                            silence_duration = 0
                            
            except asyncio.TimeoutError:
                continue
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                if isinstance(e, (sd.PortAudioError, RuntimeError)):
                    raise
