from . import mcp_server
import asyncio

def main():
    """Main entry point for the package."""
    asyncio.run(mcp_server.main())

__all__ = ['main', 'mcp_server']