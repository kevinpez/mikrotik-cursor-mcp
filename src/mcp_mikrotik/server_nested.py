import sys
import logging
from mcp_mikrotik.logger import app_logger
from mcp_mikrotik.serve_nested import serve
from mcp_mikrotik.settings.configuration import mikrotik_config

def main():
    """
    Entry point for the Nested MCP MikroTik server when run as a command-line program.
    This version reduces tool count from 100+ to ~10 nested tools.
    """
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description='Nested MCP MikroTik Server (Reduced Tool Count)')
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

    logger.info("Starting Nested MCP MikroTik server (10 tools instead of 100+)")
    logger.info(f"Using host: {mikrotik_config['host']}")
    logger.info(f"Using username: {mikrotik_config['username']}")

    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        logger.info("Nested MCP MikroTik server stopped by user")
    except Exception as e:
        logger.error(f"Error running Nested MCP MikroTik server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
