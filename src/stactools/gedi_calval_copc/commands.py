import logging

import click
from click import Command, Group
from stactools.gedi_calval_copc import stac

# from stactools.gedi_calval_copc.metadata import convert_to_copc

logger = logging.getLogger(__name__)


def create_gedicalvalcopc_command(cli: Group) -> Command:
    """Creates the stactools-gedi-calval-copc command line utility."""

    @cli.group(
        "gedicalvalcopc",
        short_help=("Commands for working with stactools-gedi-calval-copc"),
    )
    def gedicalvalcopc() -> None:
        pass

    @gedicalvalcopc.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("destination")
    def create_collection_command(destination: str) -> None:
        """Creates a STAC Collection

        Args:
            destination: An HREF for the Collection JSON
        """
        collection = stac.create_collection()
        collection.set_self_href(destination)
        collection.save_object()

    @gedicalvalcopc.command("create-item", short_help="Create a STAC item")
    @click.argument("source")
    @click.argument("destination")
    @click.option("-copc", "--copc", is_flag=True, help="Convert source to COPC format")
    def create_item_command(source: str, destination: str, copc: bool) -> None:
        """Creates a STAC Item

        Args:
            source: HREF of the Asset associated with the Item
            destination: An HREF for the STAC Item
            copc: Convert source to COPC format
        """
        item = stac.create_item(source, destination, copc)
        item_path = f"{destination}/{item.id}.json"
        item.set_self_href(item_path)

        item.validate()

        item.save_object(dest_href=item_path)

    return gedicalvalcopc
