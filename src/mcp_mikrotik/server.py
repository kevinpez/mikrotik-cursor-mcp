import sys
import logging
from mcp_mikrotik.logger import app_logger
from mcp_mikrotik.serve import serve
from mcp_mikrotik.settings.configuration import mikrotik_config
from mcp_mikrotik.connection_manager import cleanup_connections

def main():
    """
    Entry point for the MikroTik Cursor MCP server.
    Optimized for Cursor IDE with category-based tool organization.
    """
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description='MikroTik Cursor MCP Server - Optimized for Cursor IDE')
    parser.add_argument('--host', type=str, help='MikroTik device IP/hostname')
    parser.add_argument('--username', type=str, help='SSH username')
    parser.add_argument('--password', type=str, help='SSH password')
    parser.add_argument('--port', type=int, help='SSH port (default: from env or 22)')
    
    args = parser.parse_args()
    
    if args.host is not None:
        mikrotik_config["host"] = args.host
    if args.username is not None:
        mikrotik_config["username"] = args.username
    if args.password is not None:
        mikrotik_config["password"] = args.password
    if args.port is not None:
        mikrotik_config["port"] = args.port

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Starting MikroTik Cursor MCP server (19 categories, 382 actions, 99% coverage)")
    logger.info(f"Using host: {mikrotik_config['host']}")
    logger.info(f"Using username: {mikrotik_config['username']}")

    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        logger.info("MCP MikroTik server stopped by user")
    except Exception as e:
        logger.error(f"Error running MCP MikroTik server: {e}")
        sys.exit(1)
    finally:
        cleanup_connections()
        logger.info("Connection cleanup completed")

if __name__ == "__main__":
    main()