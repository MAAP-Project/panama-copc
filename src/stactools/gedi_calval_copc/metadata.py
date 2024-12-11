import json
from os import path
from typing import Any, Dict, List, TypeVar

from pystac import Asset, Item
from pystac.extensions.pointcloud import (
    PhenomenologyType,
    PointcloudExtension,
    Schema,
    Statistic,
)
from pystac.extensions.projection import ProjectionExtension

T = TypeVar("T", Item, Asset)


def convert_to_copc(las_filename: str, output_location: str) -> str:
    """Converts a LAS file to COPC format."""
    import os

    import pdal

    base_name, _ = os.path.splitext(path.basename(las_filename))
    copc_filename = f"{base_name}.copc.laz"

    r = pdal.Reader.las(filename=las_filename)
    w = pdal.Writer.copc(filename=f"{output_location}/{copc_filename}")
    pipeline: pdal.Pipeline = r | w
    pipeline.execute()

    return f"{output_location}/{copc_filename}"


class Metadata:
    def __init__(self, href: str) -> None:
        self.href = href
        self.id = self.splitext_recursive(path.basename(href))
        self.get_metadata(href)

    def splitext_recursive(self, filename: str) -> str:
        """Recursively splits the extension from a filename."""
        import os

        base, ext = os.path.splitext(filename)
        if ext != "":
            return self.splitext_recursive(base)
        return base

    def get_metadata(self, filename: str) -> None:
        import pdal

        # pdal info --all call references hexbin, stats, and info filters
        r = pdal.Reader.copc(filename)
        hb = pdal.Filter.hexbin()
        s = pdal.Filter.stats()
        i = pdal.Filter.info()

        pipeline: pdal.Pipeline = r | hb | s | i

        pipeline.execute()
        self.boundary = pipeline.metadata["metadata"][hb.type]
        self.stats = pipeline.metadata["metadata"][s.type]
        self.info = pipeline.metadata["metadata"][i.type]
        self.copc = pipeline.metadata["metadata"][r.type]

        def convertBBox(obj: Dict[str, Any]) -> List[float]:
            output = []
            output.append(float(obj["minx"]))
            output.append(float(obj["miny"]))
            output.append(float(obj["minz"]))
            output.append(float(obj["maxx"]))
            output.append(float(obj["maxy"]))
            output.append(float(obj["maxz"]))
            return output

        def convertGeometry(geom: Dict[str, Any], srs: str) -> Any:
            from osgeo import ogr, osr

            in_ref = osr.SpatialReference()
            in_ref.SetFromUserInput(srs)
            out_ref = osr.SpatialReference()
            out_ref.SetFromUserInput("EPSG:4326")

            g = ogr.CreateGeometryFromJson(json.dumps(geom))
            g.AssignSpatialReference(in_ref)
            g.TransformTo(out_ref)
            return json.loads(g.ExportToJson())

        try:
            self.geometry = convertGeometry(
                self.boundary["boundary_json"], self.copc["comp_spatialreference"]
            )
        except KeyError:
            self.geometry = self.stats["bbox"]["EPSG:4326"]["boundary"]

        self.bbox = convertBBox(self.stats["bbox"]["EPSG:4326"]["bbox"])


def fill_pointcloud_metadata(
    pc_ext: PointcloudExtension[T],
    boundary: Dict[str, Any],
    stats: Dict[str, Any],
    info: Dict[str, Any],
    copc: Dict[str, Any],
) -> None:
    """Fills the metadata of a point cloud item."""
    try:
        pc_ext.density = boundary["avg_pt_per_sq_unit"]
    except KeyError:
        pc_ext.density = 0

    try:
        schema_list = []
        for d in info["schema"]["dimensions"]:
            schema = Schema.create(name=d["name"], size=d["size"], type=d["type"])
            schema_list.append(schema)
    except KeyError:
        schema_list = []
    pc_ext.schemas = schema_list

    try:
        stats_list = []
        for s in stats["statistic"]:
            stat = Statistic.create(
                name=s["name"],
                position=s.get("position"),
                average=s.get("average"),
                count=s.get("count"),
                maximum=s.get("maximum"),
                minimum=s.get("minimum"),
                stddev=s.get("stddev"),
                variance=s.get("variance"),
            )
            stats_list.append(stat)
    except KeyError:
        stats_list = []
    pc_ext.statistics = stats_list
    pc_ext.encoding = "LASzip"

    pc_ext.count = copc["count"]
    pc_ext.type = PhenomenologyType.LIDAR


def fill_projection_metadata(
    proj_ext: ProjectionExtension[T],
    info: Dict[str, Any],
    boundary: Dict[str, Any],
    stats: Dict[str, Any],
) -> None:
    from pyproj import CRS

    proj_ext.projjson = info["srs"]["json"]

    try:
        obj = stats["bbox"]["native"]["bbox"]
        proj_ext.bbox = [
            float(obj["minx"]),
            float(obj["miny"]),
            float(obj["minz"]),
            float(obj["maxx"]),
            float(obj["maxy"]),
            float(obj["maxz"]),
        ]
    except KeyError:
        proj_ext.bbox = None

    proj_ext.geometry = boundary["boundary_json"]

    p = CRS.from_string(info["srs"]["horizontal"])
    item_proj_ext = p.to_wkt("WKT2_2019")
    proj_ext.wkt2 = item_proj_ext
