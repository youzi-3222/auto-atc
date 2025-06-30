from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.atc.core.scene.weather import Cloud, CloudType, Weather


# 测试 Cloud 类
def test_cloud_initialization():
    cloud = Cloud(CloudType.FEW, 2000)
    assert cloud.cloud_type == CloudType.FEW
    assert cloud.height_ft == 2000
    assert cloud.height_level() == 20
    assert str(cloud) == "FEW2000"


def test_cloud_validation():
    with pytest.raises(AssertionError, match="云层类型必须是 CloudType 枚举"):
        Cloud("INVALID_TYPE", 2000)

    with pytest.raises(AssertionError, match="云层高度必须是非负整数"):
        Cloud(CloudType.FEW, -100)


# 测试 Weather 类
def test_weather_initialization(mocker):
    # 模拟 API 响应
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "rawOb": "ZGGG 010000Z 08008KT 9999 FEW020 SCT030 BKN100 25/20 Q1012 NOSIG",
            "reportTime": "2035-01-01 00:00:00",
            "temp": 25,
            "dewp": 20,
            "altim": 1012,
            "wdir": 80,
            "wspd": 8,
            "visib": "6+",
            "clouds": [
                {"cover": "FEW", "base": 2000},
                {"cover": "SCT", "base": 3000},
                {"cover": "BKN", "base": 10000},
            ],
            "name": "Guangzhou Baiyun Intl Airport",
        }
    ]
    mock_response.ok = True

    mocker.patch("requests.get", return_value=mock_response)

    weather = Weather("ZGGG")

    assert weather.icao == "ZGGG"
    assert weather.raw == mock_response.json.return_value[0]["rawOb"]
    assert weather.time == datetime(2035, 1, 1, 0, 0, 0)
    assert weather.temp_c == 25
    assert weather.dewpoint_c == 20
    assert weather.qnh_hpa == 1012
    assert weather.wind_dir == 80
    assert weather.wind_speed_kt == 8
    assert len(weather.cloud) == 3
    assert weather.cloud[0].cloud_type == CloudType.FEW
    assert weather.cloud[0].height_ft == 2000
    assert weather.cloud[1].cloud_type == CloudType.SCT
    assert weather.cloud[1].height_ft == 3000
    assert weather.cloud[2].cloud_type == CloudType.BKN
    assert weather.cloud[2].height_ft == 10000
    assert weather.name == "Guangzhou Baiyun Intl Airport"


def test_weather_api_failure(mocker):
    # 模拟 API 失败
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 500

    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(AssertionError, match="获取天气信息失败（500）"):
        Weather("ZGGG")


def test_weather_invalid_data(mocker):
    # 模拟无效的 API 响应
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.ok = True

    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(AssertionError, match="未获取到有效的天气信息"):
        Weather("ZGGG")
