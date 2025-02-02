from pathlib import Path
from dagster_looker import (
    DagsterLookerApiTranslator,
    LookerApiTranslatorStructureData,
    LookerResource,
    LookerStructureType,
    load_looker_asset_specs,
    LookerFilter
)
import dagster as dg
from constants import LOOKER_CLIENT_ID, LOOKER_CLIENT_SECRET, LOOKER_BASE_URL


looker_resource = LookerResource(
    client_id=LOOKER_CLIENT_ID,
    client_secret=LOOKER_CLIENT_SECRET,
    base_url=LOOKER_BASE_URL
)



class CustomDagsterLookerApiTranslator(DagsterLookerApiTranslator):
    def get_asset_spec(
        self, looker_structure: LookerApiTranslatorStructureData
    ) -> dg.AssetSpec:
        # We create the default asset spec using super()
        default_spec = super().get_asset_spec(looker_structure)
        root_path = default_spec.key.path
        def build_custom_key(root_path):
            if root_path[0] == 'view':
                og_name = root_path[1]
                custom_key = dg.AssetKey(['mart',og_name])
            else:
                # custom_key = default_spec.key
                custom_key = default_spec.key.with_prefix('looker')
            return custom_key

        # swap the deps defo for type = explore
        def build_custom_deps(deps):
            og_deps = deps
            new_deps = []
            for dep in og_deps:
                if dep.asset_key.path[0] == 'view':
                    new_dep_key=build_custom_key(dep.asset_key.path)
                    new_deps.append(new_dep_key)
                else: 
                    og_name = dep.asset_key.path[1]
                    new_dep_key=dg.AssetKey(['looker',og_name])
                    new_deps.append(dep)
            return new_deps


                    
                    

        
        return default_spec.replace_attributes(
            key=(
                build_custom_key(root_path)
            ),
            deps=build_custom_deps(default_spec.deps),
            group_name="looker",
            description=f"""
    key: {build_custom_key(root_path)},
    deps: {build_custom_deps(default_spec.deps)}
            """
        )


looker_assets = load_looker_asset_specs(
    looker_resource=looker_resource,
    looker_filter=LookerFilter(
        dashboard_folders=[
            ["Shared", "Joon Reports"],
            ["Shared", "OKR Tracking"],
        ],
        only_fetch_explores_used_in_dashboards=True,
    ),
    dagster_looker_translator=CustomDagsterLookerApiTranslator(),
)
