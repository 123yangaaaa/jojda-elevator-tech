#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版奥的斯电梯产品图下载器
不依赖webdriver-manager，使用系统Chrome驱动
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleOtisDownloader:
    def __init__(self, download_dir="otis_products"):
        self.download_dir = download_dir
        self.base_url = "https://www.otiscreate.com/product-finder/zh/cn"
        self.driver = None
        self.setup_download_directory()
        
    def setup_download_directory(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logger.info(f"创建下载目录: {self.download_dir}")
    
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 设置下载目录
        prefs = {
            "download.default_directory": os.path.abspath(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.always_open_pdf_externally": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            # 尝试使用系统Chrome驱动
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome浏览器启动成功")
        except Exception as e:
            logger.error(f"启动Chrome浏览器失败: {e}")
            logger.info("请确保已安装Chrome浏览器和ChromeDriver")
            raise
    
    def analyze_page(self):
        logger.info("分析页面结构...")
        time.sleep(15)  # 等待页面完全加载
        
        # 保存页面源码
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        logger.info("页面源码已保存到 page_source.html")
        
        # 查找所有按钮
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        logger.info(f"找到 {len(buttons)} 个按钮")
        
        # 显示前10个按钮的文本
        for i, button in enumerate(buttons[:10]):
            try:
                text = button.text.strip()
                if text:
                    logger.info(f"  按钮 {i+1}: {text}")
            except:
                pass
        
        # 查找所有链接
        links = self.driver.find_elements(By.TAG_NAME, "a")
        logger.info(f"找到 {len(links)} 个链接")
        
        # 显示前10个链接的文本
        for i, link in enumerate(links[:10]):
            try:
                text = link.text.strip()
                if text:
                    logger.info(f"  链接 {i+1}: {text}")
            except:
                pass
        
        # 查找包含特定文本的元素
        text_patterns = ["电梯", "产品", "下载", "Download", "Product", "Elevator", "Create", "Design"]
        for pattern in text_patterns:
            elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{pattern}')]")
            if elements:
                logger.info(f"包含 '{pattern}' 的元素: {len(elements)} 个")
                for i, elem in enumerate(elements[:3]):
                    try:
                        text = elem.text.strip()
                        if text and len(text) < 100:
                            logger.info(f"  {elem.tag_name}: {text}")
                    except:
                        pass
        
        # 查找可能的下载按钮
        download_patterns = [
            "//*[contains(text(), '下载')]",
            "//*[contains(text(), 'Download')]",
            "//*[contains(text(), '导出')]",
            "//*[contains(text(), 'Export')]",
            "//*[contains(text(), '生成')]",
            "//*[contains(text(), 'Generate')]",
            "//*[contains(text(), 'Create')]"
        ]
        
        logger.info("查找下载按钮:")
        for pattern in download_patterns:
            elements = self.driver.find_elements(By.XPATH, pattern)
            if elements:
                logger.info(f"  使用模式 '{pattern}' 找到 {len(elements)} 个元素")
                for i, elem in enumerate(elements[:2]):
                    try:
                        text = elem.text.strip()
                        if text:
                            logger.info(f"    {elem.tag_name}: {text}")
                    except:
                        pass
    
    def run(self):
        try:
            logger.info("开始分析奥的斯网站")
            self.setup_driver()
            self.driver.get(self.base_url)
            logger.info(f"访问网站: {self.base_url}")
            self.analyze_page()
            logger.info("分析完成")
            
        except Exception as e:
            logger.error(f"运行失败: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("浏览器已关闭")

def main():
    downloader = SimpleOtisDownloader()
    downloader.run()

if __name__ == "__main__":
    main() 