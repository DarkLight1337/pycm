from __future__ import annotations

import click

from .pycm import pycm

__all__ = ['cli']

@click.command()
@click.argument('package_name', type=str)
@click.option('--python', 'python_versions', metavar='<VERSIONS>', type=str, required=True, help='A comma-separated list of Python versions to check against')
def cli(package_name: str, python_versions: str) -> None:
    """Show the versions of a PyPI package that are compatible with each Python version."""
    output_df = pycm(package_name, python_versions.split(','))
    click.echo(output_df)
