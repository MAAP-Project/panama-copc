from datetime import datetime, timezone
from os import path

from pystac import Asset, Collection, Item
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.pointcloud import PointcloudExtension
from pystac.extensions.projection import ProjectionExtension
from stactools.gedi_calval_copc import constants as c
from stactools.gedi_calval_copc.metadata import (
    Metadata,
    convert_to_copc,
    fill_pointcloud_metadata,
    fill_projection_metadata,
)


def create_collection() -> Collection:
    """Creates a STAC Collection.

    See `the STAC specification
    <https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md>`_
    for information about collection fields, and
    `Collection<https://pystac.readthedocs.io/en/latest/api.html#collection>`_
    for information about the PySTAC class.

    Returns:
        Collection: STAC Collection object
    """

    collection = Collection(
        id="GEDI_CalVal_Lidar_COPC",
        title="GEDI CalVal Lidar COPC",
        description=c.DESCRIPTION,
        extent=c.EXTENT,
        stac_extensions=[
            PointcloudExtension.get_schema_uri(),
            ProjectionExtension.get_schema_uri(),
            ItemAssetsExtension.get_schema_uri(),
        ],
        keywords=c.KEYWORDS,
    )

    assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    assets.item_assets = {
        "copc.laz": AssetDefinition(
            {
                "title": "COPC LAZ file",
                "description": "Cloud Optimized Point Cloud (COPC) converted GEDI CalVal Airborne Lidar LAS data.",
                "type": "application/vnd.laszip+copc",
                "roles": ["data"],
            }
        ),
    }

    return collection


def create_item(source: str, destination: str, copc: bool = False) -> Item:
    """Creates a STAC item.

    See `the STAC specification
    <https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md>`_
    for information about an item's fields, and
    `Item<https://pystac.readthedocs.io/en/latest/api/pystac.html#pystac.Item>`_ for
    information on the PySTAC class.

    Args:
        source (str): The location to an asset associated with the item

    Returns:
        Item: STAC Item object
    """
    if copc:
        source = convert_to_copc(source, destination)

    _metadata = Metadata(source)
    item = Item(
        id=_metadata.id,
        properties={},
        geometry=_metadata.geometry,
        bbox=_metadata.bbox,
        datetime=None,
        start_datetime=datetime(2019, 9, 13, 14, 0, 0, tzinfo=timezone.utc),
        end_datetime=datetime(2019, 9, 13, 23, 59, 59, tzinfo=timezone.utc),
        stac_extensions=[],
    )

    item.add_asset(
        path.basename(source).split(".", 1)[1],
        Asset(
            title="COPC LAZ file",
            media_type="application/vnd.laszip+copc",
            description="Cloud Optimized Point Cloud (COPC) converted GEDI CalVal Airborne Lidar LAS data.",
            roles=["data"],
            href=source,
        ),
    )

    pointcloud = PointcloudExtension.ext(item, add_if_missing=True)
    fill_pointcloud_metadata(
        pointcloud, _metadata.boundary, _metadata.stats, _metadata.info, _metadata.copc
    )

    projection = ProjectionExtension.ext(item, add_if_missing=True)
    fill_projection_metadata(
        projection, _metadata.info, _metadata.boundary, _metadata.stats
    )

    return item
