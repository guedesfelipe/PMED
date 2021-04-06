import typer
import docker
from enum import Enum
from typing import Optional


class Tipos(str, Enum):
    doenca = 'doenca'
    hospital = 'hospital'


LIST_COMMAND = {
    'doenca': 'gera_doenca.py',
    'hospital': 'gera_hospital.py'
}


app = typer.Typer()
client = docker.from_env()


@app.command()
def run(tipo: Tipos, nome: str, _args: Optional[str] = typer.Argument(None)):
    typer.echo(f'📦💨 Running Container {tipo.value}...')
    try:

        _command = LIST_COMMAND[f'{tipo.value}'] + f' {nome}'
        if tipo.value == 'doenca' and _args:
            try:
                int(_args)
                _command += f' --taxa-infec-seg {_args}'
            except ValueError:
                pass

        client.containers.run(
            image=f'{tipo.value}:latest',
            command=_command,
            name=f'{nome}',
            entrypoint='python',
            network='host',
            detach=True,
            stdin_open=True,
            tty=True
        )
        _icon = typer.style('    ✓ ', fg=typer.colors.GREEN, bold=True)
        _msg = typer.style(f'Build {tipo.value} successfully', bold=True)

    except docker.errors.ContainerError as error:
        _icon = typer.style('    ✗ ', fg=typer.colors.RED)
        _msg = typer.style(f'Container error: {error}', bold=True)
    except docker.errors.ImageNotFound:
        _icon = '    🖼️ '
        _msg = typer.style('Image Not Found', fg=typer.colors.RED, bold=True)

    typer.echo(_icon + _msg)


@app.command()
def images():
    typer.echo(' ✨  Listing Images')
    for image in client.images.list():
        _tag = typer.style(image.tags[0], fg=typer.colors.YELLOW)
        typer.echo('    🖼️  ' + _tag)


@app.command()
def build(tipo: Tipos):
    typer.echo(f' 🏗️  Building {tipo.value}...')
    try:
        client.images.build(
            tag=tipo.value,
            path='./',
            dockerfile=f'./docker/{tipo.value}/Dockerfile',
            quiet=True,
            rm=True,
            forcerm=True
        )
        _icon = typer.style('    ✓ ', fg=typer.colors.GREEN, bold=True)
        _msg = typer.style(f'Build {tipo.value} successfully', bold=True)

    except docker.errors.BuildError as error:
        _icon = typer.style('    ✗ ', fg=typer.colors.RED)
        _msg = typer.style(f'Build error: {error}', bold=True)
    except TypeError:
        _icon = typer.style('    ✗ ', fg=typer.colors.RED)
        _msg = typer.style('Wrong path', bold=True)

    typer.echo(_icon + _msg)


@app.command()
def start(nome_container: str):
    _name = typer.style(nome_container, fg=typer.colors.BLUE)
    typer.echo(f' ▶️  Starting 🐳 {_name}...')
    try:
        container = client.containers.get(nome_container)
        container.start()
        _icon = typer.style('    ✓ ', fg=typer.colors.GREEN, bold=True)
        _msg = typer.style('Container started', bold=True)
    except docker.errors.NotFound:
        _icon = typer.style('    ✗ ', fg=typer.colors.RED)
        _msg = typer.style('Container not found', bold=True)

    typer.echo(_icon + _msg)


@app.command()
def stop(nome_container: str):
    _name = typer.style(nome_container, fg=typer.colors.BLUE)
    typer.echo(f' ⏹️  Stoping 🐳 {_name}...')
    try:
        container = client.containers.get(nome_container)
        container.stop()
        _icon = typer.style('    ✓ ', fg=typer.colors.GREEN, bold=True)
        _msg = typer.style('Container stopped', bold=True)
    except docker.errors.NotFound:
        _icon = typer.style('    ✗ ', fg=typer.colors.RED)
        _msg = typer.style('Container not found', bold=True)

    typer.echo(_icon + _msg)


@app.command()
def remove(nome_container: str):
    _name = typer.style(nome_container, fg=typer.colors.BLUE)
    typer.echo(f' 🗑️  Removing {_name}...')
    try:
        container = client.containers.get(nome_container)
        container.remove(force=True)
        _icon = typer.style('    ✓ ', fg=typer.colors.GREEN, bold=True)
        _msg = typer.style('Container removed', bold=True)
    except docker.errors.NotFound:
        _icon = typer.style('    ✗ ', fg=typer.colors.RED)
        _msg = typer.style('Container not found', bold=True)

    typer.echo(_icon + _msg)


@app.command()
def log(nome_container: str):
    _name = typer.style(nome_container, fg=typer.colors.BLUE)
    typer.echo(f' 📄 Log {_name}')
    try:
        container = client.containers.get(nome_container)
        for line in container.logs().decode('utf-8').splitlines():
            print(line)

        _icon = typer.style('✓ ', fg=typer.colors.GREEN, bold=True)
        _msg = typer.style('Container Log', bold=True)
        print('')
    except docker.errors.NotFound:
        _icon = typer.style('    ✗ ', fg=typer.colors.RED)
        _msg = typer.style('Container not found', bold=True)

    typer.echo(_icon + _msg)


@app.command()
def list_up():
    # Showing name etc here
    typer.echo(' ✨ Listing Containers 🆙')
    for container in client.containers.list():
        format_and_print_containers(container)


@app.command()
def list_all():
    typer.echo(' ✨ Listing All Containers')
    for container in client.containers.list(all=True):
        format_and_print_containers(container)


def format_and_print_containers(container):
    _id = typer.style(container.short_id, bold=True)
    _name = typer.style(container.name, fg=typer.colors.BLUE)
    if container.image.tags:
        _image = container.image.tags[0]
    else:
        _image = ''
    typer.echo('    🐳 ' + _id + ' ' + _name + ' ' +
               container.status + ' ' + _image)


if __name__ == '__main__':
    app()
