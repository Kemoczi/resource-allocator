import sys
import subprocess


def before_scenario(context, scenario):
    subprocess.run(
        [sys.executable, "-m", "app.free_resources"],
        check=True
    )
