import click

from .docker import discover_containers, exec_in_container
from .utils import build_file_path


@click.command()
@click.argument("path")
def cli(path):
    found = discover_containers()
    if not found:
        click.echo("No container found")
        return
    click.echo("Found {} containers to backup".format(len(found)))

    for j in found:
        click.echo("  Running backup for {}... ".format(j.name), nl=False)
        try:
            run_job(j, path)
            click.echo("OK")
        except Exception as e:
            click.echo("FAIL")
            click.echo(str(e))


def run_job(job, root_path):
    out_path = build_file_path(job.filename, root_path)

    if job.pre:
        exec_in_container(job.cid, job.pre)

    exec_in_container(job.cid, job.bkp, out_path)

    if job.post:
        exec_in_container(job.cid, job.post)


if __name__ == "__main__":
    cli()
