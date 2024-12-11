import boto3
from os import path

prefixes = [
    "file-staging/nasa-map/GEDI_CalVal_Lidar_Data___2/usa_neongrsm_2018_NEON_D07_GRSM_DP1_L004-1_2018060612_unclassified_point_cloud_0000001.las"
]

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


    """Writes content to an S3 object."""
    s3 = boto3.resource("s3")
    s3.Object(
        Bucket="nasa-maap-data-store", 
        Key=copc_filename,
    )
    print(f"Successfully wrote content to s3://nasa-maap-data-store/file-staging/nasa-map/GEDI_CalVal_Lidar_COPC/{copc_filename}")

count = 0
for record in prefixes:
    try:
        _path = f's3://nasa-maap-data-store/{record}'
        convert_to_copc(_path, "./")
    except Exception as e:
        print(f"Failed to create STAC for {record} because of {e}")
        continue

    print(record)
    count=count+1
    print(count)
