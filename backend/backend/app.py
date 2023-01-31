import subprocess

import click
import time


@click.group()
def cli():
    pass


@cli.command()
def api():
    click.echo("Launching API development server...")

    while True:
        try:
            subprocess.run(
                [
                "flask",
                "--app",
                "backend.api.app",
                "--debug",
                "run",
                ]
            )
        except Exception as e:
            print(e)
            time.sleep(10)


@cli.command()
def image_tagger():
    click.echo("Launching image tagger worker...")
    raise NotImplementedError  # FIXME


@cli.command()
def video_indexer():
    click.echo("Launching video indexer worker...")
    raise NotImplementedError  # FIXME


if __name__ == "__main__":
    cli()
