from datetime import datetime, timezone
from os import path

from pystac import Asset, Collection, Item, MediaType
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.pointcloud import PointcloudExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.scientific import CollectionScientificExtension
from stactools.panama_copc import constants as c
from stactools.panama_copc.metadata import (
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
        id="ALS_Panama_COPC_Unclassified",
        title="ALS Panama COPC Unclassified",
        description=c.DESCRIPTION,
        extent=c.EXTENT,
        stac_extensions=[
            PointcloudExtension.get_schema_uri(),
            ProjectionExtension.get_schema_uri(),
            ItemAssetsExtension.get_schema_uri(),
        ],
        keywords=c.KEYWORDS,
        license="CC-BY-4.0",
        providers=c.PROVIDERS
    )

    scientific_extension = CollectionScientificExtension.ext(
        collection, add_if_missing=True
    )
    scientific_extension.citation = c.SCIENCE_CITATION
    scientific_extension.doi = c.SCIENCE_DOI

    assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    assets.item_assets = {
        "copc.laz": AssetDefinition(
            {
                "title": "COPC LAZ file",
                "description": "Cloud Optimized Point Cloud (COPC)",
                "type": "application/vnd.laszip+copc",
                "roles": ["data"],
            }
        ),
        "PO.txt": AssetDefinition(
            {
                "title": "PO file",
                "description": "PO text metadata file",
                "type": MediaType.TEXT,
                "roles": ["metadata"],
            }
        ),
        "stat.log": AssetDefinition(
            {
                "title": "stat log file",
                "description": "stat log metadata file",
                "type": MediaType.TEXT,
                "roles": ["metadata"],
            }
        ),
    }

    collection.add_links(c.ADDED_LINKS)

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
        start_datetime=datetime(2023, 5, 26, 0, 0, 0, tzinfo=timezone.utc),
        end_datetime=datetime(2023, 5, 27, 23, 59, 59, tzinfo=timezone.utc),
        stac_extensions=[],
    )

    item.add_asset(
        path.basename(source).split(".", 1)[1],
        Asset(
            title="COPC LAZ file",
            media_type="application/vnd.laszip+copc",
            description="Cloud Optimized Point Cloud (COPC)",
            roles=["data"],
            href=source,
        ),
    )
    item.add_asset(
        "PO.txt",
        Asset(
            title="PO file",
            media_type=MediaType.TEXT,
            description="",
            roles=["metadata"],
            href=f'{source.split(".", 1)[0]}_PO.txt',
        ),
    )
    item.add_asset(
        "stat.log",
        Asset(
            title="stat log file",
            media_type=MediaType.TEXT,
            description="",
            roles=["metadata"],
            href=f'{source.split(".", 1)[0]}_stat.log',
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
