#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能奥的斯电梯产品图下载器
能够正确处理页面跳转和动态加载
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
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SmartOtisDownloader:
    def __init__(self, download_dir="otis_products"):
        self.base_url = "https://www.otiscreate.com/product-finder/zh/cn"
        self.driver = None
        self.wait = None
        self.download_dir = download_dir
        
    def setup_driver(self):
        """设置Chrome浏览器"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 设置下载目录
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        
        download_prefs = {
            "download.default_directory": os.path.abspath(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", download_prefs)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            logger.info("Chrome浏览器启动成功")
            return True
        except Exception as e:
            logger.error(f"启动浏览器失败: {e}")
            return False
    
    def navigate_to_product_specs(self, product_name):
        """导航到产品规格页面"""
        try:
            logger.info("访问奥的斯网站...")
            self.driver.get(self.base_url)
            time.sleep(10)
            
            # 查找产品卡片
            logger.info(f"查找产品: {product_name}")
            product_xpath = f"//div[contains(@class, 'product') and .//div[@class='product-name' and contains(text(), '{product_name}')]]"
            product_card = self.wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
            logger.info(f"找到产品卡: {product_name}")
            
            # 点击解决方案按钮
            solution_xpath = ".//div[contains(@class, 'action-buttons')]//div[contains(@class, 'action-items')]//a[@id='create']"
            solution_link = product_card.find_element(By.XPATH, solution_xpath)
            
            # 获取当前URL
            current_url = self.driver.current_url
            logger.info(f"当前URL: {current_url}")
            
            # 点击解决方案按钮
            solution_link.click()
            logger.info("成功点击解决方案按钮")
            
            # 等待页面跳转或加载
            max_wait_time = 30
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                time.sleep(2)
                new_url = self.driver.current_url
                
                # 检查URL是否发生变化
                if new_url != current_url:
                    logger.info(f"页面已跳转到: {new_url}")
                    break
                    
                # 检查是否出现了规格填写相关的元素
                try:
                    # 查找可能的输入框
                    inputs = self.driver.find_elements(By.XPATH, "//input[@type='text' or @type='number']")
                    if len(inputs) > 0:
                        logger.info(f"发现 {len(inputs)} 个输入框，页面可能已加载规格表单")
                        break
                except:
                    pass
                
                # 检查是否出现了包含"载重"、"速度"等关键词的元素
                try:
                    spec_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '载重') or contains(text(), '速度') or contains(text(), '高度')]")
                    form_elements = [elem for elem in spec_elements if elem.tag_name in ['input', 'select', 'textarea']]
                    if len(form_elements) > 0:
                        logger.info(f"发现规格相关的表单元素")
                        break
                except:
                    pass
                
                logger.info("等待页面加载...")
            
            # 保存当前页面状态
            page_source = self.driver.page_source
            with open("current_page_after_click.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            
            self.driver.save_screenshot("current_page_after_click.png")
            logger.info("已保存当前页面状态")
            
            return True
            
        except Exception as e:
            logger.error(f"导航到产品规格页面失败: {e}")
            return False
    
    def analyze_current_page(self):
        """分析当前页面的结构"""
        logger.info("分析当前页面结构...")
        
        # 分析所有输入框
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        logger.info(f"找到 {len(inputs)} 个输入框:")
        
        for i, input_elem in enumerate(inputs):
            try:
                input_type = input_elem.get_attribute('type')
                input_name = input_elem.get_attribute('name')
                input_id = input_elem.get_attribute('id')
                input_placeholder = input_elem.get_attribute('placeholder')
                is_visible = input_elem.is_displayed()
                
                logger.info(f"  输入框 {i+1}: 类型={input_type}, 名称={input_name}, ID={input_id}, 占位符={input_placeholder}, 可见={is_visible}")
            except Exception as e:
                logger.error(f"分析输入框 {i+1} 时出错: {e}")
        
        # 分析所有按钮
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        logger.info(f"找到 {len(buttons)} 个按钮:")
        
        for i, button in enumerate(buttons):
            try:
                button_text = button.text.strip()
                button_id = button.get_attribute('id')
                is_visible = button.is_displayed()
                
                if button_text and is_visible:
                    logger.info(f"  按钮 {i+1}: 文本='{button_text}', ID={button_id}, 可见={is_visible}")
            except Exception as e:
                logger.error(f"分析按钮 {i+1} 时出错: {e}")
        
        # 查找下载相关的元素
        download_keywords = ["下载", "绘图", "download", "drawing", "图纸", "生成", "创建"]
        
        for keyword in download_keywords:
            try:
                elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{keyword}') and (self::button or self::a or self::input[@type='submit'])]")
                if elements:
                    logger.info(f"包含 '{keyword}' 的可点击元素:")
                    for elem in elements:
                        if elem.is_displayed():
                            logger.info(f"  - {elem.tag_name}: '{elem.text.strip()}', ID={elem.get_attribute('id')}")
            except Exception as e:
                logger.error(f"查找关键词 '{keyword}' 时出错: {e}")
    
    def run_smart_download(self, product_name="ARISE"):
        """运行智能下载流程"""
        logger.info(f"===== 开始为产品 '{product_name}' 执行智能下载流程 =====")
        
        if not self.setup_driver():
            return False
        
        try:
            # 导航到产品规格页面
            if not self.navigate_to_product_specs(product_name):
                return False
            
            # 分析当前页面
            self.analyze_current_page()
            
            # 尝试查找并点击下载按钮
            download_success = self.attempt_download()
            
            if download_success:
                logger.info(f"✅ 产品 '{product_name}' 下载成功")
            else:
                logger.warning(f"⚠️ 产品 '{product_name}' 下载未完成，但已收集页面信息")
            
            return download_success
            
        except Exception as e:
            logger.error(f"智能下载流程出错: {e}")
            return False
        finally:
            if self.driver:
                input("按Enter键关闭浏览器...")
                self.driver.quit()
                logger.info("浏览器已关闭")
    
    def attempt_download(self):
        """尝试执行下载操作"""
        logger.info("尝试查找下载按钮...")
        
        # 可能的下载按钮选择器
        download_selectors = [
            "//button[contains(text(), '下载')]",
            "//button[contains(text(), '绘图')]",
            "//button[contains(text(), 'download')]",
            "//a[contains(text(), '下载')]",
            "//a[contains(text(), '绘图')]",
            "//input[@type='submit' and contains(@value, '下载')]",
            "//*[@id='download' or @id='download-btn' or @id='downloadBtn']",
            "//*[contains(@class, 'download') and (self::button or self::a)]"
        ]
        
        for i, selector in enumerate(download_selectors, 1):
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                visible_elements = [elem for elem in elements if elem.is_displayed()]
                
                if visible_elements:
                    logger.info(f"选择器 {i} 找到 {len(visible_elements)} 个可见的下载元素")
                    for elem in visible_elements:
                        try:
                            elem.click()
                            logger.info(f"✅ 成功点击下载按钮: {elem.text.strip()}")
                            time.sleep(5)
                            return True
                        except Exception as e:
                            logger.warning(f"点击下载按钮失败: {e}")
                            continue
            except Exception as e:
                logger.debug(f"选择器 {i} 查找失败: {e}")
        
        logger.warning("未找到可用的下载按钮")
        return False

def main():
    downloader = SmartOtisDownloader()
    downloader.run_smart_download("ARISE")

if __name__ == "__main__":
    main() 