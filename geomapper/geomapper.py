from .config import GeoMapperConfig
import logging
from typing import Any, Dict
import cameratransform as ct

logging.basicConfig(format='%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s')
logger = logging.getLogger(__name__)

class GeoMapper:
    def __init__(self, config: GeoMapperConfig) -> None:
        self.config = config
        logger.setLevel(self.config.log_level.value)

        self._cameras: Dict[str, ct.Camera] = []

        self._setup()

    def _setup(self):
        for cam_conf in self.config.cameras:
            camera = ct.Camera(
                ct.RectilinearProjection(
                    focallength_mm=cam_conf.focallength_mm,
                    sensor_height_mm=cam_conf.sensor_height_mm,
                    sensor_width_mm=cam_conf.sensor_width_mm,
                    image_height_px=cam_conf.image_height_px,
                    image_width_px=cam_conf.image_width_px,
                ),
                ct.SpatialOrientation(
                    elevation_m=cam_conf.elevation_m,
                    tilt_deg=cam_conf.tilt_deg,
                )
            )
            camera.setGPSpos(lat=cam_conf.pos_lat, lon=cam_conf.pos_lon)
            self._cameras[cam_conf.stream_id] = camera

    def __call__(self, input_proto) -> Any:
        return self.get(input_proto)
    
    def get(self, input_proto):
        pass