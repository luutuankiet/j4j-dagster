import os 
from dotenv import load_dotenv
from pathlib import Path
from dagster_dbt import DbtCliResource




def find_project_root(current_dir, marker_file='.env'):
    while current_dir != os.path.dirname(current_dir):
        if os.path.exists(os.path.join(current_dir, marker_file)):
            return current_dir
        current_dir = Path(os.path.dirname(current_dir)).resolve(strict=True)
    raise RuntimeError("Project root with marker file '{}' not found.".format(marker_file))

# Find the project root
current_dir = Path(__file__).parent.resolve(strict=True)
project_root = find_project_root(current_dir)


# Load .env from project root
project_dotenv_path = project_root.joinpath('.env')
load_dotenv(project_dotenv_path)

DBT_REPO_NAME = os.getenv("DBT_REPO_NAME","")

DBT_PROJECT_DIR = project_root.joinpath(DBT_REPO_NAME).resolve(strict=True)
DBT_TARGET_PATH = DBT_PROJECT_DIR.joinpath("target")

dbt = DbtCliResource(project_dir=DBT_PROJECT_DIR,profiles_dir=DBT_PROJECT_DIR)

if not DBT_TARGET_PATH.exists():
    # scaffold the project target dir
    dbt.cli(["deps"], target_path=Path("target")).wait()
    dbt.cli(["compile"], target_path=Path("target")).wait()
    dbt_manifest_path = (
            dbt.cli(
                ["--quiet", "parse"],
                target_path=Path("target"),
            )
            .wait()
            .target_path.joinpath("manifest.json")
        )
else:
    dbt_manifest_path = DBT_PROJECT_DIR.joinpath("target", "manifest.json").resolve(strict=True)


LOOKER_REPO_NAME = os.getenv("LOOKER_REPO_NAME","")
LOOKER_PROJECT_DIR = project_root.joinpath(LOOKER_REPO_NAME).resolve(strict=True)
LOOKER_CLIENT_ID=os.getenv("LOOKER_CLIENT_ID","")
LOOKER_CLIENT_SECRET=os.getenv("LOOKER_CLIENT_SECRET","")
LOOKER_BASE_URL=os.getenv("LOOKER_BASE_URL","")
