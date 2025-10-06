import os
import sys
import threading
import requests
import zipfile
import subprocess
import winshell
import webview
import time

# --- 配置信息 ---
URLS = {
    "zip": "https://gitee.com/JuryBu/aichart-generator-acg/releases/download/v4.0/AIChartGenerator_4.0%E7%89%88.zip",
    "exe": "https://gitee.com/JuryBu/aichart-generator-acg/releases/download/v4.0/AIChartGenerator_4.0%E7%89%88.exe",
    "py": "https://gitee.com/JuryBu/aichart-generator-acg/releases/download/v4.0/get-pip.py"
}
MAIN_EXE_NAME = "AIChartGenerator_4.0版.exe"
SHORTCUT_NAME = "AI Chart Generator 4.0.lnk"


class Api:
    def __init__(self):
        self.window = None

    def select_directory(self):
        result = self.window.create_file_dialog(webview.FOLDER_DIALOG)
        return result[0] if result else None

    def start_installation(self, install_path):
        thread = threading.Thread(target=self._install_logic, args=(install_path,))
        thread.start()

    def _update_progress(self, percent, message):
        if self.window:
            # 使用转义字符来处理可能的消息中的引号
            escaped_message = message.replace('"', '\\"').replace('\\', '\\\\')
            self.window.evaluate_js(f'update_progress({percent}, "{escaped_message}")')

    def _update_status(self, message, msg_type):
        if self.window:
            escaped_message = message.replace('"', '\\"').replace('\\', '\\\\')
            self.window.evaluate_js(f'update_status("{escaped_message}", "{msg_type}")')

    def _install_logic(self, install_path):
        try:
            os.makedirs(install_path, exist_ok=True)

            # 1. 下载文件
            download_targets = {
                "zip": os.path.join(install_path, "program.zip"),
                "exe": os.path.join(install_path, MAIN_EXE_NAME),
                "py": os.path.join(install_path, "get-pip.py")
            }

            # 下载阶段占总进度的 0-60%
            self.download_file_with_progress(URLS["zip"], download_targets["zip"], "正在下载主程序包...", 0, 30)
            self.download_file_with_progress(URLS["exe"], download_targets["exe"], "正在下载执行文件...", 30, 20)
            self.download_file_with_progress(URLS["py"], download_targets["py"], "正在下载配置脚本...", 50, 10)

            # 2. 解压ZIP文件
            self._update_progress(65, "正在解压文件...")
            with zipfile.ZipFile(download_targets["zip"], 'r') as zip_ref:
                zip_ref.extractall(install_path)
            self._update_progress(75, "解压完成")

            # 3. 运行环境配置脚本
            self._update_progress(80, "正在配置Python环境...")
            python_exe_path = os.path.join(install_path, "python", "python.exe")
            setup_script_path = download_targets["py"]

            if os.path.exists(python_exe_path):
                creationflags = subprocess.CREATE_NO_WINDOW
                process = subprocess.run([python_exe_path, setup_script_path], capture_output=True, text=True,
                                         # 【修改】明确编码以增加健壮性
                                         encoding='utf-8', errors='ignore',
                                         creationflags=creationflags)
                if process.returncode != 0:
                    print(f"环境配置失败: {process.stderr}")
                    raise Exception(f"环境配置脚本执行失败")
                self._update_progress(90, "环境配置成功")
            else:
                self._update_status("警告：未找到嵌入式Python，跳过环境配置", "warning")
                time.sleep(2)  # 让用户看到警告

            # 4. 创建桌面快捷方式
            self._update_progress(95, "正在创建桌面快捷方式...")
            target_exe_path = os.path.join(install_path, MAIN_EXE_NAME)
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, SHORTCUT_NAME)
            with winshell.shortcut(shortcut_path) as shortcut:
                shortcut.path = target_exe_path
                shortcut.working_directory = install_path
                shortcut.description = "AI Chart Generator v4.0"

            # 5. 清理临时文件
            self._update_progress(98, "正在清理临时文件...")
            os.remove(download_targets["zip"])
            os.remove(download_targets["py"])

            # 6. 完成
            self._update_progress(100, "安装成功！此窗口将在3秒后关闭。")
            self.window.evaluate_js('installation_complete("安装成功！")')
            time.sleep(3)

            # 7. 自我销毁
            self_destruct()

        except Exception as e:
            error_message = f"安装失败: {e}"
            print(error_message)
            self._update_status(error_message, "error")

    def download_file_with_progress(self, url, save_path, message_prefix, progress_start, progress_span):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            bytes_downloaded = 0

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bytes_downloaded += len(chunk)
                    if total_size > 0:
                        percent_of_file = (bytes_downloaded / total_size) * 100
                        # 计算在总进度条中的位置
                        total_percent = progress_start + (percent_of_file / 100 * progress_span)

                        mb_downloaded = bytes_downloaded / 1024 / 1024
                        mb_total = total_size / 1024 / 1024
                        message = f"{message_prefix} ({mb_downloaded:.2f}MB / {mb_total:.2f}MB)"
                        self._update_progress(int(total_percent), message)
        except requests.exceptions.RequestException as e:
            raise Exception(f"下载文件失败: {url}") from e


def self_destruct():
    installer_path = sys.executable
    command = f'ping 127.0.0.1 -n 2 > nul & del /F /Q "{installer_path}"'
    subprocess.Popen(command, shell=True, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW)
    sys.exit(0)


if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'AIChartGenerator 安装程序',
        'web/index.html',
        js_api=api,
        width=520,
        height=480,  # 稍微调高一点以适应新布局
        resizable=False
    )
    api.window = window
    webview.start()
