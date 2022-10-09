# coding: utf-8
import io
import sys
import zipfile
import subprocess
from pathlib import Path

import typer
import requests


def main(
    script: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="The script which should resolve the problem",
    ),
    url: str = typer.Argument(..., help="The url of the problem"),
):
    r = requests.get(f"{url}/file/statement/samples.zip")
    r.raise_for_status()
    failed = False

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for file in z.filelist:
            file_path = Path(file.filename)
            if file_path.suffix == ".in":
                test_input = z.read(file).decode("utf-8")
                test_answer = z.read(f"{file_path.stem}.ans").decode("utf-8")
                p = subprocess.run(
                    [sys.executable, str(script)],
                    input=test_input,
                    encoding="utf-8",
                    capture_output=True,
                )

                if p.returncode != 0:
                    failed = True
                    typer.secho(f"Error on sample {file_path.stem} :\n{p.stderr}", fg="red", err=True)
                    continue

                if p.stdout != test_answer:
                    failed = True
                    typer.secho(f"Wrong answer for sample {file_path.stem} !", fg="red")

                    if len(p.stdout) != len(test_answer):
                        typer.secho(
                            f"Length does not match ! Got {len(p.stdout)} characters, excepted {len(test_answer)}",
                            fg="red",
                        )
                    else:
                        char = []
                        for a, b in zip(p.stdout, test_answer):
                            if a == b:
                                char.append(a)
                            else:
                                char.append(typer.style(a, fg="red"))
                        typer.echo("Excepted :")
                        typer.echo(test_answer)
                        typer.echo("Got :")
                        typer.echo("".join(char))

    if failed is False:
        typer.secho("Good answer !", fg="green")


if __name__ == "__main__":
    typer.run(main)
