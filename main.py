"""Plugin entry point for Claude Think Tool."""

import logging
import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the plugin."""
    try:
        from dify_plugin import Plugin, DifyPluginEnv

        logger.info("Initializing Claude Think Tool plugin...")

        # Create plugin configuration from environment
        config = DifyPluginEnv()
        
        # Create plugin application
        # Plugin will auto-discover providers via plugin.yaml
        app = Plugin(config)

        logger.info("Claude Think Tool plugin started successfully")
        logger.info("Waiting for tool invocations...")

        # Run application
        app.run()

    except KeyboardInterrupt:
        logger.info("Plugin stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start plugin: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

