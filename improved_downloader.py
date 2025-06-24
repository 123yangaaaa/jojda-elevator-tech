#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的奥的斯产品下载器 - 分析实际页面流程并实现自动化下载
"""

import os
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImprovedOtisDownloader:
    def __init__(self):
        self.base_url = "https://www.otiscreate.com/product-finder/zh/cn"
        self.driver = None
        self.wait = None
        self.download_dir = "otis_products"
        
        # 确保下载目录存在
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def setup_driver(self):
        """设置Chrome浏览器"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 设置下载目录
        prefs = {
            "download.default_directory": os.path.abspath(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            logger.info("Chrome浏览器启动成功")
            return True
        except Exception as e:
            logger.error(f"启动浏览器失败: {e}")
            return False
    
    def analyze_page_structure(self):
        """分析页面结构，了解实际的工作流程"""
        try:
            logger.info("开始分析页面结构...")
            
            # 访问网站
            self.driver.get(self.base_url)
            time.sleep(5)
            
            # 保存初始页面
            self.save_page_state("initial_page")
            
            # 查找产品卡片
            products = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'product')]")
            logger.info(f"找到 {len(products)} 个产品")
            
            if products:
                # 分析第一个产品
                first_product = products[0]
                self.analyze_product_structure(first_product)
                
                # 尝试点击解决方案按钮
                self.try_click_solution_button(first_product)
            
            return True
            
        except Exception as e:
            logger.error(f"分析页面结构时出错: {e}")
            return False
    
    def analyze_product_structure(self, product_element):
        """分析单个产品的结构"""
        try:
            logger.info("=" * 50)
            logger.info("分析产品结构...")
            logger.info("=" * 50)
            
            # 获取产品名称
            try:
                product_name = product_element.find_element(By.XPATH, ".//div[contains(@class, 'product-name')]").text
                logger.info(f"产品名称: {product_name}")
            except:
                logger.warning("无法获取产品名称")
            
            # 查找所有按钮和链接
            buttons = product_element.find_elements(By.XPATH, ".//a | .//button")
            logger.info(f"找到 {len(buttons)} 个按钮/链接")
            
            for i, button in enumerate(buttons):
                try:
                    text = button.text.strip()
                    href = button.get_attribute("href")
                    onclick = button.get_attribute("onclick")
                    id_attr = button.get_attribute("id")
                    class_attr = button.get_attribute("class")
                    
                    info = {
                        "index": i,
                        "text": text,
                        "href": href,
                        "onclick": onclick,
                        "id": id_attr,
                        "class": class_attr,
                        "visible": button.is_displayed(),
                        "enabled": button.is_enabled()
                    }
                    
                    if button.is_displayed():
                        logger.info(f"可见按钮 {i+1}: {info}")
                        
                except Exception as e:
                    logger.error(f"分析按钮 {i} 时出错: {e}")
            
            # 查找产品图片
            try:
                images = product_element.find_elements(By.XPATH, ".//img")
                for i, img in enumerate(images):
                    src = img.get_attribute("src")
                    alt = img.get_attribute("alt")
                    logger.info(f"图片 {i+1}: src={src}, alt={alt}")
            except Exception as e:
                logger.error(f"分析图片时出错: {e}")
                
        except Exception as e:
            logger.error(f"分析产品结构时出错: {e}")
    
    def try_click_solution_button(self, product_element):
        """尝试点击解决方案按钮"""
        try:
            logger.info("尝试点击解决方案按钮...")
            
            # 查找解决方案按钮
            solution_button = product_element.find_element(By.XPATH, ".//a[@id='create']")
            
            if solution_button and solution_button.is_displayed():
                logger.info("找到解决方案按钮，准备点击...")
                
                # 保存点击前的页面
                self.save_page_state("before_solution_click")
                
                # 点击按钮
                solution_button.click()
                logger.info("已点击解决方案按钮")
                
                # 等待页面变化
                time.sleep(5)
                
                # 保存点击后的页面
                self.save_page_state("after_solution_click")
                
                # 分析点击后的页面
                self.analyze_page_after_click()
                
            else:
                logger.warning("未找到可点击的解决方案按钮")
                
        except Exception as e:
            logger.error(f"点击解决方案按钮时出错: {e}")
    
    def analyze_page_after_click(self):
        """分析点击解决方案按钮后的页面"""
        try:
            logger.info("=" * 50)
            logger.info("分析点击后的页面...")
            logger.info("=" * 50)
            
            # 检查URL是否变化
            current_url = self.driver.current_url
            logger.info(f"当前URL: {current_url}")
            
            # 查找表单元素
            forms = self.driver.find_elements(By.XPATH, "//form")
            logger.info(f"找到 {len(forms)} 个表单")
            
            # 查找输入字段
            inputs = self.driver.find_elements(By.XPATH, "//input | //select | //textarea")
            logger.info(f"找到 {len(inputs)} 个输入元素")
            
            for i, input_elem in enumerate(inputs):
                try:
                    if input_elem.is_displayed():
                        input_type = input_elem.get_attribute("type")
                        input_name = input_elem.get_attribute("name")
                        input_id = input_elem.get_attribute("id")
                        placeholder = input_elem.get_attribute("placeholder")
                        
                        logger.info(f"可见输入 {i+1}: type={input_type}, name={input_name}, id={input_id}, placeholder={placeholder}")
                        
                except Exception as e:
                    logger.error(f"分析输入元素 {i} 时出错: {e}")
            
            # 查找下载按钮
            download_buttons = self.driver.find_elements(By.XPATH, "//*[contains(text(), '下载') or contains(text(), 'Download') or contains(text(), '生成') or contains(text(), 'Generate')]")
            logger.info(f"找到 {len(download_buttons)} 个可能的下载按钮")
            
            for i, button in enumerate(download_buttons):
                try:
                    if button.is_displayed():
                        text = button.text.strip()
                        tag = button.tag_name
                        logger.info(f"可能的下载按钮 {i+1}: {tag} - {text}")
                        
                except Exception as e:
                    logger.error(f"分析下载按钮 {i} 时出错: {e}")
            
            # 查找所有链接
            links = self.driver.find_elements(By.XPATH, "//a[@href]")
            logger.info(f"找到 {len(links)} 个链接")
            
            for i, link in enumerate(links):
                try:
                    if link.is_displayed():
                        href = link.get_attribute("href")
                        text = link.text.strip()
                        if "download" in href.lower() or "pdf" in href.lower() or "drawing" in href.lower():
                            logger.info(f"可能的下载链接 {i+1}: {text} -> {href}")
                            
                except Exception as e:
                    logger.error(f"分析链接 {i} 时出错: {e}")
                    
        except Exception as e:
            logger.error(f"分析点击后页面时出错: {e}")
    
    def save_page_state(self, prefix):
        """保存页面状态"""
        try:
            # 保存HTML
            page_source = self.driver.page_source
            with open(f"{prefix}.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            
            # 保存截图
            self.driver.save_screenshot(f"{prefix}.png")
            logger.info(f"已保存 {prefix} 页面状态")
        except Exception as e:
            logger.error(f"保存页面状态失败: {e}")
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            logger.info("浏览器已关闭")

def main():
    downloader = ImprovedOtisDownloader()
    try:
        if downloader.setup_driver():
            downloader.analyze_page_structure()
            input("按Enter键关闭浏览器...")
    except Exception as e:
        logger.error(f"主程序运行失败: {e}")
    finally:
        downloader.close()

if __name__ == "__main__":
    main() 