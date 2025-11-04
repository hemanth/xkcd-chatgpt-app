# xkcd-chatgpt-app

An app to fetch and display XKCD comics in UI widgets

## Description

This is a ChatGPT app built using the OpenAI Apps SDK and MCP (Model Context Protocol).

**Authentication: NONE** - This app is completely open and requires no authentication. All endpoints are publicly accessible.

## Features

### Widgets

- **XKCD Comic Viewer** (`xkcd-viewer`): Fetches and displays XKCD comics in a beautiful UI widget

### Functionality

- Fetch the latest XKCD comic
- Fetch specific XKCD comics by number
- Display comic with title, image, alt text, and publication date
- Clean black and white UI design with responsive layout
- Error handling for invalid comic numbers

## Installation

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the development server:

```bash
python main.py
```

The server will be running at `http://0.0.0.0:8000`

## Public Endpoints (No Auth Required)

The following endpoints are publicly accessible without any authentication:

- **Root:** `GET http://localhost:8000/` - Server info and available endpoints
- **Health Check:** `GET http://localhost:8000/health` - Health status
- **MCP Endpoint:** `http://localhost:8000/mcp` - MCP server for ChatGPT integration
- **Messages:** `http://localhost:8000/mcp/messages` - MCP messages endpoint

Test it:
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
```

## Using with ChatGPT

To use this widget in ChatGPT:

1. Make sure the server is running on `http://0.0.0.0:8000`
2. In ChatGPT, connect to the MCP server at `http://localhost:8000/mcp`
3. Once connected, you can ask ChatGPT with:
   - **URLs:** `https://xkcd.com/327/` or `xkcd.com/327`
   - **Comic numbers:** `#327` or `Show me XKCD comic 327`
   - **Natural language:** `Show me the latest XKCD comic`

The widget will render beautifully in the ChatGPT interface with the comic image, title, alt text, and metadata.

### URL Support

The viewer automatically extracts comic numbers from XKCD URLs:
- `https://xkcd.com/327/` → Comic #327
- `http://xkcd.com/327` → Comic #327
- `xkcd.com/327` → Comic #327

## Development

### Adding a New Widget

Use the scaffold CLI to add new widgets:

```bash
create-chatgpt-app add-widget --identifier my-widget --title "My Widget"
```

Or run it interactively:

```bash
create-chatgpt-app add-widget
```

### Project Structure

```
xkcd-chatgpt-app/
├── main.py                    # Main MCP server entry point
├── src/
│   └── xkcd_app/              # Application package
│       ├── __init__.py        # Package initialization (v1.0.0)
│       ├── models.py          # Data models and schemas
│       ├── widgets.py         # Widget definitions and registry
│       ├── handlers.py        # MCP request handlers
│       ├── html_generator.py  # HTML generation for comics
│       └── xkcd_client.py     # XKCD API client
├── tests/                     # Test directory
├── docs/                      # Documentation directory
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Testing

Install test dependencies first:

```bash
pip install pytest pytest-asyncio httpx
```

Then create tests in a `tests/` directory.

## MCP Inspector

To test your MCP server with the MCP Inspector:

```bash
npm install -g @modelcontextprotocol/inspector
mcp-inspector
```

Then connect to `http://0.0.0.0:8000/mcp`.

## Docker

To add Docker support, create a `Dockerfile` in your project directory.

## API Documentation

Once the server is running, visit:
- OpenAPI docs: `http://0.0.0.0:8000/docs`
- ReDoc: `http://0.0.0.0:8000/redoc`

## License

MIT