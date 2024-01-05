# setup.py
from PyInstaller.__main__ import run

if __name__ == "__main__":
    run([
        'baidu_app.py',      # 要打包的 Python 脚本文件
        '--onefile',         # 打包成单个可执行文件
        '--noconsole',       # 不显示控制台窗口（如果是GUI应用）
        '--icon=logo.ico',  # 指定程序图标，将 your_logo.ico 替换为你自己的图标文件路径
        # 其他选项和资源文件
    ])
