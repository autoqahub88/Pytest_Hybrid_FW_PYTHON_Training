import logging
from pathlib import Path

def setup_logger(name):
    """
    ***************************************************************************************
    Author: Nagaraju
    Creation Date : Sep 2025
    Purspose : this function helps to create the log file wrt each module
    *****************************************************************************************
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels

    log_dir = Path(__file__).resolve().parents[1] / "test-results/logs"
    log_dir.mkdir(parents=True,exist_ok=True)

    log_file = log_dir / f"{name}.log"  # Fixed file per module
    # Avoid adding handlers multiple times
    if not logger.handlers:
        # File handler (append mode)

        file_handler = logging.FileHandler(log_file, mode='a', encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

