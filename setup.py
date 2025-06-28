#!/usr/bin/env python3
"""
MCP-Based Vulnerability Scanner Setup Script

This script helps automate the installation and configuration process
for the MCP-Based Vulnerability Scanner project.
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path

class MCPVulnScannerSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.platform = platform.system().lower()
        
    def print_banner(self):
        """Print setup banner"""
        print("=" * 60)
        print("  MCP-Based Vulnerability Scanner Setup")
        print("  Çağla Nur Yuva & Murat Erbilici")
        print("  Gebze Technical University")
        print("=" * 60)
        print()

    def check_prerequisites(self):
        """Check if required tools are installed"""
        print("🔍 Checking prerequisites...")
        
        required_tools = {
            'python': ['python', '--version'],
            'node': ['node', '--version'],
            'npm': ['npm', '--version'],
            'nmap': ['nmap', '--version'],
            'uv': ['uv', '--version']
        }
        
        missing_tools = []
        
        for tool, command in required_tools.items():
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip().split('\n')[0]
                    print(f"  ✅ {tool}: {version}")
                else:
                    missing_tools.append(tool)
                    print(f"  ❌ {tool}: Not found")
            except FileNotFoundError:
                missing_tools.append(tool)
                print(f"  ❌ {tool}: Not found")
        
        if missing_tools:
            print(f"\n⚠️  Missing required tools: {', '.join(missing_tools)}")
            print("Please install them before continuing.")
            return False
        
        print("✅ All prerequisites satisfied!")
        return True

    def setup_python_projects(self):
        """Set up Python projects using UV"""
        print("\n🐍 Setting up Python projects...")
        
        python_projects = ['src/mcp-security', 'src/sqlite']
        
        for project in python_projects:
            project_path = self.project_root / project
            if project_path.exists():
                print(f"  📦 Installing dependencies for {project}")
                try:
                    subprocess.run(['uv', 'sync'], cwd=project_path, check=True)
                    print(f"  ✅ {project} setup complete")
                except subprocess.CalledProcessError:
                    print(f"  ❌ Failed to setup {project}")
                    return False
        
        return True

    def setup_node_projects(self):
        """Set up Node.js projects"""
        print("\n📦 Setting up Node.js projects...")
        
        node_projects = ['src/gemini-mcp-server', 'src/filesystem']
        
        for project in node_projects:
            project_path = self.project_root / project
            if project_path.exists():
                print(f"  📦 Installing dependencies for {project}")
                try:
                    subprocess.run(['npm', 'install'], cwd=project_path, check=True)
                    print(f"  ✅ {project} dependencies installed")
                    
                    # Build TypeScript projects
                    if 'gemini' in project:
                        subprocess.run(['npm', 'run', 'build'], cwd=project_path, check=True)
                        print(f"  🔨 {project} built successfully")
                        
                except subprocess.CalledProcessError:
                    print(f"  ❌ Failed to setup {project}")
                    return False
        
        return True

    def create_config_template(self):
        """Create Claude Desktop configuration template"""
        print("\n⚙️  Creating configuration template...")
        
        config_template = {
            "mcpServers": {
                "mcp-security": {
                    "command": "uv",
                    "args": [
                        "--directory",
                        str(self.project_root / "src/mcp-security"),
                        "run",
                        "mcp-security.py"
                    ]
                },
                "gemini": {
                    "command": "node",
                    "args": [
                        str(self.project_root / "src/gemini-mcp-server/dist/gemini_mcp_server.js")
                    ],
                    "env": {
                        "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY_HERE"
                    }
                },
                "filesystem": {
                    "command": "npx",
                    "args": [
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        str(self.project_root)
                    ]
                },
                "sqlite": {
                    "command": "uv",
                    "args": [
                        "--directory",
                        str(self.project_root / "src/sqlite"),
                        "run",
                        "mcp-server-sqlite",
                                                 "--db-path",
                         str(self.project_root / "src/sqlite/test.db")
                    ]
                },
                "ddg-search": {
                    "command": "uvx",
                    "args": ["duckduckgo-mcp-server"]
                }
            }
        }
        
        config_file = self.project_root / "config/claude_desktop_config_template.json"
        with open(config_file, 'w') as f:
            json.dump(config_template, f, indent=2)
        
        print(f"  ✅ Configuration template created: {config_file}")
        print("  📝 Please copy this to your Claude Desktop config directory:")
        
        if self.platform == 'windows':
            claude_config_path = os.path.expanduser("~/AppData/Roaming/Claude/claude_desktop_config.json")
        else:
            claude_config_path = os.path.expanduser("~/.config/claude-desktop/claude_desktop_config.json")
        
        print(f"     {claude_config_path}")
        print("  🔑 Don't forget to set your GEMINI_API_KEY!")

    def create_directories(self):
        """Create necessary directories"""
        print("\n📁 Creating project directories...")
        
        directories = [
            'logs'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {directory}")

    def run_setup(self):
        """Run the complete setup process"""
        self.print_banner()
        
        if not self.check_prerequisites():
            sys.exit(1)
        
        if not self.setup_python_projects():
            print("❌ Python setup failed")
            sys.exit(1)
        
        if not self.setup_node_projects():
            print("❌ Node.js setup failed")
            sys.exit(1)
        
        self.create_config_template()
        self.create_directories()
        
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Get a Gemini API key from https://ai.google.dev/")
        print("2. Copy the configuration template to your Claude Desktop config")
        print("3. Update the GEMINI_API_KEY in the configuration")
        print("4. Install Vulscan NSE script for Nmap")
        print("5. Restart Claude Desktop")
        print("\n🚀 You're ready to start vulnerability scanning!")

if __name__ == '__main__':
    setup = MCPVulnScannerSetup()
    setup.run_setup() 