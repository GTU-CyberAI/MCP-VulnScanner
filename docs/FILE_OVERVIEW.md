# File Overview - MCP-Based Vulnerability Scanner

This document provides comprehensive technical documentation of the MCP-Based Vulnerability Scanner project, detailing each file's purpose, functionality, and interactions within the system architecture.

## 📂 Project Structure

```
mcp-vulnerability-scanner/
├── src/                                    # Source code
│   ├── mcp-security/                      # Network scanning MCP server
│   │   ├── mcp-security.py               # Main vulnerability scanner
│   │   ├── pyproject.toml                # Python dependencies
│   │   ├── uv.lock                       # UV lock file
│   │   ├── README.md                     # MCP security documentation
│   │   └── Dockerfile                    # Docker configuration
│   ├── gemini-mcp-server/                # Gemini AI integration
│   │   ├── src/                          # TypeScript source code
│   │   │   ├── gemini_mcp_server.ts      # Main Gemini server
│   │   │   ├── gemini_mcp_agent.ts       # Gemini agent wrapper
│   │   │   └── mcp_client.ts             # MCP client utilities
│   │   ├── dist/                         # Compiled JavaScript
│   │   ├── package.json                  # Node.js dependencies
│   │   ├── package-lock.json             # Dependency lock file
│   │   ├── tsconfig.json                 # TypeScript configuration
│   │   ├── smithery.yaml                 # Tool metadata
│   │   ├── LICENSE.txt                   # License file
│   │   ├── README.md                     # Gemini server documentation
│   │   └── Dockerfile                    # Docker configuration
│   ├── filesystem/                       # File system access
│   │   ├── index.ts                      # Filesystem server
│   │   ├── package.json                  # Node.js dependencies
│   │   ├── tsconfig.json                 # TypeScript configuration
│   │   ├── README.md                     # Filesystem documentation
│   │   └── Dockerfile                    # Docker configuration
│   └── sqlite/                          # Database operations
│       ├── src/mcp_server_sqlite/        # SQLite server implementation
│       │   ├── __init__.py               # Python package init
│       │   └── server.py                 # SQLite server
│       ├── test.db                       # SQLite database file
│       ├── pyproject.toml                # Python dependencies
│       ├── uv.lock                       # UV lock file
│       ├── README.md                     # SQLite documentation
│       └── Dockerfile                    # Docker configuration
├── config/                              # Configuration files
│   ├── claude_desktop_config.json        # MCP server configuration template
│   └── SETUP_INSTRUCTIONS.md            # Security setup guide
├── docs/                                # Documentation
│   └── FILE_OVERVIEW.md                 # Technical documentation (this file)
├── tests/                               # Test cases
│   └── test_mcp_security.py             # Working test suite
├── README.md                            # Main project documentation
├── setup.py                             # Automated setup script
├── .gitignore                           # Git ignore patterns
└── CHANGELOG.md                         # Project changes log
```

## 🔧 Core Components Analysis

### 🛡️ MCP Security Server (`/src/mcp-security/`)

**Primary File**: `mcp-security.py`
- **Architecture**: FastMCP-based server implementing network scanning capabilities
- **Core Functions**:
  - `run_nmap_command(command: str, timeout: int = 300)`: Safe command execution with timeout protection
  - `simple_scan(target: str)`: Host discovery using ping sweeps (-sn flag)
  - `full_scan(target: str)`: Comprehensive TCP port scanning with service detection
  - `port_scan(target: str, ports: str)`: Targeted port scanning with custom port ranges
  - `vulscan_basic(target: str)`: NSE vulnerability scanning using Vulscan database
  - `aggressive_scan(target: str)`: OS detection, service enumeration, and traceroute
- **Security Features**:
  - Command injection prevention through input validation
  - Subprocess timeout protection (5-minute default)
  - Safe shell command construction
- **Input Validation**: Sanitizes target addresses and port specifications
- **Output Format**: Structured text results compatible with AI analysis
- **Dependencies**: Requires Nmap installation and Vulscan NSE script
- **Error Handling**: Comprehensive exception catching with informative error messages

