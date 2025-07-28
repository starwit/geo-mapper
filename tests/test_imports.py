import pytest

def test_geommapper_import():
    try:
        from geomapper.geomapper import GeoMapper, Point
    except ImportError as e:
        pytest.fail(f"Failed to import GeoMapper: {e}")

    assert GeoMapper is not None, "GeoMapper should be imported successfully"
    assert Point is not None, "Point should be imported successfully"
        
        