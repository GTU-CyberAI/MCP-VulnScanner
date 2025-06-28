# Claude Desktop Configuration Setup Instructions

## 🔒 Security Notice

The `claude_desktop_config.json` file in this directory is a **template** with placeholder values. **DO NOT** use it directly as it contains placeholder values that need to be customized for your system.

## 📍 Configuration File Location

The actual Claude Desktop configuration file should be placed at:

### Windows:
```
C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json
```

### macOS:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Linux:
```
~/.config/claude-desktop/claude_desktop_config.json
```

## 🛠️ Setup Steps

### 1. Copy Template
Copy the content from `config/claude_desktop_config.json` to the appropriate location above.

### 2. Replace Placeholders

Replace the following placeholders with your actual values:

#### `<YOUR_PROJECT_PATH>`
Replace with your actual project directory path.

**Example for Windows:**
```json
"<YOUR_PROJECT_PATH>/src/mcp-security"
```
**Becomes:**
```json
"C:\\Users\\YourName\\Documents\\mcp-vulnerability-scanner\\src\\mcp-security"
```

**Example for macOS/Linux:**
```json
"<YOUR_PROJECT_PATH>/src/mcp-security"
```
**Becomes:**
```json
"/home/yourname/mcp-vulnerability-scanner/src/mcp-security"
```

#### `<YOUR_GEMINI_API_KEY>`
Replace with your actual Gemini API key from [Google AI Studio](https://ai.google.dev/).

**Example:**
```json
"GEMINI_API_KEY": "<YOUR_GEMINI_API_KEY>"
```
**Becomes:**
```json
"GEMINI_API_KEY": "AIzaSyC-YourActualApiKeyHere"
```

#### `<PATH_TO_ANALYZE>`
Replace with the directory you want the filesystem server to have access to.

**Example:**
```json
"<PATH_TO_ANALYZE>"
```
**Becomes:**
```json
"C:\\Users\\YourName\\Documents\\projects"
```

### 3. Verify Paths

Ensure all paths exist and are accessible:
- `src/mcp-security/` directory exists
- `src/gemini-mcp-server/dist/gemini_mcp_server.js` file exists
- `src/sqlite/` directory exists
- `src/sqlite/test.db` file exists

### 4. Set Permissions

Ensure Python and Node.js have permission to:
- Execute the MCP servers
- Read/write to the SQLite database
- Access the specified directories

## 🔐 Security Best Practices

### API Key Security
- **Never commit** your actual API key to version control
- Store API keys in environment variables when possible
- Use separate API keys for development and production
- Regularly rotate your API keys

### Path Security
- Use absolute paths to avoid confusion
- Ensure directories have appropriate permissions
- Limit filesystem server access to necessary directories only
- Avoid granting access to system directories

### Configuration Security
- Keep your actual configuration file private
- Use different configurations for different environments
- Regularly review and update configurations

## 🧪 Testing Configuration

After setup, test each MCP server:

1. **Start Claude Desktop** with the new configuration
2. **Test MCP Security**: Try a simple scan command
3. **Test Gemini Integration**: Ask for AI analysis
4. **Test Filesystem Access**: Request file operations
5. **Test SQLite Database**: Check data storage

## 🐛 Troubleshooting

### Common Issues:

**Path not found errors:**
- Check that all paths use correct path separators for your OS
- Verify directories and files exist
- Use absolute paths instead of relative paths

**Permission denied errors:**
- Check file/directory permissions
- Ensure UV and Node.js are properly installed
- Try running Claude Desktop as administrator (Windows) or with sudo (Linux/macOS)

**API key errors:**
- Verify your Gemini API key is valid and active
- Check API quota and usage limits
- Ensure the key has necessary permissions

**Module import errors:**
- Run `uv sync` in each Python project directory
- Run `npm install` in each Node.js project directory
- Check that all dependencies are installed

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Review Claude Desktop logs for error messages
4. Ensure all placeholder values have been replaced

## 🔄 Updates

When updating the project:
1. Check for new configuration options
2. Update your local configuration file
3. Test all MCP servers after updates
4. Keep backups of working configurations 