# alfred-gitea

- [alfred-gitea](#alfred-gitea)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Quick Open](#quick-open)
    - [Starting fresh](#starting-fresh)
  - [Acknowledgment](#acknowledgment)
  - [Misc](#misc)

## Installation

- Download the [alfredworkflow](https://github.com/pat-s/alfred-gitea/releases/download/v1.0.0/Gitea.alfredworkflow) from GitHub
- Install from [packal](http://www.packal.org/workflow/gitea)

1. Set your Gitea Access Token via `tea set token <token>` or `tea set key <token>` (both do the same)
2. Set your Gitea URL via `tea set url <url>`.
   The workflow also works without access token but will be restricted to public repos.

The workflow makes calls to the `/users/repos` endpoint and will only list repos which are accessible via the given access token.

**Python3 and macOS > 12.3**

macOS 12.3 does not ship with a Python2 interpreter anymore, hence `alfred-gitea` versions < 2.0.0 will not work.
Please update to `alfred-gitea` >= 2.0.0.

## Usage

`tea <query>` shows all repos using the repos slug `owner/repo`
The next menu let's you make a selection which subpart of the repo to open:

- Code (repo home)
- Issues
- Pull Requests
- Releases
- Wiki
- Projects
- Settings

The workflow learns from usage and will sort the returned results by this criteria.

### Quick Open

If you hold the &#x2325; (`option`) key and then hit &#x23ce; (`return`), the subfolder selection will be skipped and the repository will be opened directly.
This behavior can also be set as the default by setting variable `quick_open` to `true` in the Alfred workflow options.
Note however that this will not allow selecting a specific location (repo, settings, etc.) anymore.

<p style="text-align:center">
<img alt="alfred-gitea-gif" src="https://media.giphy.com/media/GlHoA8FEovaNgkUlrj/giphy.gif"/>
</p>

### Starting fresh

If you want to reset the learned behavior or switch to a new Gitea instance, call `tea reset`.
This will delete the cache, access token and the URL.

If you **only** want to delete the repo cache, call `tea clearcache`.
This will keep the URL and API key set and only invalidate the repo cache.

## Acknowledgment

- Inspired by [alfred-gitlab](https://github.com/lukewaite/alfred-gitlab)
- Python2 version was initially powered by the [Alfred-Workflow](https://www.deanishe.net/alfred-workflow/index.html) python module
- Python3 conversion was adapted from [TribuneX/alfred-gitlab](https://github.com/TribuneX/alfred-gitlab)
- Webscraping functionality comes from [slingamn/mureq](https://github.com/slingamn/mureq)

## Misc

- [How to add dynamic repo thumbnails in alfred-workflow](https://github.com/deanishe/alfred-workflow/issues/106#issuecomment-737505965)
- Dev info: The Gitea API does not return `x-next-page` and `x-page` headers, therefore the total number of pages needs to be calculated on the fly in every run

**What about repo avatars?**

There is in fact a working solution for repo avatars.
However it requires the download of all avatars on each run and a subsequent thumbnail conversion.
This adds a delay of at least two seconds until the first match appears in Alfred.
Hence I decided to use fixed repo icons.
