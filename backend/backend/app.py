import subprocess

import click


@click.group()
def cli():
    pass


@cli.command()
def api():
    click.echo("Launching API development server...")

    while True:
        subprocess.run(
            [
                "flask",
                "--app",
                "backend.api.app",
                "--debug",
                "run",
            ]
        )


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
