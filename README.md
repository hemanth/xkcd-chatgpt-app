# xkcd-chatgpt-app

A ChatGPT app that fetches and displays XKCD comics using MCP (Model Context Protocol) and the OpenAI Apps SDK.

**Authentication: NONE** - All endpoints are publicly accessible.

## Features

- **XKCD Comic Viewer**: Beautiful widget displaying comics with title, image, alt text, and date
- Fetch latest or specific comics by number
- URL support: Automatically extracts comic numbers from XKCD URLs
- Clean black and white UI with responsive layout

## Quick Start

```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run
python main.py
```

Server runs at `http://0.0.0.0:8000`

## Using with ChatGPT

1. Start the server: `python main.py`
2. In ChatGPT, connect to MCP server at `http://localhost:8000/mcp`
3. Request comics using:
   - URLs: `https://xkcd.com/327/` or `xkcd.com/327`
   - Numbers: `#327` or `Show me XKCD comic 327`
   - Natural language: `Show me the latest XKCD comic`

## Project Structure

```
xkcd-chatgpt-app/
├── main.py                    # MCP server entry point
├── src/
│   └── xkcd_app/              # Application package
│       ├── models.py          # Data models and schemas
│       ├── widgets.py         # Widget definitions
│       ├── handlers.py        # MCP request handlers
│       ├── html_generator.py  # HTML generation
│       └── xkcd_client.py     # XKCD API client
└── requirements.txt           # Dependencies
```

## Development

Add new widgets using the scaffold CLI:
```bash
create-chatgpt-app add-widget --identifier my-widget --title "My Widget"
```

API documentation available at:
- OpenAPI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT