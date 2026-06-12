import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from controllers.app_controller import AppController

if __name__ == "__main__":
    controller = AppController()
    controller.run()