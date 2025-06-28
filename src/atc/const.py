"""
常量。
"""

from pathlib import Path

from pygame import Color

# 渲染
MAX_FPS: int = 30
"""最大 FPS。"""
RESOLUTION: tuple[int, int] = (1280, 720)
"""窗口分辨率。"""
RWY_COLOR: Color = Color(30, 30, 255)
"""跑道显示颜色。"""
RWY_LENGTH: int = 25
"""跑道长度，像素。"""
RWY_LOC_LENGTH: int = 150
"""跑道定位线长度，像素。"""
TICK_TIMEOUT: float = 1.5
"""渲染两帧之间的时间间隔，秒。"""

# 运行
WEATHER_REFRESH_TIMEOUT: int = 10 * 60
"""天气信息刷新间隔，秒。"""

# 路径
CONFIG_PATH = Path("./src/static/config.json")
"""`./static/config.json` 路径。"""
