import socket
import time
import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning)

async def wait_for_server_ready(port: int = 8000, timeout: float = 10) -> None:
    """Wait for SSE server to be ready"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                print("✅ SSE server TCP port is accepting connections")
                return
        except OSError as e:
            if time.time() - start > timeout - 1: # Only print on last attempt
                print(f"Waiting for server... ({e})")
            time.sleep(0.5)
    raise RuntimeError("❌ SSE server did not become ready in time.")
