import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
import os

class MacImageClicker:
    def __init__(self):
        print("[✅] Mac 图像识别点击器初始化完成")

    def screenshot(self):
        img = pyautogui.screenshot()
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def find_image(self, template_path, threshold=0.8):
        if not os.path.exists(template_path):
            print(f"[❌] 模板图像不存在: {template_path}")
            return None

        screen = self.screenshot()
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = template.shape[:2]
            center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return center
        return None

    def click_at(self, pos):
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.click()

    def run_task(self, name, image_path, offset=(0, 0), threshold=0.8, max_retries=3, retry_delay=0.5):
        print(f"[🔍] 执行任务: {name}")
        for attempt in range(max_retries):
            match_pos = self.find_image(image_path, threshold)
            if match_pos:
                click_pos = (match_pos[0] + offset[0], match_pos[1] + offset[1])
                self.click_at(click_pos)
                print(f"[✅] 点击成功: {click_pos}")
                return True
            else:
                print(f"[⏳] 第 {attempt+1} 次未找到图像，等待重试...")
                time.sleep(retry_delay)
        print(f"[❌] 未找到图像: {image_path}")
        return False