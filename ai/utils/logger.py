import logging
import sys
from pathlib import Path

def setup_logger(name: str = "ai_engine", log_file: str = "ai_training.log", level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a centralized logger for AI training and evaluation.
    Logs are written to both standard output and a file.
    """
    logger = logging.getLogger(name)
    
    # If already configured, avoid adding multiple handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    # Define formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    try:
        # Determine logs directory based on root path
        root_path = Path(__file__).resolve().parent.parent.parent
        logs_dir = root_path / "logs"
        logs_dir.mkdir(exist_ok=True, parents=True)
        
        log_path = logs_dir / log_file
        file_handler = logging.FileHandler(log_path, mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to set up file logger: {e}")

    return logger

# Global default logger instance for easy import
ai_logger = setup_logger()
