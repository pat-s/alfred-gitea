# encoding: utf-8
from workflow import Workflow, Workflow3, ICON_WEB, ICON_WARNING, ICON_INFO, web, PasswordNotFound
# from workflow import web, Workflow3, PasswordNotFound

# log = None


def get_projects(api_key, url):
    """
    Parse all pages of projects
    :return: list
    """
    return get_project_page(api_key, url, 1, [])


def get_project_page(api_key, url, page, list):
    log.info("Calling API page {page}".format(page=page))
    params = dict(token=api_key, per_page=100, page=page, membership='true')
    r = web.get(url, params)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by Gitea and extract the projects
    projects_gitea = list + r.json()

    total_count = int(r.headers.get('x-total-count'))
    pages_count = total_count // 29
    # for page in range(2, pages+1):
    #  projects_gitea = get_project_page(api_key, url, page, projects_gitea)
    #  log.info(page)

    nextpage = page + 1
    log.debug(page)
    if nextpage < pages_count:
        log.debug('nextpage', page)
        projects_gitea = get_project_page(
            api_key, url, nextpage, projects_gitea)

    return projects_gitea


def main(wf):
    try:
        # Get API key from Keychain
        api_key = wf.get_password('gitea_api_key')
        api_url = wf.settings.get('api_url')

        # Retrieve projects from cache if available and no more than 600
        # seconds old
        def wrapper():
            return get_projects(api_key, api_url)

        projects_gitea = wf.cached_data('projects_gitea', wrapper, max_age=3600)

        # Record our progress in the log file
        log.info('{} gitea repos cached'.format(len(projects_gitea)))

    except PasswordNotFound:  # API key has not yet been set
        # Nothing we can do about this, so just log it
        log.error('No API key saved')


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    wf.run(main)
