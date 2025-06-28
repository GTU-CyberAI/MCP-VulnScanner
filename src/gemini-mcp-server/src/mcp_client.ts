/**
 * MCP Client Implementation - Model Context Protocol Client
 * 
 * This module provides a comprehensive client implementation for the Model Context Protocol (MCP).
 * It handles server process spawning, WebSocket communication, and JSON-RPC messaging
 * for seamless integration with various MCP servers.
 * 
 * Key Features:
 * - Process spawning and lifecycle management
 * - WebSocket-based communication
 * - JSON-RPC protocol implementation
 * - Tool discovery and invocation
 * - Robust error handling and logging
 * 
 * @author MCP-Based Vulnerability Scanner Team
 * @version 1.0.0
 */

import { spawn, ChildProcess } from 'child_process';
import WebSocket from 'ws';

// Interface definitions for MCP server configuration
export interface MCPServerParameters {
  command: string;           // Command to execute the MCP server
  args: string[];           // Command-line arguments
  env?: NodeJS.ProcessEnv | null;  // Environment variables
}

// Interface for MCP client operations
export interface MCPClient {
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  call_tool(toolName: string): (args: any) => Promise<any>;
  list_tools(): Promise<any[]>;
}

/**
 * MCP Client Implementation
 * 
 * Handles communication with MCP servers through process spawning and WebSocket connections.
 * Provides a clean interface for tool discovery and invocation.
 */
export class MCPClientImpl implements MCPClient {
  private process: ChildProcess | null = null;
  private socket: WebSocket | null = null;
  private messageQueue: Buffer[] = [];
  private currentResolver: ((value: Buffer) => void) | null = null;
  private rpcInterface: {
    read: () => Promise<Buffer>;
    write: (data: Buffer) => Promise<void>;
  } | null = null;

  /**
   * Initialize MCP Client with server parameters
   * 
   * @param serverParams - Configuration for the MCP server to connect to
   */
  constructor(private serverParams: MCPServerParameters) {
    console.log('MCPClientImpl initialized with params:', {
      command: serverParams.command,
      args: serverParams.args,
      env: serverParams.env ? Object.keys(serverParams.env) : null
    });
  }

  /**
   * Connect to the MCP server
   * 
   * Spawns the server process and establishes a WebSocket connection for communication.
   * Handles process lifecycle events and error conditions.
   */
  async connect(): Promise<void> {
    console.log('Attempting to connect to MCP server...');
    return new Promise((resolve, reject) => {
      console.log('Spawning process:', this.serverParams.command, this.serverParams.args);
      
      // Spawn the MCP server process with configured environment
      this.process = spawn(this.serverParams.command, this.serverParams.args, {
        env: {
          ...process.env,
          ...this.serverParams.env
        }
      });

      // Validate process creation
      if (!this.process) {
        const error = new Error('Failed to start MCP server process');
        console.error('Spawn failed:', error);
        reject(error);
        return;
      }

      console.log('Process spawned with PID:', this.process.pid);

      // Handle process errors (e.g., command not found, permission denied)
      this.process.on('error', (err: Error) => {
        console.error('MCP server process error:', err);
        console.error('Error details:', {
          message: err.message,
          name: err.name,
          stack: err.stack
        });
        reject(new Error(`Failed to execute MCP server: ${err.message}`));
        this.process = null;
      });

      // Handle process exit events
      this.process.on('exit', (code: number, signal: string) => {
        console.warn(`MCP server process exited with code ${code} and signal ${signal}`);
        this.process = null;
      });

      // Monitor stdout for WebSocket URL discovery
      let wsUrl = '';
      this.process.stdout?.on('data', (data: Buffer) => {
        const msg = data.toString('utf-8');
        console.log('MCP server stdout:', msg);
        
        // Parse WebSocket URL from server output
        const match = msg.match(/ws:\/\/localhost:\d+/);
        if (match) {
          wsUrl = match[0];
          console.log('WebSocket URL found:', wsUrl);
          this.createWebSocket(wsUrl).then(resolve).catch(reject);
        }
      });

      // Log server error output for debugging
      this.process.stderr?.on('data', (data: Buffer) => {
        console.error(`MCP server stderr: ${data.toString('utf-8')}`);
      });
    });
  }

