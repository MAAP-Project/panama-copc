# stactools-gedi-calval-copc

- Name: gedi-calval-copc
- Package: `stactools.gedi_calval_copc`
- [stactools-gedi-calval-copc on PyPI](https://pypi.org/project/stactools-gedi-calval-copc/)
- Owner: @jjfrench @omshinde
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
  - [pointcloud](htts://github.com/stac-extensions/pointcloud/)

## STAC examples

- [Collection](examples/collection.json)
- [Item](examples/usa_neonsrer_2019_NEON_D14_SRER_DP1_L090-1_2019091314_unclassified_point_cloud_0000003/usa_neonsrer_2019_NEON_D14_SRER_DP1_L090-1_2019091314_unclassified_point_cloud_0000003.json)

## Installation

```shell
pip install stactools-gedi-calval-copc
```

## Command-line usage

Description of the command line functions

For generating STAC items from COPC files, use the following command:

```shell
stac gedicalvalcopc create-item <source> <destination>
stac gedicalvalcopc create-item tests/data/usa_neonsrer_2019_NEON_D14_SRER_DP1_L090-1_2019091314_unclassified_point_cloud_0000003.copc.laz examples
```

For converting LAS files to COPC.LAZ, use the '--copc' flag
to first generate the COPC file and then generate the STAC item
using the COPC.LAZ destination location:

```shell
stac gedicalvalcopc create-item <source> <destination> --copc
stac gedicalvalcopc create-item tests/data/usa_neonsrer_2019_NEON_D14_SRER_DP1_L090-1_2019091314_unclassified_point_cloud_0000003.las examples -copc
```

Use `stac gedi-calval-copc --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
pip install -e '.[dev]'
pre-commit install
```

To check all files:

```shell
pre-commit run --all-files
```

To run the tests:

```shell
pytest -vv
```

If you've updated the STAC metadata output, update the examples:

```shell
scripts/update-examples
```
