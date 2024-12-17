from pystac import (
    Extent, 
    SpatialExtent, 
    TemporalExtent, 
    Provider, 
    ProviderRole,
    Link
)
from pystac.extensions.scientific import (
    ScientificRelType,
)
from pystac.utils import str_to_datetime

SCIENCE_CITATION = (
    "ForestGEO Smithsonian. (2024). 2023 high-resolution airborne LiDAR data for"
    " Barro Colorado Island and other Smithsonian ForestGEO Sites in Central Panama."
    " Smithsonian Research Data Repository."
)
SCIENCE_DOI = "10.60635/C34W2W"

PROVIDERS = [
    Provider(
        name="ForestGEO Smithsonian",
        roles=[
            ProviderRole.PRODUCER,
            ProviderRole.LICENSOR,
        ],
        url="https://forestgeo.si.edu/",
    ),
    Provider(
        name="Smithsonian Research Data Repository",
        roles=[
            ProviderRole.HOST
        ],
        url="https://smithsonian.dataone.org/",
    ),
]
ADDED_LINKS = [
    Link(
        rel="license",
        target="https://creativecommons.org/licenses/by/4.0/",
        title="CC-BY-4.0"
    ),
    Link(
        rel=ScientificRelType.CITE_AS,
        target="https://doi.org/10.60635/C34W2W",
        title="DOI"
    ),
]
TEMPORAL_EXTENT = TemporalExtent([[
    str_to_datetime("2023-05-26T00:00:00.000Z"), 
    str_to_datetime("2023-05-27T23:59:59.000Z")
]])
SPATIAL_EXTENT = SpatialExtent(
    [
        [-79.87191537940562, 9.132262269654667, -79.81748861392951, 9.179793057228403],
        [-79.781912, 9.33379, -79.778995, 9.336684],
        [-79.77962801639599, 9.186050571859713, -79.71514599035866, 9.238603428459562],
        [-79.83060200642741, 9.178801568981758, -79.82768599353687, 9.18126043100854],
        [-79.75432699728182, 9.153464571219999, -79.74086800058708, 9.163959426949997],
        [-79.64024496988135, 9.0610425752265, -79.6373300299675, 9.06393941894969],
        [-79.66440097657673, 9.083051574189328, -79.6614860235188, 9.085948425829514],
        [-79.60330493865827, 8.941723582093845, -79.6003910612002, 8.9446204239737],
        [-79.8592858642689, 9.09852096467, -79.84903413582397, 9.12116349731504],
        [-79.98132691460196, 9.27855562355809, -79.97092687796511, 9.286259571570373]
    ]
)
EXTENT = Extent(SPATIAL_EXTENT, TEMPORAL_EXTENT)
KEYWORDS = [
    "ALS",
    "COPC",
    "Point Cloud",
    "Unclassified",
    "Airborne lidar scanning",
    "Tropical forest",
    "Remote sensing",
    "Panama",
    "Photogrammetry",
    "Aboveground biomass (AGB)",
    "Forest structure",
    "Smithsonian ForestGEO",
    "Barro Colorado Island",
    "Agua Salud"
]
DESCRIPTION = (
    "The work, funded by Smithsonian ForestGEO and NASA JPL, consists of the LiDAR survey of an"
    " area of 3825.24 hectares in several areas about of the Panama Canal from the south to the"
    " Atlantic coast. This survey aims to obtain digital models for the definition of reality"
    " terrain and surface and the very dense mapping of vegetation. On LiDAR technology, a"
    " Fullwave Form sensor."
)
