# MySQL MCP Server

[English](#english) | [中文](#中文)

## English

A MySQL database server based on MCP (Model Context Protocol) that provides database operation capabilities for Cursor IDE.

### ✨ Features

- 🔍 **Data Querying**: Execute SELECT queries with formatted results
- ✏️ **Data Modification**: Support INSERT, UPDATE, DELETE operations
- 🏗️ **Schema Management**: Create tables, add columns, view table structures
- 📊 **Metadata Operations**: List databases and tables, describe table structures
- 🔒 **Security**: Database connection configured through environment variables
- 🚀 **Easy Integration**: Seamless integration with Cursor IDE via MCP protocol

### 📋 Prerequisites

- Python 3.7+
- MySQL 5.7+ or 8.0+
- Cursor IDE with MCP support

### 🚀 Installation & Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Configure Database Connection

Copy the example configuration file:
```bash
cp mcp-config.example.json mcp-config.json
```

Edit `mcp-config.json` with your database connection details:

```json
{
  "mcpServers": {
    "mysql-server": {
      "command": "python",
      "args": ["mysql_mcp_server.py"],
      "env": {
        "MYSQL_HOST": "your-mysql-host",
        "MYSQL_PORT": "3306",
        "MYSQL_DATABASE": "your-database-name",
        "MYSQL_USER": "your-username",
        "MYSQL_PASSWORD": "your-password",
        "MYSQL_CHARSET": "utf8mb4"
      }
    }
  }
}
```

#### 3. Cursor IDE Integration

Add the MCP server configuration to Cursor settings:

1. Open Cursor Settings
2. Search for "MCP"
3. Add your `mcp-config.json` configuration to MCP server settings

### 🛠️ Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `query_database` | Execute SELECT queries | `SELECT * FROM users WHERE age > 18` |
| `execute_sql` | Execute INSERT/UPDATE/DELETE | `INSERT INTO users (name, email) VALUES (...)` |
| `create_table` | Create new tables | Create users table with columns |
| `add_column` | Add columns to existing tables | Add phone column to users table |
| `show_tables` | List all tables in database | - |
| `describe_table` | Show table structure | View columns, types, constraints |
| `show_databases` | List all available databases | - |

### 🔧 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MYSQL_HOST` | ✅ | - | MySQL server host |
| `MYSQL_PORT` | ❌ | 3306 | MySQL server port |
| `MYSQL_DATABASE` | ✅ | - | Database name |
| `MYSQL_USER` | ✅ | - | Database username |
| `MYSQL_PASSWORD` | ✅ | - | Database password |
| `MYSQL_CHARSET` | ❌ | utf8mb4 | Character set |
| `MYSQL_CONNECTION_TIMEOUT` | ❌ | 10 | Connection timeout (seconds) |

### 🔒 Security Features

- 🔐 Database credentials passed via environment variables
- 🛡️ Only safe SQL operation types allowed
- ⚠️ Query result limits to prevent large data output
- 🔍 Basic security checks for all SQL operations

### 🐛 Development & Testing

Run the server directly for testing:
```bash
# Set environment variables
export MYSQL_HOST="your-host"
export MYSQL_USER="your-user"
export MYSQL_PASSWORD="your-password" 
export MYSQL_DATABASE="your-database"

# Run server
python mysql_mcp_server.py
```

### 📄 License

MIT License

### 🤝 Contributing

Issues and Pull Requests are welcome!

---

## 中文

一个基于 MCP (Model Context Protocol) 的 MySQL 数据库服务器，为 Cursor IDE 提供数据库操作功能。

### ✨ 功能特性

- 🔍 **数据查询**: 执行 SELECT 查询并格式化返回结果
- ✏️ **数据修改**: 支持 INSERT, UPDATE, DELETE 操作
- 🏗️ **结构管理**: 创建表、添加列、查看表结构
- 📊 **元数据查看**: 列出数据库、表，查看表结构
- 🔒 **安全控制**: 通过环境变量配置数据库连接信息
- 🚀 **轻松集成**: 通过 MCP 协议无缝集成到 Cursor IDE

### 📋 环境要求

- Python 3.7+
- MySQL 5.7+ 或 8.0+
- 支持 MCP 的 Cursor IDE

### 🚀 安装配置

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 配置数据库连接

复制配置示例文件：
```bash
cp mcp-config.example.json mcp-config.json
```

编辑 `mcp-config.json` 文件，填入您的数据库连接信息：

```json
{
  "mcpServers": {
    "mysql-server": {
      "command": "python", // 可以用项目的绝对路径 如 : /Users/baozi/python-mysql-mcp-server/venv/bin/python
      "args": ["mysql_mcp_server.py"],  // 这里也是,如 : /Users/baozi/python-mysql-mcp-server/mysql_mcp_server.py
      "env": {
        "MYSQL_HOST": "your-mysql-host",
        "MYSQL_PORT": "3306",
        "MYSQL_DATABASE": "your-database-name",
        "MYSQL_USER": "your-username",
        "MYSQL_PASSWORD": "your-password",
        "MYSQL_CHARSET": "utf8mb4"
      }
    }
  }
}
```

#### 3. Cursor IDE 集成

将 MCP 服务器配置添加到 Cursor 的设置中：

1. 打开 Cursor 设置 (Settings)
2. 搜索 "MCP"
3. 在 MCP 服务器配置中添加您的 `mcp-config.json` 配置

### 🛠️ 可用工具

| 工具 | 描述 | 示例 |
|------|------|------|
| `query_database` | 执行 SELECT 查询 | `SELECT * FROM users WHERE age > 18` |
| `execute_sql` | 执行 INSERT/UPDATE/DELETE | `INSERT INTO users (name, email) VALUES (...)` |
| `create_table` | 创建新表 | 创建带有列定义的用户表 |
| `add_column` | 为现有表添加列 | 为用户表添加电话列 |
| `show_tables` | 列出数据库中的所有表 | - |
| `describe_table` | 查看表结构 | 查看列、类型、约束 |
| `show_databases` | 列出所有可用数据库 | - |

### 🔧 环境变量说明

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `MYSQL_HOST` | ✅ | - | MySQL 服务器地址 |
| `MYSQL_PORT` | ❌ | 3306 | MySQL 服务器端口 |
| `MYSQL_DATABASE` | ✅ | - | 数据库名称 |
| `MYSQL_USER` | ✅ | - | 数据库用户名 |
| `MYSQL_PASSWORD` | ✅ | - | 数据库密码 |
| `MYSQL_CHARSET` | ❌ | utf8mb4 | 字符集 |
| `MYSQL_CONNECTION_TIMEOUT` | ❌ | 10 | 连接超时时间(秒) |

### 🔒 安全注意事项

- 🔐 数据库凭据通过环境变量传递，避免硬编码
- 🛡️ 只允许安全的 SQL 操作类型
- ⚠️ 查询结果有行数限制，防止大量数据输出
- 🔍 所有 SQL 操作都会进行基本的安全检查

### 🐛 开发和调试

直接运行服务器进行测试：
```bash
# 设置环境变量
export MYSQL_HOST="your-host"
export MYSQL_USER="your-user"
export MYSQL_PASSWORD="your-password"
export MYSQL_DATABASE="your-database"

# 运行服务器
python mysql_mcp_server.py
```

### 📄 许可证

MIT License

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！ 