  /**
   * Create and configure WebSocket connection
   * 
   * Establishes WebSocket communication with the MCP server and sets up
   * the JSON-RPC interface for tool calls and responses.
   * 
   * @param wsUrl - WebSocket URL provided by the MCP server
   */
  private async createWebSocket(wsUrl: string): Promise<void> {
    console.log('Creating WebSocket connection to:', wsUrl);
    return new Promise((resolve, reject) => {
      this.socket = new WebSocket(wsUrl);

      // Handle successful WebSocket connection
      this.socket.on('open', () => {
        console.log('WebSocket connection established');
        
        // Set up JSON-RPC communication interface
        this.rpcInterface = {
          /**
           * Read messages from the WebSocket
           * 
           * Handles message queuing and asynchronous message delivery
           * for JSON-RPC communication.
           */
          read: async () => {
            console.log('RPC read called');
            return new Promise<Buffer>((resolveRead) => {
              // Check if messages are already queued
              if (this.messageQueue.length > 0) {
                const message = Buffer.concat(this.messageQueue);
                this.messageQueue = [];
                console.log('Reading from message queue:', message.toString());
                resolveRead(message);
              } else {
                // Wait for next message
                console.log('Waiting for message...');
                this.currentResolver = resolveRead;
              }
            });
          },
          
          /**
           * Write messages to the WebSocket
           * 
           * Sends JSON-RPC messages to the MCP server with error handling.
           * 
           * @param data - Message data to send
           */
          write: async (data: Buffer) => {
            console.log('RPC write called with data:', data.toString());
            if (!this.socket?.readyState) {
              const error = new Error('WebSocket not connected');
              console.error('Write failed:', error);
              throw error;
            }
            this.socket.send(data);
            console.log('Data sent successfully');
          },
        };
        resolve();
      });

      // Handle incoming WebSocket messages
      this.socket.on('message', (data: WebSocket.Data) => {
        console.log('WebSocket message received:', data.toString());
        const buffer = Buffer.from(data as Buffer);
        
        // Resolve pending read operation or queue message
        if (this.currentResolver) {
          console.log('Resolving pending read');
          this.currentResolver(buffer);
          this.currentResolver = null;
        } else {
          console.log('Queueing message');
          this.messageQueue.push(buffer);
        }
      });

      // Handle WebSocket errors
      this.socket.on('error', (err: Error) => {
        console.error('WebSocket error:', {
          message: err.message,
          name: err.name,
          stack: err.stack
        });
        reject(new Error(`WebSocket connection failed: ${err.message}`));
      });

      // Handle WebSocket closure
      this.socket.on('close', (code: number, reason: Buffer) => {
        console.log(`WebSocket connection closed with code ${code}`, {
          reason: reason.toString(),
          wasClean: code === 1000
        });
      });

      // Set connection timeout to prevent hanging
      setTimeout(() => {
        if (this.socket?.readyState !== WebSocket.OPEN) {
          const error = new Error('WebSocket connection timeout');
          console.error('Connection timeout:', error);
          reject(error);
        }
      }, 10000); // 10 second timeout
    });
  }

  /**
   * List available tools from the MCP server
   * 
   * Sends a JSON-RPC request to discover all tools available on the connected
   * MCP server and returns their metadata.
   * 
   * @returns Promise resolving to array of tool metadata
   */
  async list_tools(): Promise<any[]> {
    if (!this.rpcInterface) {
      throw new Error('Not connected to MCP server');
    }

    // Construct JSON-RPC request for tool discovery
    const request = {
      jsonrpc: '2.0',
      method: 'list_tools',
      id: Math.floor(Math.random() * 1000000),
    };

    // Send request and wait for response
    await this.rpcInterface.write(Buffer.from(JSON.stringify(request)));
    const response = await this.rpcInterface.read();
    const result = JSON.parse(response.toString());

    // Handle JSON-RPC errors
    if (result.error) {
      throw new Error(result.error.message);
    }

    return result.result;
  }

  /**
   * Create a tool calling function
   * 
   * Returns a function that can be used to call a specific tool on the MCP server.
   * The returned function handles JSON-RPC communication and error handling.
   * 
   * @param toolName - Name of the tool to create a caller for
   * @returns Function that calls the specified tool with given arguments
   */
  call_tool(toolName: string): (args: any) => Promise<any> {
    const rpcInterface = this.rpcInterface;
    if (!rpcInterface) {
      throw new Error('Not connected to MCP server');
    }

    /**
     * Tool calling function
     * 
     * Executes the specified tool with provided arguments through JSON-RPC.
     * 
     * @param args - Arguments to pass to the tool
     * @returns Promise resolving to tool execution result
     */
    return async (args: any) => {
      // Construct JSON-RPC tool call request
      const request = {
        jsonrpc: '2.0',
        method: toolName,
        params: args,
        id: Math.floor(Math.random() * 1000000),
      };

      await rpcInterface.write(Buffer.from(JSON.stringify(request)));
      const response = await rpcInterface.read();
      const result = JSON.parse(response.toString());

      if (result.error) {
        throw new Error(result.error.message);
      }

      return result.result;
    };
  }

  /**
   * Disconnect from the MCP server
   * 
   * Gracefully closes the WebSocket connection and terminates the server process.
   * Cleans up all resources and handles cleanup errors.
   */
  async disconnect(): Promise<void> {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.close();
      this.socket = null;
    }

    if (this.process) {
      this.process.kill();
      this.process = null;
    }
  }
} 