**Configuration**: `pyproject.toml`
- **Package Manager**: UV (modern Python dependency management)
- **MCP Framework**: FastMCP for efficient server implementation
- **Build System**: setuptools with modern Python packaging standards

### 🤖 Gemini AI Integration (`/src/gemini-mcp-server/`)

**Main Server**: `src/gemini_mcp_server.ts`
- **AI Model**: Google Gemini 2.5 Pro with large context window
- **Key Classes**:
  - `GeminiMCPServer`: Primary server implementation
  - Tool registration and prompt processing
- **Core Capabilities**:
  - `generateText()`: Processes vulnerability scan results through AI analysis
  - Context-aware security recommendations
  - Multi-turn conversation support
- **API Integration**: Google Generative AI SDK with proper error handling
- **Input Processing**: Handles complex vulnerability data and user queries
- **Output Generation**: Structured security analysis and recommendations

**Agent Wrapper**: `src/gemini_mcp_agent.ts`
- **Purpose**: Abstraction layer for Gemini model interactions
- **Features**: Configuration management and response optimization
- **Error Handling**: Graceful degradation on API failures

**Client Utilities**: `src/mcp_client.ts`
- **Communication**: MCP protocol client implementation
- **Connection Management**: Server discovery and tool invocation

**Build Configuration**: 
- **TypeScript**: Modern ES modules with strict type checking
- **Dependencies**: @google/generative-ai, @modelcontextprotocol/sdk
- **Compilation**: Automated build process with source maps

### 📁 Filesystem Security Scanner (`/src/filesystem/`)

**Core Server**: `index.ts`
- **Security Scope**: Static code analysis and file vulnerability detection
- **Access Control**: Configurable directory restrictions
- **Scanning Capabilities**:
  - Pattern-based vulnerability detection
  - Code quality analysis
  - Dependency security assessment
- **File Operations**: 
  - Secure file reading with path validation
  - Directory traversal protection
  - Content analysis and reporting
- **Integration**: Works with Gemini AI for intelligent code review

### 💾 Database Management (`/src/sqlite/`)

**Server Implementation**: `src/mcp_server_sqlite/server.py`
- **Database Engine**: SQLite with MCP protocol integration
- **Schema Management**: 
  - Scan results storage with timestamps
  - Vulnerability tracking and history
  - Report metadata and export logs
- **Key Operations**:
  - `INSERT` operations for scan data persistence
  - `SELECT` queries for historical analysis
  - `UPDATE` operations for scan status tracking
- **Data Integrity**: Transaction support and constraint enforcement
- **Performance**: Indexed queries for efficient data retrieval

**Database File**: `test.db`
- **Location**: Local SQLite database in project structure
- **Size Management**: Automatic cleanup and archival capabilities
- **Backup**: Manual backup procedures documented

## ⚙️ Configuration and Setup

### 🔧 MCP Configuration (`/config/claude_desktop_config.json`)

**Template Structure**:
```json
{
  "mcpServers": {
    "mcp-security": {
      "command": "uv",
      "args": ["--directory", "<YOUR_PROJECT_PATH>/src/mcp-security", "run", "mcp-security"],
      "env": {}
    },
    "gemini-mcp-server": {
      "command": "node",
      "args": ["<YOUR_PROJECT_PATH>/src/gemini-mcp-server/dist/gemini_mcp_server.js"],
      "env": {
        "GEMINI_API_KEY": "<YOUR_GEMINI_API_KEY>"
      }
    }
  }
}
```

**Critical Placeholders**:
- `<YOUR_PROJECT_PATH>`: Absolute path to project root
- `<YOUR_GEMINI_API_KEY>`: Google AI Studio API key
- `<PATH_TO_ANALYZE>`: Target directories for filesystem scanning

**Security Setup**: `config/SETUP_INSTRUCTIONS.md`
- **Cross-platform installation guides**
- **API key management best practices**
- **Troubleshooting common configuration issues**
- **Security hardening recommendations**

