from pydantic import BaseModel, conint, conlist
from pydantic_settings import BaseSettings, SettingsConfigDict
from visionlib.pipeline.settings import LogLevel, YamlConfigSettingsSource
from typing import List


class RedisConfig(BaseModel):
    host: str = 'localhost'
    port: conint(ge=1, le=65536) = 6379
    input_stream_prefix: str = 'objecttracker'
    output_stream_prefix: str = 'geomapper'

class CameraConfig(BaseModel):
    stream_id: str
    focallength_mm: float
    sensor_height_mm: float
    sensor_width_mm: float
    image_width_px: int
    image_height_px: int
    elevation_m: float
    tilt_deg: float
    pos_lat: float
    pos_lon: float
    heading_deg: float


class GeoMapperConfig(BaseSettings):
    log_level: LogLevel = LogLevel.WARNING
    redis: RedisConfig
    cameras: List[CameraConfig]


    model_config = SettingsConfigDict(env_nested_delimiter='__')

    @classmethod
    def settings_customise_sources(cls, settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings):
        return (init_settings, env_settings, YamlConfigSettingsSource(settings_cls), file_secret_settings)