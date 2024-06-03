# SAE geo-mapper

A SAE stage that maps object locations from camera / pixel space to geo-coordinate space. For that it needs to be configured with a number of optical and geometrical camera parameters.

## Input/Output
- **Input** message must be a `SaeMessage`. The geo-mapping is done on each `Detection` message within. If there are no `Detection` messages, the processing is effectively a no-op.
- **Output** is the input `SaeMessage` with geo-coordinates added to every `Detection`. All other fields are preserved.