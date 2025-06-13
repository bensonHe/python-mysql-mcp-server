#!/usr/bin/env python3
"""
MySQL MCP Server
Provides database operations for Cursor IDE through MCP protocol
"""

import json
import sys
import os
import traceback
from typing import Dict, List, Any, Optional
import mysql.connector
from mysql.connector import Error

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', '3306')),
    'database': os.getenv('MYSQL_DATABASE', 'test'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'charset': os.getenv('MYSQL_CHARSET', 'utf8mb4'),
    'autocommit': True,
    'connection_timeout': int(os.getenv('MYSQL_CONNECTION_TIMEOUT', '10'))
}

class MySQLMCPServer:
    def __init__(self):
        self.connection = None
        
        # Validate required environment variables
        required_vars = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        self.tools = [
            {
                "name": "query_database",
                "description": "Execute SELECT queries to retrieve data from database",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SQL SELECT query to execute"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of rows to return (default: 100)",
                            "default": 100
                        }
                    },
                    "required": ["sql"]
                }
            },
            {
                "name": "execute_sql",
                "description": "Execute INSERT, UPDATE, DELETE statements",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SQL statement to execute (INSERT, UPDATE, DELETE)"
                        }
                    },
                    "required": ["sql"]
                }
            },
            {
                "name": "create_table",
                "description": "Create a new table in the database",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Name of the table to create"
                        },
                        "columns": {
                            "type": "string",
                            "description": "Column definitions (e.g., 'id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), email VARCHAR(255)')"
                        }
                    },
                    "required": ["table_name", "columns"]
                }
            },
            {
                "name": "add_column",
                "description": "Add a new column to an existing table",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Name of the table to modify"
                        },
                        "column_definition": {
                            "type": "string",
                            "description": "Column definition (e.g., 'age INT DEFAULT 0', 'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')"
                        }
                    },
                    "required": ["table_name", "column_definition"]
                }
            },
            {
                "name": "show_tables",
                "description": "List all tables in the database",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "describe_table",
                "description": "Show the structure of a table (columns, types, etc.)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Name of the table to describe"
                        }
                    },
                    "required": ["table_name"]
                }
            },
            {
                "name": "show_databases",
                "description": "List all available databases",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]

    def get_connection(self):
        """Get or create database connection"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**DB_CONFIG)
            return self.connection
        except Error as e:
            raise Exception(f"Database connection failed: {e}")

    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def handle_initialize(self, request: Dict) -> Dict:
        """Handle initialize request"""
        return {
            "jsonrpc": "2.0",
            "id": request["id"],
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "mysql-mcp-server",
                    "version": "1.0.0"
                }
            }
        }

    def handle_tools_list(self, request: Dict) -> Dict:
        """Handle tools/list request"""
        return {
            "jsonrpc": "2.0",
            "id": request["id"],
            "result": {
                "tools": self.tools
            }
        }

    def handle_tools_call(self, request: Dict) -> Dict:
        """Handle tools/call request"""
        try:
            tool_name = request["params"]["name"]
            arguments = request["params"].get("arguments", {})

            if tool_name == "query_database":
                result = self.query_database(arguments)
            elif tool_name == "execute_sql":
                result = self.execute_sql(arguments)
            elif tool_name == "create_table":
                result = self.create_table(arguments)
            elif tool_name == "add_column":
                result = self.add_column(arguments)
            elif tool_name == "show_tables":
                result = self.show_tables(arguments)
            elif tool_name == "describe_table":
                result = self.describe_table(arguments)
            elif tool_name == "show_databases":
                result = self.show_databases(arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
            }
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {str(e)}"
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": -32000,
                    "message": error_msg
                }
            }

    def query_database(self, args: Dict) -> str:
        """Execute SELECT query"""
        sql = args["sql"].strip()
        limit = args.get("limit", 100)
        
        if not sql.upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed for query_database")
        
        # Add LIMIT if not present
        if "LIMIT" not in sql.upper():
            sql += f" LIMIT {limit}"
        
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            
            if not results:
                return "Query executed successfully. No rows returned."
            
            # Format results as table
            output = f"Query: {sql}\n"
            output += f"Rows returned: {len(results)}\n\n"
            
            # Table headers
            headers = list(results[0].keys())
            output += "| " + " | ".join(headers) + " |\n"
            output += "|" + "|".join(["-" * (len(h) + 2) for h in headers]) + "|\n"
            
            # Table rows
            for row in results:
                values = [str(row[h]) if row[h] is not None else "NULL" for h in headers]
                output += "| " + " | ".join(values) + " |\n"
            
            return output
            
        finally:
            cursor.close()

    def execute_sql(self, args: Dict) -> str:
        """Execute INSERT, UPDATE, DELETE statements"""
        sql = args["sql"].strip()
        
        # Security check - only allow specific statements
        sql_upper = sql.upper()
        allowed_statements = ["INSERT", "UPDATE", "DELETE"]
        if not any(sql_upper.startswith(stmt) for stmt in allowed_statements):
            raise ValueError("Only INSERT, UPDATE, DELETE statements are allowed")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            conn.commit()
            
            affected_rows = cursor.rowcount
            return f"SQL executed successfully. Affected rows: {affected_rows}\nSQL: {sql}"
            
        finally:
            cursor.close()

    def create_table(self, args: Dict) -> str:
        """Create a new table"""
        table_name = args["table_name"]
        columns = args["columns"]
        
        sql = f"CREATE TABLE {table_name} ({columns})"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            conn.commit()
            return f"Table '{table_name}' created successfully.\nSQL: {sql}"
            
        finally:
            cursor.close()

    def add_column(self, args: Dict) -> str:
        """Add column to existing table"""
        table_name = args["table_name"]
        column_definition = args["column_definition"]
        
        sql = f"ALTER TABLE {table_name} ADD COLUMN {column_definition}"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            conn.commit()
            return f"Column added to table '{table_name}' successfully.\nSQL: {sql}"
            
        finally:
            cursor.close()

    def show_tables(self, args: Dict) -> str:
        """List all tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if not tables:
                return "No tables found in the database."
            
            output = "Tables in database:\n"
            for i, (table,) in enumerate(tables, 1):
                output += f"{i}. {table}\n"
            
            return output
            
        finally:
            cursor.close()

    def describe_table(self, args: Dict) -> str:
        """Describe table structure"""
        table_name = args["table_name"]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            if not columns:
                return f"Table '{table_name}' not found or has no columns."
            
            output = f"Structure of table '{table_name}':\n\n"
            output += "| Field | Type | Null | Key | Default | Extra |\n"
            output += "|-------|------|------|-----|---------|-------|\n"
            
            for col in columns:
                field, type_, null, key, default, extra = col
                default_str = str(default) if default is not None else "NULL"
                output += f"| {field} | {type_} | {null} | {key} | {default_str} | {extra} |\n"
            
            return output
            
        finally:
            cursor.close()

    def show_databases(self, args: Dict) -> str:
        """List all databases"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            
            output = "Available databases:\n"
            for i, (db,) in enumerate(databases, 1):
                current = " (current)" if db == DB_CONFIG['database'] else ""
                output += f"{i}. {db}{current}\n"
            
            return output
            
        finally:
            cursor.close()

    def run(self):
        """Main server loop"""
        try:
            for line in sys.stdin:
                try:
                    request = json.loads(line.strip())
                    
                    if request["method"] == "initialize":
                        response = self.handle_initialize(request)
                    elif request["method"] == "tools/list":
                        response = self.handle_tools_list(request)
                    elif request["method"] == "tools/call":
                        response = self.handle_tools_call(request)
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {
                                "code": -32601,
                                "message": f"Method not found: {request['method']}"
                            }
                        }
                    
                    print(json.dumps(response))
                    sys.stdout.flush()
                    
                except json.JSONDecodeError:
                    # Ignore invalid JSON
                    continue
                except Exception as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id", None),
                        "error": {
                            "code": -32000,
                            "message": f"Internal error: {str(e)}"
                        }
                    }
                    print(json.dumps(error_response))
                    sys.stdout.flush()
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.close_connection()

if __name__ == "__main__":
    server = MySQLMCPServer()
    server.run() 