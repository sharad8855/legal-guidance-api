import logging

def setup_logger():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get the root logger
    logger = logging.getLogger(__name__)
    return logger

# Create logger instance
logger = setup_logger()
