import logging
from typing import Any, Dict, NamedTuple

import cameratransform as ct
from prometheus_client import Counter, Histogram, Summary
from visionapi.messages_pb2 import BoundingBox, SaeMessage

from .config import GeoMapperConfig

logging.basicConfig(format='%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s')
logger = logging.getLogger(__name__)

GET_DURATION = Histogram('geo_mapper_get_duration', 'The time it takes to deserialize the proto until returning the tranformed result as a serialized proto',
                         buckets=(0.0025, 0.005, 0.0075, 0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25))
TRANSFORM_DURATION = Summary('geo_mapper_transform_duration', 'How long the coordinate transformation takes')
OBJECT_COUNTER = Counter('geo_mapper_object_counter', 'How many detections have been transformed')
PROTO_SERIALIZATION_DURATION = Summary('geo_mapper_proto_serialization_duration', 'The time it takes to create a serialized output proto')
PROTO_DESERIALIZATION_DURATION = Summary('geo_mapper_proto_deserialization_duration', 'The time it takes to deserialize an input proto')

class Point(NamedTuple):
    x: float
    y: float


class GeoMapper:
    def __init__(self, config: GeoMapperConfig) -> None:
        self.config = config
        logger.setLevel(self.config.log_level.value)

        self._cameras: Dict[str, ct.Camera] = dict()

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
                    heading_deg=cam_conf.heading_deg,
                )
            )
            camera.setGPSpos(lat=cam_conf.pos_lat, lon=cam_conf.pos_lon)
            self._cameras[cam_conf.stream_id] = camera

    def __call__(self, input_proto) -> Any:
        return self.get(input_proto)
    
    @GET_DURATION.time()
    def get(self, input_proto):
        sae_msg = self._unpack_proto(input_proto)

        camera = self._cameras.get(sae_msg.frame.source_id)

        if camera is None:
            return sae_msg

        with TRANSFORM_DURATION.time():
            for detection in sae_msg.detections:
                center = self._get_center(detection.bounding_box)
                gps = camera.gpsFromImage([center.x, center.y])
                lat, lon = gps[0], gps[1]
                detection.geo_coordinate.latitude = lat
                detection.geo_coordinate.longitude = lon

        return self._pack_proto(sae_msg)
        
    def _get_center(self, bbox: BoundingBox) -> Point:
        return Point(
            x=(bbox.min_x + bbox.max_x) / 2,
            y=(bbox.min_y + bbox.max_y) / 2
        )

    @PROTO_DESERIALIZATION_DURATION.time()
    def _unpack_proto(self, sae_message_bytes):
        sae_msg = SaeMessage()
        sae_msg.ParseFromString(sae_message_bytes)

        return sae_msg
    
    @PROTO_SERIALIZATION_DURATION.time()
    def _pack_proto(self, sae_msg: SaeMessage):
        return sae_msg.SerializeToString()