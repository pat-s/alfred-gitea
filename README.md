# alfred-gitea

## Installation

1. Download the [alfredworkflow]()

## Usage

1. Set your Gitea URL via `tea set url <url>`
1. Set your Gitea Access Token via `tea set token <token>`.
   The workflow also works without access token but will be restricted to public repos.

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
If you want to reset the learned behavior, you can call `tea reset`.
Note however that this will delete everything including the URL and access token.

**Quick Open**

If you hold the &#x2325; (`option`) key and then hit &#x23ce; (`return`), the subfolder selection will be skipped and the repository will be opened directly.

<p style="text-align:center">
<img alt="alfred-gitea-gif" src="https://media.giphy.com/media/GlHoA8FEovaNgkUlrj/giphy.gif"/>
</p>

## Acknowledgment

- Inspired by [alfred-gitlab](https://github.com/lukewaite/alfred-gitlab)
- Powered by [Alfred-Workflow](https://www.deanishe.net/alfred-workflow/index.html) python module

## Misc

- [How to add dynamic repo thumbnails in alfred-workflow](https://github.com/deanishe/alfred-workflow/issues/106#issuecomment-737505965)
- Dev info: The Gitea API does not return `x-next-page` and `x-page` headers, therefore the total number of pages needs to be calculated on the fly in every run
