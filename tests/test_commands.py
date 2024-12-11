from pathlib import Path

from click import Group
from click.testing import CliRunner
from pystac import Collection, Item
from stactools.panama_copc.commands import create_panamacopc_command

from . import test_data

command = create_panamacopc_command(Group())


def test_create_collection(tmp_path: Path) -> None:
    # Smoke test for the command line create-collection command
    #
    # Most checks should be done in test_stac.py::test_create_collection

    path = str(tmp_path / "collection.json")
    runner = CliRunner()
    result = runner.invoke(command, ["create-collection", path])
    assert result.exit_code == 0, f"\n{result.output}"
    collection = Collection.from_file(path)
    collection.validate()


def test_create_item(tmp_path: Path) -> None:
    # Smoke test for the command line create-item command
    #
    # Most checks should be done in test_stac.py::test_create_item
    stac_id = "usa_neonsrer_2019_NEON_D14_SRER_DP1_L090-1_2019091314_unclassified_point_cloud_0000003"
    asset_href = test_data.get_path(f"data/{stac_id}.copc.laz")
    path = str(tmp_path / "examples")
    runner = CliRunner()
    result = runner.invoke(command, ["create-item", asset_href, path])
    assert result.exit_code == 0, f"\n{result.output}"
    item = Item.from_file(f"{path}/{stac_id}.json")
    item.validate()
