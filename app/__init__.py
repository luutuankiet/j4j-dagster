# need this line to make the imports work
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import dagster as dg
from constants import dbt
import assets.dbt_assets as dbt_assets
from assets.dbt_assets import dbt_models, source_assets
from assets.looker_assets import looker_assets, looker_resource


all_assets = [dbt_models,*looker_assets]
all_assets.extend(source_assets)
# dbt_job = dg.define_asset_job("all_assets")
dbt_job = dg.define_asset_job(name="dbt_build",selection=[dbt_models])

all_resources = {
    "dbt": dbt,
    "looker": looker_resource
}

all_jobs = [dbt_job]


defs = dg.Definitions(
    assets=all_assets,
    jobs=all_jobs,
    resources=all_resources,
)
