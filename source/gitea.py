# encoding: utf-8
# from __future__ import unicode_literals
import sys
import argparse
from workflow import Workflow3, ICON_WEB, ICON_ERROR, ICON_WARNING, ICON_INFO, web, PasswordNotFound, util
from workflow.background import run_in_background, is_running
from workflow.util import run_command
# install into workflow folder via pip install --target=. requests
import requests
from thumbnails import Thumbs

log = None


def search_for_project(project):
    """Generate a string search key for a project"""
    elements = []
    elements.append(project['full_name'])
    elements.append(project['description'])
    return u' '.join(elements)


def main(wf):
    # build argument parser to parse script args and collect their
    # values
    parser = argparse.ArgumentParser()
    # add an optional (nargs='?') --setkey argument and save its
    # value to 'apikey' (dest). This will be called from a separate "Run Script"
    # action with the API key
    parser.add_argument('--setkey', dest='apikey', nargs='?', default=None)
    parser.add_argument('--seturl', dest='apiurl', nargs='?', default=None)
    parser.add_argument('query', nargs='?', default=None)
    # parse the script's arguments
    args = parser.parse_args(wf.args)

    ####################################################################
    # Save the provided API key or URL
    ####################################################################

    # decide what to do based on arguments
    if args.apikey:  # Script was passed an API key
        log.info("Setting API Key")
        wf.save_password('gitea_api_key', args.apikey)
        return 0  # 0 means script exited cleanly

    ####################################################################
    # Check that we have an API key saved
    ####################################################################

    try:
        wf.get_password('gitea_api_key')
    except PasswordNotFound:  # API key has not yet been set
        wf.add_item('No API key set',
                    'Please use `tea set key` to set your Gitea API key.',
                    valid=False,
                    icon=ICON_ERROR)
        wf.send_feedback()
        return 0

    ####################################################################
    # Check for the URL
    ####################################################################

    log.info(args.apiurl)
    # if user passed a new URL
    if args.apiurl:
        wf.settings['base_url'] = args.apiurl
        wf.settings['api_url'] = args.apiurl + "/api/v1/repos/search"
    # if not yet set, fall back to try.gitea.io
    elif not wf.settings.get('base_url'):
        wf.settings['base_url'] = 'https://try.gitea.io'
        wf.settings['api_url'] = 'https://try.gitea.io/api/v1/repos/search'
        return 0

    log.debug("Setting API URL to {url}".format(
        url=wf.settings.get('api_url')))

    ####################################################################
    # View/filter gitea Projects
    ####################################################################

    query = args.query

    projects_gitea = wf.cached_data('projects_gitea', None, max_age=0)

    # log.debug('XXX %s', projects_gitea)

    if wf.update_available:
        # Add a notification to top of Script Filter results
        wf.add_item('New version available',
                    'Action this item to install the update',
                    autocomplete='workflow:update',
                    icon=ICON_INFO)

    # Notify the user if the cache is being updated
    if is_running('update') and not projects_gitea:
        log.info("Updating project list via gitea..")
        wf.rerun = 0.5
        wf.add_item('Updating project list via gitea...',
                    subtitle=u'This can take some time if you have a large number of projects.',
                    valid=False,
                    icon=ICON_INFO)

    # Start update script if cached data is too old (or doesn't exist)
    if not wf.cached_data_fresh('projects_gitea', max_age=1) and not is_running('update'):
        cmd = ['/usr/bin/python3', wf.workflowfile('update.py')]
        run_in_background('update', cmd)
        # foreground for debugging
        # run_command(cmd)
        wf.rerun = 0.5

    # If script was passed a query, use it to filter projects
    if query and projects_gitea:
        projects_gitea = wf.filter(
            query, projects_gitea, key=search_for_project, min_score=20)

    if not projects_gitea:  # we have no data to show, so show a warning and stop
        wf.add_item('No projects found', icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    # log.debug('%s', projects_gitea)

    # Create thumbnails from repo avatars - slow!
    # thumbs = Thumbs(wf.datafile('thumbs'))

    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    for project in projects_gitea:
        # icon =
        wf.add_item(title=project['full_name'],
                    subtitle=project['description'],
                    arg=project['html_url'],
                    valid=True,
                    # Create thumbnails from repo avatars - slow!
                    # icon=thumbs.thumbnail(requests.get(project['owner']['avatar_url']).url),
                    icon=wf.workflowfile('gitea-transparent.png'),
                    largetext=project['full_name'],
                    quicklookurl=project['html_url'],
                    copytext=project['html_url'],
                    uid=project['id'])

    # Send the results to Alfred as XML
    wf.send_feedback()

    # Create thumbnails from repo avatars - slow!
    # thumbs.save_queue()
    # if thumbs.has_queue:
    #     thumbs.process_queue()
    #     if not is_running('generate_thumbnails'):
    #         run_in_background('generate_thumbnails',
    #                           ['/usr/bin/python3',
    #                            wf.workflowfile('thumbnails.py')])

    # return 0


if __name__ == u"__main__":
    wf = Workflow3(update_settings={
        'github_slug': 'pat-s/alfred-gitea',
    })
    log = wf.logger
    sys.exit(wf.run(main))
