import os
import json
import shutil
from pathlib import Path

def setup_mcp():
    """
    Automatically configures the MCP settings for Roo Code/Cline.
    It injects:
    1. The absolute path of the current project (cwd).
    2. The absolute path of the 'uv' executable (to avoid PATH issues in VS Code).
    """
    
    # 1. Get the current absolute project path
    current_dir = os.getcwd()
    print(f"📍 Detected project directory: {current_dir}")

    # 2. Detect the absolute path of 'uv'
    # VS Code extensions often don't inherit the shell PATH, so "uv" alone might fail.
    # shutil.which finds the full path (e.g., /Users/user/.cargo/bin/uv).
    uv_executable = shutil.which("uv")
    
    if uv_executable:
        print(f"🔧 Detected 'uv' executable at: {uv_executable}")
    else:
        # Fallback if not found (unlikely if you are running this with uv run)
        uv_executable = "uv"
        print("⚠️ Warning: Could not find absolute path for 'uv'. Using 'uv' as command.")

    # 3. Define Roo Code config path (hidden folder)
    roo_config_path = Path(".roo/mcp.json")
    
    # Ensure the directory exists
    roo_config_path.parent.mkdir(exist_ok=True)

    # 4. Create JSON content with dynamic paths
    config_data = {
        "mcpServers": {
            "clone-brain": {
                "command": uv_executable,  # Dynamic absolute path to uv
                "args": ["run", "server.py"],
                "cwd": current_dir,        # Dynamic absolute path to project
                "env": {}
            }
        }
    }

    # 5. Write the file
    try:
        with open(roo_config_path, "w") as f:
            json.dump(config_data, f, indent=2)
        print(f"✅ Success! Configuration written to: {roo_config_path}")
        print("👉 Now go to Roo Code and click the 'Refresh' icon in the MCP panel.")
    except Exception as e:
        print(f"❌ Error writing configuration: {e}")

if __name__ == "__main__":
    setup_mcp()