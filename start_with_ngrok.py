"""
Helper script to start the PostgreSQL MCP server with ngrok tunnel.
This will expose your local MCP server to the internet via ngrok.
"""

import subprocess
import time
import sys
import os
import signal

# Configuration
MCP_SERVER_PORT = 8010
NGROK_REGION = "us"  # Change to your preferred region: us, eu, ap, au, sa, jp, in


def start_mcp_server():
    """Start the MCP server in a subprocess."""
    print("Starting PostgreSQL MCP Server...")
    server_process = subprocess.Popen(
        [sys.executable, "postgres_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    return server_process


def start_ngrok():
    """Start ngrok tunnel."""
    print(f"\nStarting ngrok tunnel on port {MCP_SERVER_PORT}...")
    ngrok_process = subprocess.Popen(
        ["ngrok", "http", str(MCP_SERVER_PORT), "--region", NGROK_REGION],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return ngrok_process


def get_ngrok_url():
    """Get the public ngrok URL."""
    import requests
    import json
    
    # Wait for ngrok to start
    time.sleep(2)
    
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = response.json()
        
        if tunnels.get("tunnels"):
            public_url = tunnels["tunnels"][0]["public_url"]
            return public_url
        else:
            return None
    except Exception as e:
        print(f"Could not retrieve ngrok URL: {e}")
        print("You can check the ngrok dashboard at: http://localhost:4040")
        return None


def main():
    """Main function to start both server and ngrok."""
    server_process = None
    ngrok_process = None
    
    try:
        # Start MCP server
        server_process = start_mcp_server()
        time.sleep(3)  # Give server time to start
        
        # Check if server started successfully
        if server_process.poll() is not None:
            print("Error: MCP server failed to start!")
            print("Make sure you have configured your .env file with database credentials.")
            return
        
        print("✓ MCP Server started successfully on http://localhost:8010")
        
        # Start ngrok
        ngrok_process = start_ngrok()
        time.sleep(2)
        
        # Get and display ngrok URL
        public_url = get_ngrok_url()
        
        if public_url:
            print(f"\n{'='*60}")
            print(f"✓ Ngrok tunnel established!")
            print(f"{'='*60}")
            print(f"\nPublic URL: {public_url}")
            print(f"Local URL:  http://localhost:{MCP_SERVER_PORT}")
            print(f"\nNgrok Dashboard: http://localhost:4040")
            print(f"\n{'='*60}")
            print("\nYour MCP server is now accessible from anywhere!")
            print("Press Ctrl+C to stop both server and ngrok tunnel.")
            print(f"{'='*60}\n")
        else:
            print("\n⚠ Ngrok started but could not retrieve public URL")
            print("Check the ngrok dashboard at: http://localhost:4040")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if server_process.poll() is not None:
                print("\n⚠ MCP server stopped unexpectedly!")
                break
            
            if ngrok_process.poll() is not None:
                print("\n⚠ Ngrok tunnel stopped unexpectedly!")
                break
    
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    
    except Exception as e:
        print(f"\nError: {e}")
    
    finally:
        # Clean up processes
        if server_process and server_process.poll() is None:
            print("Stopping MCP server...")
            server_process.terminate()
            server_process.wait(timeout=5)
        
        if ngrok_process and ngrok_process.poll() is None:
            print("Stopping ngrok tunnel...")
            ngrok_process.terminate()
            ngrok_process.wait(timeout=5)
        
        print("✓ Cleanup complete. Goodbye!")


if __name__ == "__main__":
    # Check if ngrok is installed
    try:
        subprocess.run(["ngrok", "version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ngrok is not installed or not in PATH!")
        print("\nTo install ngrok:")
        print("1. Download from: https://ngrok.com/download")
        print("2. Extract and add to your PATH")
        print("3. Sign up at https://ngrok.com and get your auth token")
        print("4. Run: ngrok authtoken YOUR_AUTH_TOKEN")
        sys.exit(1)
    
    main()
