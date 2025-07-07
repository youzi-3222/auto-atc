"""
程序入口点。
"""

# https://www.bilibili.com/video/BV1kK411q7fk
# https://mskclover.com/2024/04/19/LES-air-traffic-control-automation-guide/
# https://std.samr.gov.cn/hb/hbQuery?initnode=MH%20%E6%B0%91%E7%94%A8%E8%88%AA%E7%A9%BA
from atc.display import MainWindow

if __name__ == "__main__":
    window = MainWindow()
    while window.running:
        window.render()
