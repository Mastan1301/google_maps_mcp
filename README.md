# Google Maps MCP Server

This project provides a Python-based Model Context Protocol (MCP) server that leverages the Google Maps and Places APIs to answer queries about local businesses and tourist attractions in India. It is designed to help users and developers easily retrieve information such as "What are the best cafes in Bangalore?" or "Top-rated tourist places near Hyderabad" using a simple MCP interface.

## Features
- Query Google Maps for places, restaurants, tourist attractions, and more
- Easily configurable with your own Google Maps API key
- Modular, maintainable, and testable codebase
- Ready for extension and contribution

## Getting Started

### Prerequisites
- Python 3.8+
- A Google Maps API key ([Get one here](https://developers.google.com/maps/documentation/places/web-service/get-api-key))

### Run the MCP server
- Install `uvx` using
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Run the MCP server-
```bash
uvx google-mcp-server
```

## Contributing
- Fork this repository and create a feature branch.
- Add or update tests for your changes.
- Submit a pull request with a clear description of your changes.

### Setup Steps
- **Clone the repository:**
   ```bash
   git clone <your-fork-url>
   cd google_maps_mcp
   ```
- **Build:**
    Go to the root of the project and run-
   ```bash
   uv build
   ```
- **Set your Google Maps API key:**
   - You can set it in your environment or in the config (see below).
   - Example (Linux/macOS):
     ```bash
     export GOOGLE_MAPS_API_KEY=your_api_key_here
     ```
- **Install the local build as an executable:**
    Ensure that your `PATH` env var contains the `~/.local/bin` path.

    If not, add this to the end of your `~/.bashrc` file.
    ```
    export PATH=$PATH:~/.local/bin
    ```
    and then run-
    ```
    source ~/.bashrc
    ```

6. **Run the executable containing the MCP server:**
   ```bash
   uvx dist/google_maps_mcp-1.0.0-py3-none-any.whl
   ```

## Visual Studio Code: MCP Server Configuration Example

```json
"mcp": {
        "servers": {
            "google_maps_mcp_server":{
                "type": "stdio",
                "command": "uvx",
                "args": ["google-maps-mcp"],
                "env": {
                    "GOOGLE_MAPS_API_KEY": "<your google maps API key>"
                }
            }
        }
    }
```