# stactools-panama-copc

- Name: panama-copc
- Package: `stactools.panama_copc`
- [stactools-panama-copc on PyPI](https://pypi.org/project/stactools-panama-copc/)
- Owner: @jjfrench @omshinde
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
  - [pointcloud](htts://github.com/stac-extensions/pointcloud/)

## STAC examples

- [Collection](examples/collection.json)
- [Item](examples/230526_200655/230526_200655.json)

## Installation

```shell
pip install stactools-panama-copc
```

## Command-line usage

Description of the command line functions

For generating STAC items from COPC files, use the following command:

```shell
stac panamacopc create-item <source> <destination>
stac panamacopc create-item tests/data/230526_200655.copc.laz examples
```

For converting LAS files to COPC.LAZ, use the '--copc' flag
to first generate the COPC file and then generate the STAC item
using the COPC.LAZ destination location:

```shell
stac panamacopc create-item <source> <destination> --copc
stac panamacopc create-item tests/data/230526_200655.laz examples -copc
```

Use `stac panama-copc --help` to see all subcommands and options.

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
