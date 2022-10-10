# Snapper 🐟
![snapper-logo](https://github.com/in03/snapper/blob/main/assets/snapper_logo.svg)
 
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/in03/snapper/main.svg)](https://results.pre-commit.ci/latest/github/in03/snapper/main) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Warning**
>
> This version only supports Resolve 18.
> Checkout the 'resolve-17' branch. Development on that branch has stopped, but pull requests are welcome.
> Versions below 17 have not been tested but should theoretically work.

## What's it for? ##
Sometimes you want to try out some risky idea, create a couple of variations of a clip-sequence to compare or even just have some timeline backups within easy reach.
Resolve Snapshot Timeline does just that. It's just a quick and easy utility to create timeline versions without going for a deep dive or getting confused about the latest version.
Snapshots just sounds cool. They're just timelines with a version suffix: 

*Organisation - Project - V1, Organisation - Project - V2, Organisation* - Project - V3, etc.

## What does it need?
**This app has a few non-negotiable prerequisites:**
- Python 3.10 - install with pyenv, pipx if you want to keep things tidy
- DaVinci Resolve Studio, with scripting set up (read Resolve's scripting README)

## How do I install it?
pipx install git+https://github.com/in03/snapper

## How do I use it?

![Usage demo GIF](https://github.com/in03/snapper/blob/main/assets/usage_demo.gif)

```
 ___ ___ ___ ___ ___ ___ ___
|_ -|   | .'| . | . | -_|  _|
|___|_|_|__,|  _|  _|___|_|
            |_| |_|

Create and manage DaVinci Resolve timeline revisions 🐟

Usage: snapper [OPTIONS] COMMAND [ARGS]...

  Do yourself a favour and create frequent timeline snapshots. Don't leave
  messy little experiments at the end of your timelines. Keep it tidy. Keep it
  clean.

  Just type: "snapper new"

Options:
  --verbose / --no-verbose        Log debug messages  [default: no-verbose]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  new  Create a new timeline snapshot
```



## How can I contribute?
Clone the repo, install dependencies, call from poetry shell:
```
git clone https://github.com/in03/snapper
cd snapper
python3 -m pip install poetry
python3 -m poetry shell
poetry install
snapper --help
```
If you're unfamiliar with using Poetry for dependency management and packaging, [give it a look](https://python-poetry.org/docs/basic-usage).
