# SAE GEO Mapper

A SAE stage that maps object locations from camera / pixel space to geo-coordinate space. For that it needs to be configured with a number of optical and geometrical camera parameters.\

Geo Mapper can be run in two fundamental modes: static and dynamic. Static means, that for every videosource (camera) next to necessary mapping data position data is configured in [settings.yaml](settings.template.yaml). In dynamic mode Geo Mapper will take camera position from video frames which are inserted by [video source component](https://github.com/starwit/video-source-py).

## Quick Setup
Due to `cameratransform` being stuck on Python 3.11 (due to Pandas 1.x), we need to use pyenv for this repository.
- Make sure `pyenv` is installed
- Install the latest Python 3.11 (e.g. Python 3.11.9 at the time of writing): `pyenv install 3.11.9`
  - If you encounter installation error, check that you have all Python build dependencies installed (refer to pyenv README)
- Set the installed Python version for this directory, e.g. `pyenv local 3.11.9`
- Run `poetry install`, it should automatically pick up the correct Python version and use it for the virtualenv

## How to Build

See [dev readme](doc/DEV_README.md) for build & package instructions.

## Input/Output
- **Input** message must be a `SaeMessage`. The geo-mapping is done on each `Detection` message within. If there are no `Detection` messages, the processing is effectively a no-op.
- **Output** is the input `SaeMessage` with geo-coordinates added to every `Detection`. All other fields are preserved.

# Changelog
## 0.7.0
- Upgrade `vision-api` to `3.1.0`
- Add `SaeMessage.frame.camera_location` if `pos_lat` and `pos_lon` is set (independent of `passthrough` mode)