#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版奥的斯电梯产品图自动下载器
V3.0 - 修复版：采用更精准的元素定位和操作流程
"""

import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedOtisDownloader:
    def __init__(self, download_dir="otis_products"):
        self.base_url = "https://www.otiscreate.com/product-finder/zh/cn"
        self.driver = None
        self.wait = None
        
        # 确保下载目录存在
        self.download_dir = os.path.abspath(download_dir)
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logger.info(f"创建下载目录: {self.download_dir}")
    
    def setup_driver(self):
        """配置并初始化WebDriver"""
        if self.driver: # 如果已有实例，先关闭
            self.driver.quit()

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.always_open_pdf_externally": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            logger.info("正在初始化WebDriver...")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("Chrome浏览器启动成功")
        except Exception as e:
            logger.error(f"启动Chrome浏览器失败: {e}")
            raise

    def safe_click(self, element, description=""):
        """更安全的点击方法，包含滚动和等待"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            self.wait.until(EC.element_to_be_clickable(element)).click()
            logger.info(f"成功点击: {description}")
            return True
        except Exception as e:
            logger.error(f"点击 '{description}' 失败: {e}")
            return False

    def safe_input(self, element, text, description=""):
        """更安全的输入方法"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            element.clear()
            element.send_keys(text)
            logger.info(f"成功输入 '{text}' 到: {description}")
            return True
        except Exception as e:
            logger.error(f"输入 '{text}' 到 '{description}' 失败: {e}")
            return False

    def select_product_solution(self, product_name):
        """根据产品名称查找并点击'解决方案'"""
        logger.info(f"正在查找产品: {product_name}")
        try:
            # 根据实际HTML结构查找产品卡片
            # 查找包含指定产品名称的产品卡片
            product_xpath = f"//div[contains(@class, 'product') and .//div[@class='product-name' and contains(text(), '{product_name}')]]"
            product_card = self.wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
            logger.info(f"找到产品卡: {product_name}")
            
            # 在该产品卡片内查找"解决方案"链接
            # 根据实际HTML结构：action-buttons -> action-items -> a[id='create']
            solution_link_xpath = ".//div[contains(@class, 'action-buttons')]//div[contains(@class, 'action-items')]//a[@id='create']"
            solution_link = product_card.find_element(By.XPATH, solution_link_xpath)
            
            self.safe_click(solution_link, f"产品 '{product_name}' 的解决方案按钮")
            time.sleep(5)
            return True
        except TimeoutException:
            logger.error(f"查找产品 '{product_name}' 超时或未找到。")
            return False
        except Exception as e:
            logger.error(f"选择产品 '{product_name}' 的解决方案时出错: {e}")
            return False

    def fill_specifications(self, specs):
        """根据给定的规格填写表单"""
        logger.info("开始填写产品规格...")
        all_fields_filled = True
        
        for label, value in specs.items():
            logger.info(f"处理字段: '{label}' = '{value}'")
            try:
                # 寻找包含标签文本的父级元素，这更具鲁棒性
                field_container_xpath = f"//*[contains(normalize-space(), '{label}') and (self::p or self::label or self::div)]/ancestor::div[contains(@class, 'form-group') or contains(@class, 'field') or contains(@class, 'form-item')][1]"
                
                try:
                    field_container = self.driver.find_element(By.XPATH, field_container_xpath)
                except NoSuchElementException:
                    # 备用策略：寻找标签旁边的元素
                    field_container_xpath = f"//*[contains(normalize-space(), '{label}')]/parent::*"
                    field_container = self.driver.find_element(By.XPATH, field_container_xpath)

                # 1. 尝试作为下拉菜单处理
                try:
                    dropdown_element = field_container.find_element(By.XPATH, ".//select | .//div[contains(@role, 'button')]")
                    self.safe_click(dropdown_element, f"下拉菜单 '{label}'")
                    time.sleep(1)
                    
                    option_xpath = f"//li[normalize-space()='{value}'] | //div[contains(@class, 'option') and normalize-space()='{value}'] | //option[normalize-space()='{value}']"
                    option_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
                    self.safe_click(option_element, f"选项 '{value}' for '{label}'")
                    logger.info(f"成功选择 '{label}': '{value}'")
                    continue
                except NoSuchElementException:
                    pass # 不是下拉菜单，继续

                # 2. 尝试作为普通输入框处理
                try:
                    input_field = field_container.find_element(By.XPATH, ".//input")
                    self.safe_input(input_field, value, f"输入框 '{label}'")
                    logger.info(f"成功输入 '{label}': '{value}'")
                    continue
                except NoSuchElementException:
                    logger.warning(f"在容器中未找到 '{label}' 的输入框。")

                logger.warning(f"未能处理字段: '{label}'")
                all_fields_filled = False

            except Exception as e:
                logger.error(f"处理字段 '{label}' 时出错: {e}")
                all_fields_filled = False
        
        return all_fields_filled

    def find_and_click_download_button(self):
        """查找并点击下载/绘图按钮"""
        logger.info("正在查找下载按钮...")
        patterns = [
            "//button[contains(., '下载绘图')]",
            "//button[contains(., '下载')]",
            "//a[contains(., '下载')]",
            "//button[contains(., '生成')]",
            "//button[contains(., 'Create')]"
        ]
        for pattern in patterns:
            try:
                buttons = self.driver.find_elements(By.XPATH, pattern)
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        self.safe_click(button, f"下载按钮 (Pattern: {pattern})")
                        time.sleep(5)
                        return True
            except Exception as e:
                logger.warning(f"使用模式 '{pattern}' 查找下载按钮时出错: {e}")
        logger.error("最终未能找到任何可点击的下载按钮。")
        return False
        
    def wait_for_download(self, timeout=90):
        """等待下载完成"""
        logger.info(f"等待下载完成... (超时: {timeout}s)")
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            # 查找所有.crdownload临时文件
            temp_files = [f for f in os.listdir(self.download_dir) if f.endswith('.crdownload')]
            if not temp_files and any(f.lower().endswith(('.pdf', '.dwg', '.zip', '.png')) for f in os.listdir(self.download_dir)):
                 # 检查是否有新文件（非临时文件）
                 # 此处逻辑可以更复杂，比如检查特定时间后创建的文件
                 logger.info("检测到下载活动完成。")
                 time.sleep(3) # 等待文件系统稳定
                 return True
            time.sleep(2)
        
        logger.warning("下载超时。")
        return False

    def run_automation(self, product_name, specs):
        """运行单个产品的完整自动化下载流程"""
        try:
            logger.info(f"===== 开始为产品 '{product_name}' 执行自动化流程 =====")
            
            self.driver.get(self.base_url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            if not self.select_product_solution(product_name):
                logger.error(f"选择产品 '{product_name}' 失败，中止任务。")
                return False
            
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2) # 等待页面稳定

            if not self.fill_specifications(specs):
                logger.warning("部分或全部规格填写失败，仍将尝试下载。")

            time.sleep(3)

            if self.find_and_click_download_button():
                if self.wait_for_download():
                    logger.info(f"✅ 产品 '{product_name}' 下载成功。")
                    return True
                else:
                    logger.error(f"❌ 产品 '{product_name}' 下载超时。")
                    return False
            else:
                logger.error(f"❌ 未能为产品 '{product_name}' 点击下载按钮。")
                return False
        except Exception as e:
            logger.error(f"为产品 '{product_name}' 执行时发生致命错误: {e}")
            self.capture_screenshot(f"error_{product_name}")
            return False
            
    def capture_screenshot(self, name):
        """捕获当前页面截图用于调试"""
        try:
            path = os.path.join(self.download_dir, f"{name}_{int(time.time())}.png")
            self.driver.save_screenshot(path)
            logger.info(f"错误截图已保存至: {path}")
        except Exception as e:
            logger.error(f"保存截图失败: {e}")

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("浏览器已关闭。")

if __name__ == '__main__':
    # 用于直接运行测试
    downloader = None
    try:
        downloader = EnhancedOtisDownloader()
        downloader.setup_driver()
        # 测试下载 ARISE 产品
        downloader.run_automation("ARISE", {
            "载重(kg)": "1000",
            "速度(m/s)": "1.75",
            "轿厢宽度(mm)": "1100",
            "轿厢深度(mm)": "2100",
            "对重位置": "左侧"
        })
    except Exception as e:
        logger.error(f"主程序运行失败: {e}")
    finally:
        if downloader:
            downloader.close() 