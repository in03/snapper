# Snapper 🐟
![snapper-logo](https://github.com/in03/snapper/blob/main/assets/snapper_logo.svg)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/in03/snapper/main.svg)](https://results.pre-commit.ci/latest/github/in03/snapper/main) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Note**
> 
> Currently only Resolve 18 is supported.
> Resolve 17 and older require Python 3.6, which is now EOL. Some dependencies have started dropping support for it.
> If you use Resolve 17, checkout the 'resolve-17' branch. You can fork that branch and any incompatible dependencies if you're feeling brave.
> Although new features will not be ported, pull requests are welcome. The Resolve 17 branch has not been tested with older versions of Resolve.

## Purpose
Sometimes you want to try out some risky idea, create a couple of variations of something to compare, or even just have some timeline backups within easy reach when your project take some big steps. Snapper helps automate that. It's all too easy to throw 'best practice' out the window when you're on a tight turn-around. Snapper is really just a quick and easy utility to help you version your timelines. *Snapshots* sound **cool**, but really they're just timelines with a simple version number appended: 

**My timeline V1**, **My timeline V2**, **My timeline V3**, etc.

## Usage

Simply run `snapper new` to create a new snapshot of the active timeline.
You can run this command with a shell-script, batch-file, StreamDeck, desktop shortcut, whatever you like.  

When you create a new snapshot, Snapper duplicates your active timeline, renames it as the newest version, and puts it in a subfolder called '@Snapshots' next to your working timeline. If you keep all of your timelines in one place they'll all share the same subfolder, but if you like to keep unrelated timelines in separate folders, they'll each get their own '@Snapshots' subfolder. This helps prevent one person locking all the timelines if they park on the subfolder in collaborative mode.

If you still like seeing all your timeline versions in one place, you can enable the timelines smart bin in Resolve's settings - best of both worlds.

## What it doesn't do
Creating snapshots was always a point of friction for me and others I work with. That's why I made Snapper. That being said there are things I specifically don't want it to do. I want them to **stay** points of friction:

Deleting snapshots - That's dangerous territory, and better left as a manual process. Just keep them - unless you work with huge timelines, they don't really bloat your projects

Reverting snapshots - More often than not you'll want to do a partial revert, and there's no way of knowing how much you'd like to revert. It makes more sense to use the very granular tools Resolve provides you to pick and choose what you want to. Plus, if we're to avoid deleting all versions upstream of a revert, we leave behind a messy, jump-around history.

## Installation
First make sure you have:

- Python 3.10 - install with pyenv and pipx if you want to keep things tidy
- DaVinci Resolve Studio, with scripting set up (read Resolve's scripting README)

Then run:
```
pipx install git+https://github.com/in03/snapper
```

---

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