## 🧪 Testing Infrastructure (`/tests/`)

**Test Suite**: `test_mcp_security.py`
- **Framework**: Python unittest with advanced mocking
- **Coverage**: 8 comprehensive test cases
- **Test Categories**:
  - **Functional Tests**: `test_simple_scan_function`, `test_port_scan_function`
  - **Error Handling**: `test_run_nmap_command_exception`
  - **Security Tests**: `test_security_input_validation`, `test_subprocess_call_safety`
  - **Integration Tests**: `test_mcp_server_initialization`
- **Mocking Strategy**: `patch.object()` for subprocess isolation
- **Security Validation**: Command injection prevention testing
- **Performance**: Timeout and resource usage validation

## 🔄 System Architecture and Data Flow

### Primary Workflow:
1. **User Interaction**: Natural language input via Claude Desktop
2. **Intent Recognition**: Claude determines appropriate MCP tool chain
3. **Network Scanning**: 
   - mcp-security executes Nmap commands
   - Results captured and sanitized
4. **AI Analysis**: 
   - Gemini processes scan outputs
   - Generates security insights and recommendations
5. **Data Persistence**: 
   - SQLite stores scan results and metadata
   - Historical data available for trend analysis
6. **Report Generation**: 
   - Multi-format output (.csv, .pdf, .txt)
   - Customizable report templates

### Inter-Component Communication:
- **Claude ↔ MCP Servers**: JSON-RPC protocol over stdio
- **Security Scanner ↔ System**: Controlled subprocess execution
- **Gemini Server ↔ Google AI**: HTTPS API calls with authentication
- **Database Server ↔ SQLite**: Local file-based operations
- **Filesystem Server ↔ OS**: Restricted file system access

## 🔒 Security Architecture

### Input Validation:
- **Command Injection Prevention**: Parameterized command construction
- **Path Traversal Protection**: Filesystem access restrictions
- **API Rate Limiting**: Gemini API usage controls
- **Resource Limits**: Memory and execution time constraints

### Data Protection:
- **Configuration Security**: Template-based sensitive data handling
- **API Key Management**: Environment variable isolation
- **Database Security**: Local storage with access controls
- **Network Security**: Controlled scanning targets and timeouts

### Operational Security:
- **Error Handling**: Information disclosure prevention
- **Logging**: Security event tracking without sensitive data exposure
- **Access Control**: Principle of least privilege implementation
- **Audit Trail**: Scan history and user activity logging

## 🛠️ Development and Deployment

### Build Requirements:
- **Python**: 3.8+ with UV package manager
- **Node.js**: 16+ with npm/yarn support
- **TypeScript**: 4.5+ for modern language features
- **External Tools**: Nmap, Vulscan NSE script installation

### Development Workflow:
1. **Environment Setup**: Use `setup.py` for automated configuration
2. **Dependency Management**: UV for Python, npm for Node.js
3. **Testing**: Run test suite before deployment
4. **Build Process**: TypeScript compilation for Gemini server
5. **Configuration**: Secure template customization

### Performance Considerations:
- **Concurrent Scanning**: Parallel execution capabilities
- **Memory Management**: Efficient result processing
- **Network Optimization**: Intelligent scan scheduling
- **Caching**: Repeated scan result optimization

### Monitoring and Maintenance:
- **Health Checks**: MCP server status monitoring
- **Performance Metrics**: Scan execution time tracking
- **Error Monitoring**: Exception logging and alerting
- **Update Management**: Dependency security updates

## 📊 File Dependencies and Relationships

### Critical Dependencies:
- **mcp-security.py** → Nmap binary installation
- **gemini_mcp_server.ts** → Google AI API credentials
- **claude_desktop_config.json** → All MCP server executables
- **test.db** → SQLite server read/write permissions

### Optional Components:
- **Dockerfile files** → Container deployment scenarios
- **README.md files** → Component-specific documentation
- **smithery.yaml** → Tool metadata and discovery

This comprehensive file overview provides the technical foundation for understanding, maintaining, and extending the MCP-Based Vulnerability Scanner system.