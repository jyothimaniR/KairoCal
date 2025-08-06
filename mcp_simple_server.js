#!/usr/bin/env node

/**
 * Simple MCP Server for Website Cloning and Frontend Creation
 * This server provides tools to fetch website content and analyze structure
 */

const fs = require('fs').promises;
const https = require('https');
const http = require('http');
const { URL } = require('url');

class SimpleMCPServer {
  constructor() {
    this.tools = [
      {
        name: "fetch_website",
        description: "Fetch and analyze a website's HTML structure",
        inputSchema: {
          type: "object",
          properties: {
            url: {
              type: "string",
              description: "URL of the website to fetch"
            }
          },
          required: ["url"]
        }
      },
      {
        name: "analyze_structure", 
        description: "Analyze HTML structure and extract components",
        inputSchema: {
          type: "object",
          properties: {
            html: {
              type: "string",
              description: "HTML content to analyze"
            }
          },
          required: ["html"]
        }
      }
    ];
  }

  async handleRequest(request) {
    const { method, params } = request;

    switch (method) {
      case 'initialize':
        return {
          protocolVersion: "2024-11-05",
          capabilities: {
            tools: {}
          },
          serverInfo: {
            name: "website-cloner",
            version: "1.0.0"
          }
        };

      case 'tools/list':
        return { tools: this.tools };

      case 'tools/call':
        return await this.callTool(params.name, params.arguments);

      default:
        throw new Error(`Unknown method: ${method}`);
    }
  }

  async callTool(name, args) {
    switch (name) {
      case 'fetch_website':
        return await this.fetchWebsite(args.url);
      case 'analyze_structure':
        return await this.analyzeStructure(args.html);
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  }

  async fetchWebsite(url) {
    try {
      const urlObj = new URL(url);
      const module = urlObj.protocol === 'https:' ? https : http;
      
      return new Promise((resolve, reject) => {
        const req = module.get(url, (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            resolve({
              content: [{
                type: "text",
                text: JSON.stringify({
                  url: url,
                  status: res.statusCode,
                  headers: res.headers,
                  html: data.substring(0, 10000), // Limit size
                  size: data.length
                }, null, 2)
              }]
            });
          });
        });
        
        req.on('error', reject);
        req.setTimeout(10000, () => reject(new Error('Timeout')));
      });
    } catch (error) {
      return {
        content: [{
          type: "text", 
          text: `Error fetching website: ${error.message}`
        }]
      };
    }
  }

  async analyzeStructure(html) {
    try {
      // Simple HTML analysis
      const analysis = {
        hasNavigation: /<nav/i.test(html),
        hasHeader: /<header/i.test(html),
        hasFooter: /<footer/i.test(html),
        hasSidebar: /<aside/i.test(html) || /sidebar/i.test(html),
        components: [],
        styles: []
      };

      // Extract common components
      const components = html.match(/<(nav|header|footer|aside|main|section|article)[^>]*>/gi) || [];
      analysis.components = components;

      // Extract CSS links
      const cssLinks = html.match(/<link[^>]*rel=["']stylesheet["'][^>]*>/gi) || [];
      analysis.styles = cssLinks;

      return {
        content: [{
          type: "text",
          text: JSON.stringify(analysis, null, 2)
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: `Error analyzing structure: ${error.message}`
        }]
      };
    }
  }
}

// Start server
const server = new SimpleMCPServer();

process.stdin.setEncoding('utf8');
process.stdin.on('readable', async () => {
  const chunk = process.stdin.read();
  if (chunk !== null) {
    try {
      const request = JSON.parse(chunk.trim());
      const response = await server.handleRequest(request);
      console.log(JSON.stringify(response));
    } catch (error) {
      console.log(JSON.stringify({
        error: { message: error.message }
      }));
    }
  }
});

console.error('Simple MCP Server started');
