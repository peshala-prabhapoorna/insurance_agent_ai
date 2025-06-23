import shutil
import subprocess
from typing import Optional
import nest_asyncio

from setup import wait_for_server_ready


class ServerProcess:
    """Context manager for handling SSE server process"""
    def __init__(self, server_file: str):
        self.server_file = server_file
        self.process: Optional[subprocess.Popen] = None


    async def __aenter__(self):
        if not shutil.which("uv"):
            raise RuntimeError(
                "uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/"
            )

        print("Starting SSE server at http://localhost:8000/sse ...")
        self.process = subprocess.Popen(["uv", "run", self.server_file])
        try:
            await wait_for_server_ready()
            nest_asyncio.apply()
            print("SSE server started. Starting voice assistant...\n")
            return self
        except Exception as e:
            if self.process:
                self.process.terminate()
            raise RuntimeError(f"Failed to start SSE server: {e}")


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                if self.process.poll() is None:
                    self.process.kill()
            except Exception as e:
                print(f"Warning: Error during server shutdown: {e}")
