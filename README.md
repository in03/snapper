# Resolve Snapshot Timeline
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/in03/resolve-snapshot-timeline/main.svg)](https://results.pre-commit.ci/latest/github/in03/resolve-snapshot-timeline/main) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
 
## What's it for? ##
Sometimes you want to try out some risky idea, create a couple of variations of a clip-sequence to compare or even just have some timeline backups within easy reach.
Resolve Snapshot Timeline does just that. It's just a quick and easy utility to create timeline versions without going for a deep dive or getting confused about the latest version.
Snapshots just sounds cool. They're just timelines with a version suffix: 

*Organisation - Project - V1, Organisation - Project - V2, Organisation* - Project - V3, etc.

## What does it need?
**This app has a few non-negotiable prerequisites:**
- Python 3.6 **ONLY** (DaVinci Resolve's Python API requires it)
- DaVinci Resolve Studio, with scripting set up (read Resolve's scripting README)

## How do I install it?

### A Warning about Python 3.6
Because DaVinci Resolve requires Python 3.6 to communicate with it's API, no versions over Python 3.6 will work with *Resolve Proxy Encoder*.
Unfortunately this means that *Resolve Proxy Encoder* may get stuck using older versions of certain packages as they begin to drop support for 3.6.
It also means that security patches for some dependencies won't make it into *Resolve Proxy Encoder* 
This kind of setup almost guarantees dependency conflicts if you have multiple Python CLI tools you keep installed.
To mitigate this you can:

- Use Python 3.6 for this application **ONLY** and install a newer Python alongside it for your other needs.

- Install a tool like *pipx* that isolates Python CLI tools with their own virtual environments but keeps the CLI entrypoints exposed. (Recommended)


### CLI / Worker
The CLI app is bundled with everything necessary to queue from Resolve and start workers that run the encoding.
```
py -3.6 -m pip install git+https://github.com/in03/resolve-snapshot-timeline
```
Or with *pipx*
``` 
pipx install git+https://github.com/in03/resolve-snapshot-timeline
```


## How can I contribute?
Clone the repo, install dependencies, call from poetry shell:
```
git clone https://github.com/in03/resolve-snapshot-timeline
cd resolve-snapshot-timeline
py -3.6 -m pip install poetry
py -3.6 -m poetry shell
poetry install
rsnaptime
```
If you're unfamiliar with using Poetry for dependency management and packaging, [give it a look](https://python-poetry.org/docs/basic-usage).

## How do I use it?

```
RESOLVE SNAPSHOT TIMELINE 📷

Usage: rsnaptime new [OPTIONS]

  Create a new timeline snapshot

Options:
  --dry-run / --no-dry-run  Don't duplicate the timeline, just return the next
                            version name  [default: no-dry-run]
  --help                    Show this message and exit.
PS C:\Users\Caleb\Documents\Programming\local\resolve-snapshot-timeline> 
```
