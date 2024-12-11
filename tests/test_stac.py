from stactools.gedi_calval_copc import constants as c
from stactools.gedi_calval_copc import stac

from . import test_data


def test_create_collection() -> None:
    # This function should be updated to exercise the attributes of interest on
    # the collection

    collection = stac.create_collection()
    collection.set_self_href(None)  # required for validation to pass
    assert collection.id == "GEDI_CalVal_Lidar_COPC"
    assert collection.title == "GEDI CalVal Lidar COPC"
    assert collection.extent == c.EXTENT
    collection.validate()


def test_create_item() -> None:
    # This function should be updated to exercise the attributes of interest on
    # a typical item

    item = stac.create_item(
        test_data.get_path(
            "data/usa_neonsrer_2019_NEON_D14_SRER_DP1_L090-1_2019091314_unclassified_point_cloud_0000003.copc.laz"
        ),
        "examples/usa_neonsrer_2019_NEON_D14_SRER_DP1_L090-1_2019091314_unclassified_point_cloud_0000003.json",
    )
    assert (
        item.id
        == "usa_neonsrer_2019_NEON_D14_SRER_DP1_L090-1_2019091314_unclassified_point_cloud_0000003"
    )
    assert item.properties["start_datetime"] == "2019-09-13T14:00:00Z"
    assert item.properties["end_datetime"] == "2019-09-13T23:59:59Z"

    # assert that item has an asset called copc.laz
    assert "copc.laz" in item.assets

    item.validate()
