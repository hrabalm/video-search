import subprocess
import time

import click


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


if __name__ == "__main__":
    cli()
