# -*- coding: utf-8 -*-

import click
import click_spinner

from .. import api
from .. import cli
from .. import options


@cli.cli.command()
@options.app
def maintenance(app):
    """
    Returns if the application is in maintenance mode.
    """
    click.echo('Fetching maintenance mode... ', nl=False)
    with click_spinner.spinner():
        enabled = api.Apps.maintenance(app=app, maintenance=None)
    if enabled:
        click.echo(click.style('ON. Application is disabled.',
                   bold=True, fg='red'))
    else:
        click.echo(click.style('off. Application is running.',
                   bold=True, fg='green'))


@cli.cli.command(aliases=['maintenance:on'])
@options.app
def maintenance_on(app):
    """
    Turns maintenance mode on.
    """
    click.echo('Enabling maintenance mode... ', nl=False)
    with click_spinner.spinner():
        app = api.Apps.maintenance(app=app, maintenance=True)
    click.echo(click.style('√', fg='green'))
    click.echo(click.style('Application is now in maintenance mode.',
                           dim=True))


@cli.cli.command(aliases=['maintenance:off'])
@options.app
def maintenance_off(app):
    """
    Turns maintenance mode off.
    """
    click.echo('Disabling maintenance mode... ', nl=False)
    with click_spinner.spinner():
        app = api.Apps.maintenance(app=app, maintenance=False)
    click.echo(click.style('√', fg='green'))
    click.echo(click.style('Application is now running.',
                           dim=True))
