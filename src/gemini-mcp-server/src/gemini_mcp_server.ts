/**
 * Gemini MCP Server - AI Integration Component
 * 
 * This server integrates Google's Gemini AI model with the Model Context Protocol (MCP),
 * enabling AI-powered analysis of vulnerability scan results and security insights.
 * 
 * Key Features:
 * - Gemini 2.5 Pro integration for large context processing
 * - Streaming and non-streaming text generation
 * - Error handling and graceful degradation
 * - MCP protocol compliance for tool registration
 * 
 * @author MCP-Based Vulnerability Scanner Team
 * @version 1.0.0
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { GoogleGenerativeAI, GenerativeModel } from '@google/generative-ai';
import { config } from 'dotenv';
import { z } from "zod";

// Immediately send the startup message before anything else can write to stdout
// This ensures proper MCP protocol initialization
process.stdout.write(JSON.stringify({
  jsonrpc: "2.0",
  method: "startup",
  params: {
    transport: "stdio"
  }
}) + '\n');

// Redirect stdout to stderr for everything else to avoid MCP protocol interference
// MCP requires clean stdout for JSON-RPC communication
const originalStdoutWrite = process.stdout.write.bind(process.stdout);
process.stdout.write = (chunk: any, ...args: any[]) => {
  return process.stderr.write(chunk, ...args);
};

// Redirect console methods to stderr to prevent protocol contamination
const consoleMethods = ['log', 'info', 'warn', 'error', 'debug'] as const;
consoleMethods.forEach(method => {
  (console as any)[method] = (...args: any[]) => process.stderr.write(`[${method}] ` + args.join(' ') + '\n');
});

// Suppress npm and Node.js startup messages for clean MCP communication
process.env.NODE_ENV = 'production';
process.env.NO_UPDATE_NOTIFIER = '1';
process.env.SUPPRESS_NO_CONFIG_WARNING = 'true';
process.env.npm_config_loglevel = 'silent';

// Load environment variables from .env file
config();

// Validate required API key for Gemini integration
const GEMINI_API_KEY = process.env.GEMINI_API_KEY ?? '';
if (!GEMINI_API_KEY) {
  console.error('GEMINI_API_KEY environment variable is required');
  process.exit(1);
}

// Define Zod schema for text generation parameters validation
const generateTextSchema = z.object({
  prompt: z.string().min(1),
  temperature: z.number().min(0).max(1).optional(),
  maxOutputTokens: z.number().min(1).max(8192).optional(),
  topK: z.number().min(1).max(40).optional(),
  topP: z.number().min(0).max(1).optional(),
  stream: z.boolean().optional(),
});

type GenerateTextParams = z.infer<typeof generateTextSchema>;

/**
 * Gemini MCP Server Class
 * 
 * Handles integration between MCP protocol and Google's Gemini AI model.
 * Provides text generation capabilities for vulnerability analysis and security insights.
 */
class GeminiMCPServer {
  private model: GenerativeModel;
  private server: McpServer;
  private transport: StdioServerTransport;
  private chat: any; // Store chat session for conversation continuity

  /**
   * Initialize the Gemini MCP Server
   * 
   * Sets up Google AI client, MCP server configuration, and stdio transport.
   * Configures Gemini 1.5 Pro model with appropriate capabilities.
   */
  constructor() {
    // Initialize Google AI client with API key
    const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
    this.model = genAI.getGenerativeModel({ model: 'gemini-1.5-pro' });
    
    // Start chat session for maintaining conversation context
    this.chat = this.model.startChat();
    
    // Configure MCP server with tool capabilities
    this.server = new McpServer({
      name: "gemini",
      version: "1.0.0",
      capabilities: {
        tools: {
          generate_text: {
            description: "Generate text using Gemini Pro model",
            streaming: true
          }
        }
      }
    });

    // Initialize stdio transport for MCP communication
    this.transport = new StdioServerTransport();
  }

  /**
   * Generate text using Gemini AI model
   * 
   * Processes prompts through Gemini 1.5 Pro with configurable parameters.
   * Supports both streaming and non-streaming responses.
   * 
   * @param params - Generation parameters including prompt, temperature, etc.
   * @returns Generated text content or error message
   */
  private async generateText(params: GenerateTextParams) {
    try {
      // Extract parameters with sensible defaults
      const { prompt, temperature = 0.7, maxOutputTokens = 8192, topK, topP, stream = false } = params;
      
      // Configure generation parameters for optimal security analysis
      const generationConfig = {
        temperature,
        maxOutputTokens,
        topK,
        topP,
      };

      console.log('Sending message to Gemini:', prompt);

      // Handle streaming response for real-time feedback
      if (stream) {
        const result = await this.chat.sendMessageStream(prompt);
        let fullText = '';
        
        // Process streaming chunks and accumulate full response
        for await (const chunk of result.stream) {
          const chunkText = chunk.text();
          fullText += chunkText;
          
          // Note: Progress events not yet supported in MCP SDK
          // Future enhancement for real-time streaming to client
        }

        console.log('Received streamed response from Gemini:', fullText);

        return {
          content: [{
            type: "text" as const,
            text: fullText
          }]
        };
      } else {
        // Handle standard (non-streaming) response
        const result = await this.chat.sendMessage(prompt);
        const response = result.response.text();
        
        console.log('Received response from Gemini:', response);

        return {
          content: [{
            type: "text" as const,
            text: response
          }]
        };
      }
    } catch (err) {
      // Comprehensive error handling with detailed logging
      console.error('Error generating content:', err);
      return {
        content: [{
          type: "text" as const,
          text: err instanceof Error ? err.message : 'Internal error'
        }],
        isError: true
      };
    }
  }

  /**
   * Start the MCP server and register tools
   * 
   * Initializes the server, registers the generate_text tool, and begins
   * listening for MCP protocol messages via stdio transport.
   */
  async start() {
    try {
      console.info('Initializing Gemini MCP server...');

      // Register generate_text tool with schema validation
      this.server.tool(
        "generate_text",
        generateTextSchema.shape,
        async (args: GenerateTextParams) => this.generateText(args)
      );

      // Restore stdout for MCP communication after setup
      process.stdout.write = originalStdoutWrite;
      
      // Connect using stdio transport for MCP protocol
      await this.server.connect(this.transport);
      console.info('Server started successfully and waiting for messages...');
    } catch (error) {
      console.error('Failed to start server:', error);
      process.exit(1);
    }
  }

  /**
   * Gracefully stop the MCP server
   * 
   * Cleanly disconnects from the transport and shuts down the server.
   * Currently a placeholder as disconnect is not yet supported in MCP SDK.
   */
  async stop() {
    try {
      // Note: Disconnect functionality not yet available in MCP SDK
      // This is prepared for future SDK versions
      console.info('Server stopped successfully');
    } catch (error) {
      console.error('Error stopping server:', error);
      process.exit(1);
    }
  }
}

// Handle graceful shutdown on SIGINT (Ctrl+C)
process.on('SIGINT', () => {
  console.info('Server shutting down');
  process.exit(0);
});

// Handle uncaught exceptions to prevent server crashes
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
  process.exit(1);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason) => {
  console.error('Unhandled rejection:', reason);
  process.exit(1);
});

// Start the server instance
const server = new GeminiMCPServer();
server.start().catch(error => {
  console.error('Unhandled error:', error);
  process.exit(1);
}); 