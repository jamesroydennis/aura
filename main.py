# C:\Users\jarde\Projects\aura\main.py

import sys
import os
from pathlib import Path

# --- Dynamic Path Setup (CRITICAL for Monorepo Imports) ---
# Add the main 'aura' project root to Python's path if it's not already there.
# This allows all sub-projects (aura-data, aura-presentation) to be imported
# as top-level packages (e.g., 'from aura_data.task import Task').
aura_root = Path(__file__).resolve().parent
if str(aura_root) not in sys.path:
    sys.path.append(str(aura_root))

# --- Centralized Core Imports ---
# These modules are now directly under the /aura root
from config.loguru_setup import setup_logging
from config.config import DEBUG_MODE
from core.dependency_container import DependencyContainer

# --- Project-Specific Service Imports (from sub-projects) ---
# These imports will treat aura-data and aura-presentation as top-level packages.
# Ensure that all __init__.py files are in place to make them packages.
# For now, we'll only import what's needed for initialization and basic testing.
from aura_data.interfaces.ICrudRepository import ICrudRepository
from aura_data.task import Task
from aura_data.task_manager_service import TaskManagerService
from aura_data.data.csv_task_repository import CsvTaskRepository

# from aura_presentation.backend.ai_generator import AIGenerator # Will add later when ready for Flask


# --- Global Setup ---
setup_logging() # Initialize Loguru
from loguru import logger # Import the logger after setup

logger.info(f"INFO - Aura Monorepo Main Initialized.")
logger.info(f"INFO - Python interpreter: {sys.executable}")
logger.info(f"INFO - Current working directory: {os.getcwd()}")
logger.info(f"INFO - Aura project root added to PATH: {aura_root}")
logger.info(f"INFO - Running in DEBUG_MODE: {DEBUG_MODE}")


def configure_aura_data_dependencies(container: DependencyContainer):
    """
    Configures dependencies specific to the aura-data project.
    """
    logger.info("INFO - Registering Aura-Data dependencies.")
    # Registering the concrete CsvTaskRepository as the implementation for ICrudRepository[Task]
    # Note: Pass the class directly, not a string, as it's now importable.
    container.register(ICrudRepository[Task], CsvTaskRepository)
    
    # Register the TaskManagerService, injecting its dependencies
    container.register(TaskManagerService, lambda: TaskManagerService(
        task_repository=container.resolve(ICrudRepository[Task])
    ))
    logger.success("SUCCESS - Aura-Data dependencies configured.")

def configure_aura_presentation_dependencies(container: DependencyContainer):
    """
    Configures dependencies specific to the aura-presentation project.
    Will include AI-related services.
    """
    logger.info("INFO - Registering Aura-Presentation dependencies.")
    # Assuming AIGenerator will be in aura-presentation/backend/ai_generator.py
    # from aura_presentation.backend.ai_generator import AIGenerator
    # container.register(AIGenerator, lambda: AIGenerator(api_key=os.getenv("GOOGLE_API_KEY")))
    logger.success("SUCCESS - Aura-Presentation dependencies configured (conceptual).")

# ... Add functions to configure aura-business dependencies later ...


if __name__ == '__main__':
    global_container = DependencyContainer() # Instantiate the global DI container

    # Configure dependencies for each sub-project
    configure_aura_data_dependencies(global_container)
    configure_aura_presentation_dependencies(global_container) # Even if just conceptual now

    logger.info("INFO - All core services and sub-project dependencies configured.")

    # --- Example of resolving and using a service from aura-data ---
    try:
        task_manager = global_container.resolve(TaskManagerService)
        all_tasks = task_manager.get_all_tasks()
        logger.info(f"INFO - Retrieved {len(all_tasks)} tasks via Aura-Data's TaskManagerService.")
        for task in all_tasks[:2]:
            logger.info(f"Example Task: Title='{task.title}', Status='{task.status}'")
    except Exception as e:
        logger.error(f"ERROR - Failed to resolve or use TaskManagerService: {e}", exc_info=True)

    logger.info("INFO - Aura Monorepo Main execution complete. All systems online (conceptually).")