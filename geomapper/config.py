from typing import List, Optional

from geojson_pydantic import Polygon
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated
from visionlib.pipeline.settings import LogLevel, YamlConfigSettingsSource


class RedisConfig(BaseModel):
    host: str = 'localhost'
    port: Annotated[int, Field(ge=1, le=65536)] = 6379
    input_stream_prefix: str = 'objecttracker'
    output_stream_prefix: str = 'geomapper'

class CameraConfig(BaseModel):
    stream_id: str
    passthrough: bool
    focallength_mm: float = None
    sensor_height_mm: float = None
    sensor_width_mm: float = None
    view_x_deg: float = None
    view_y_deg: float = None
    image_width_px: int = None
    image_height_px: int = None
    elevation_m: float = None
    tilt_deg: float = None
    roll_deg: float = None
    pos_lat: float = None
    pos_lon: float = None
    heading_deg: float = None
    abc_distortion_a: float = None
    abc_distortion_b: float = None
    abc_distortion_c: float = None
    brown_distortion_k1: float = None
    brown_distortion_k2: float = None
    brown_distortion_k3: float = None
    mapping_area: Optional[Polygon] = None
    remove_unmapped_detections: bool = False

class GeoMapperConfig(BaseSettings):
    log_level: LogLevel = LogLevel.WARNING
    redis: RedisConfig
    cameras: List[CameraConfig]
    object_center_elevation_m: float = 0
    prometheus_port: Annotated[int, Field(gt=1024, le=65536)] = 8000    

    model_config = SettingsConfigDict(env_nested_delimiter='__')

    @classmethod
    def settings_customise_sources(cls, settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings):
        return (init_settings, env_settings, YamlConfigSettingsSource(settings_cls), file_secret_settings)