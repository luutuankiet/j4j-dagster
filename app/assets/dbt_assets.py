from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator
from dagster import AssetExecutionContext, AssetKey, Config
from constants import dbt_manifest_path
from typing import Any, Mapping, Sequence
import dagster as dg
import json
# class CustomDagsterDbtTranslator(DagsterDbtTranslator):
#     def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
#         return super().get_asset_key(dbt_resource_props).with_prefix(target_schema)

class DbtAssetConfig(Config):
    cli_args: list[str] = ["run"]

@dbt_assets(manifest=dbt_manifest_path)
# @dbt_assets(manifest=dbt_manifest_path, dagster_dbt_translator=CustomDagsterDbtTranslator())
def dbt_models(context: AssetExecutionContext, dbt: DbtCliResource, config: DbtAssetConfig):
    dbt_invocation = dbt.cli(config.cli_args, context=context)
    # yield from dbt_invocation.stream()
    yield from dbt.cli(["build"], context=context).stream()


def build_dbt_sources(manifest, dagster_dbt_translator: DagsterDbtTranslator) -> Sequence[dg.AssetSpec]:
    with open(manifest) as manifest_file:
        manifest = json.load(manifest_file)
    return [
        dg.AssetSpec(
             key=dagster_dbt_translator.get_asset_key(dbt_resource_props),
             group_name="source"
        )
        for dbt_resource_props in manifest["sources"].values()
    ]

source_assets = build_dbt_sources(dbt_manifest_path, DagsterDbtTranslator())

