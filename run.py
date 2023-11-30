from pathlib import Path
import os
import subprocess

cwd = Path.cwd()
project_name = cwd.name

parent_dir = cwd.parent

os.environ["FLASK_APP"] = project_name
os.environ["FLASK_DEBUG"] = "1"

subprocess.run(["flask", "run"], cwd=parent_dir)
