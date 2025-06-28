# MCP-Based Vulnerability Scanner

## 📌 Project Title
**MCP-Based Vulnerability Scanner**: An AI-driven network vulnerability scanning tool that combines Nmap's scanning capabilities with Large Language Model analysis through the Model Context Protocol (MCP).

## 📖 Project Description

The MCP-Based Vulnerability Scanner addresses critical cybersecurity challenges by integrating traditional network scanning tools with advanced AI capabilities. This system combines:

- **Nmap's powerful network scanning** for comprehensive port scanning and service detection
- **Vulscan integration** for CVE-based vulnerability identification  
- **Large Language Model analysis** via Claude AI for intelligent result interpretation
- **Model Context Protocol (MCP)** for seamless tool integration
- **Multi-format reporting** (.csv, .pdf, .txt) with actionable remediation suggestions

### Key Features

- **Natural Language Interface**: Interact with the scanner using simple prompts
- **Comprehensive Scanning**: Network mapping, port scanning, service detection, and vulnerability assessment
- **AI-Powered Analysis**: LLM interprets raw scan data and provides contextual insights
- **Static Code Analysis**: Analyze local code repositories for security vulnerabilities
- **Automated Reporting**: Generate structured reports with severity assessments and remediation steps
- **Real-time Web Integration**: Access up-to-date vulnerability information through web browsing
- **Flexible Storage**: Support for various output formats and temporary result storage

## 🛠️ Installation Instructions

### Prerequisites

1. **Python 3.8+** with UV package manager
2. **Node.js 16+** with npm
3. **Nmap** installed and accessible from command line
4. **Vulscan NSE script** for Nmap vulnerability scanning
5. **Claude Desktop** application
6. **Gemini API Key** from Google AI Studio

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd mcp-vulnerability-scanner
```

### Step 2: Install MCP Security Server

```bash
cd src/mcp-security
uv sync
```

### Step 3: Install Gemini MCP Server

```bash
cd src/gemini-mcp-server
npm install
npm run build
```

### Step 4: Install Filesystem MCP Server

```bash
cd src/filesystem
npm install
```

### Step 5: Install SQLite MCP Server

```bash
cd src/sqlite
uv sync
```

### Step 6: Configure Claude Desktop

🔒 **SECURITY NOTICE**: The configuration file in this repository contains placeholder values only. **DO NOT** use it directly!

📖 **For detailed, secure setup instructions, see**: [`config/SETUP_INSTRUCTIONS.md`](config/SETUP_INSTRUCTIONS.md)

**Quick Summary:**
1. The `config/claude_desktop_config.json` file is a **template only**
2. Copy it to your Claude Desktop configuration directory
3. Replace ALL placeholder values with your actual paths and API keys
4. Never commit files containing real credentials to version control

**Configuration locations:**
- **Windows**: `C:\Users\<UserName>\AppData\Roaming\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/claude-desktop/claude_desktop_config.json`

### Step 7: Set Environment Variables

Create a `.env` file in the `src/gemini-mcp-server` directory:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 8: Install Vulscan

Download and install the Vulscan NSE script for Nmap:

```bash
# Download Vulscan
git clone https://github.com/scipag/vulscan.git
# Copy to Nmap scripts directory (path varies by OS)
```

## ▶️ Usage Examples

### Basic Network Scan

```
Scan 192.168.1.1 for open ports and services
```

### Vulnerability Assessment

```
Perform a comprehensive vulnerability scan on scanme.nmap.org and generate a PDF report
```

### Code Analysis

```
Analyze the files in /src directory for security vulnerabilities and suggest patches
```

### Custom Scanning

```
Run an aggressive Nmap scan with OS detection on 10.0.0.0/24 network
```

## 🧩 Troubleshooting

### Common Issues

1. **"Nmap not found" error**
   - Ensure Nmap is installed and added to system PATH
   - Verify installation: `nmap --version`

2. **Claude Desktop connection failed**
   - Check that paths in claude_desktop_config.json are correct
   - Restart Claude Desktop after configuration changes
   - Verify all MCP servers are built and dependencies installed
   - See [`config/SETUP_INSTRUCTIONS.md`](config/SETUP_INSTRUCTIONS.md) for detailed troubleshooting

3. **Gemini API errors**
   - Verify GEMINI_API_KEY is correctly set
   - Check API key permissions and quota limits

4. **Permission errors**
   - Run with appropriate privileges for network scanning
   - Ensure write permissions for report generation directories

5. **UV/Node.js issues**
   - Update UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Update Node.js to latest LTS version

## 🤝 Acknowledgments

- **Course**: Network and Information Security (CSE473)
- **Instructor**: Assistant Prof. Salih SARP
- **Institution**: Gebze Technical University
- **Collaborators**: 
  - Çağla Nur Yuva (c.yuva2020@gtu.edu.tr - caglanur__2001@hotmail.com (github))
  - Murat Erbilici (m.erbilici2020@gtu.edu.tr - muraterbiliciofficial@gmail.com (github))

## 📄 License

This project is developed for academic purposes as part of the Network and Information Security (CSE473) course at Gebze Technical University.

## 🔗 References

- Model Context Protocol: https://modelcontextprotocol.io/
- Nmap Network Mapper: https://nmap.org/
- Vulscan NSE Script: https://github.com/scipag/vulscan
- Claude AI: https://www.anthropic.com/
- Google Gemini API: https://ai.google.dev/
- Filesystem MCP: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- Sqlite Local Database MCP: https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sqlite
- Web browsing MCP: https://github.com/nickclyde/duckduckgo-mcp-server
- Gemini MCP: https://github.com/georgejeffers/gemini-mcp-server/tree/main
- A Similar Project: https://github.com/davidfortytwo/AI-Vuln-Scanner
