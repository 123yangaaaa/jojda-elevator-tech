#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奥的斯电梯产品图下载器
自动下载 https://www.otiscreate.com/product-finder/zh/cn 页面中的所有产品图
"""

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OtisProductDownloader:
    def __init__(self, download_dir="otis_products"):
        self.download_dir = download_dir
        self.base_url = "https://www.otiscreate.com/product-finder/zh/cn"
        self.driver = None
        self.setup_download_directory()
        
    def setup_download_directory(self):
        """创建下载目录"""
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logger.info(f"创建下载目录: {self.download_dir}")
    
    def setup_driver(self):
        """设置Chrome浏览器驱动"""
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
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome浏览器启动成功")
        except Exception as e:
            logger.error(f"启动Chrome浏览器失败: {e}")
            raise
    
    def wait_for_element(self, by, value, timeout=10):
        """等待元素出现"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"等待元素超时: {value}")
            return None
    
    def get_product_categories(self):
        """获取所有产品类别"""
        try:
            # 等待页面加载
            time.sleep(3)
            
            # 查找产品类别元素
            categories = self.driver.find_elements(By.CSS_SELECTOR, ".product-category, .category-item, [data-category]")
            
            if not categories:
                # 尝试其他选择器
                categories = self.driver.find_elements(By.CSS_SELECTOR, ".product-item, .solution-item, .category")
            
            logger.info(f"找到 {len(categories)} 个产品类别")
            return categories
            
        except Exception as e:
            logger.error(f"获取产品类别失败: {e}")
            return []
    
    def get_product_specifications(self):
        """获取产品规格选项"""
        try:
            # 常见的规格字段
            spec_fields = [
                "楼层数", "载重量", "速度", "井道尺寸", "轿厢尺寸",
                "floors", "capacity", "speed", "hoistway", "car"
            ]
            
            specifications = {}
            for field in spec_fields:
                try:
                    # 查找输入框或选择框
                    elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{field}') or contains(@placeholder, '{field}')]")
                    if elements:
                        specifications[field] = elements
                except:
                    continue
            
            return specifications
            
        except Exception as e:
            logger.error(f"获取产品规格失败: {e}")
            return {}
    
    def fill_specifications(self, specifications):
        """填写产品规格"""
        try:
            # 这里需要根据实际网站的表单结构来填写
            # 由于无法直接访问网站，这里提供通用的填写逻辑
            
            for field, elements in specifications.items():
                if elements:
                    element = elements[0]
                    try:
                        if element.tag_name == "input":
                            # 输入框
                            element.clear()
                            element.send_keys("标准规格")  # 使用默认值
                        elif element.tag_name == "select":
                            # 下拉选择框
                            options = element.find_elements(By.TAG_NAME, "option")
                            if options:
                                options[1].click()  # 选择第一个非默认选项
                        
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.warning(f"填写规格 {field} 失败: {e}")
                        continue
            
            logger.info("规格填写完成")
            
        except Exception as e:
            logger.error(f"填写规格失败: {e}")
    
    def download_product_drawing(self, product_name):
        """下载产品图纸"""
        try:
            # 查找下载按钮
            download_buttons = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), '下载') or contains(text(), 'Download') or contains(@class, 'download')]")
            
            if download_buttons:
                download_buttons[0].click()
                logger.info(f"开始下载产品: {product_name}")
                
                # 等待下载完成
                time.sleep(5)
                
                # 检查下载文件
                downloaded_files = os.listdir(self.download_dir)
                if downloaded_files:
                    logger.info(f"下载完成: {downloaded_files[-1]}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"下载产品图纸失败: {e}")
            return False
    
    def process_product(self, product_element, product_index):
        """处理单个产品"""
        try:
            # 获取产品名称
            product_name = product_element.text.strip() or f"product_{product_index}"
            logger.info(f"处理产品: {product_name}")
            
            # 点击产品
            product_element.click()
            time.sleep(2)
            
            # 获取规格选项
            specifications = self.get_product_specifications()
            
            if specifications:
                # 填写规格
                self.fill_specifications(specifications)
                
                # 下载图纸
                success = self.download_product_drawing(product_name)
                
                if success:
                    logger.info(f"产品 {product_name} 处理成功")
                else:
                    logger.warning(f"产品 {product_name} 下载失败")
            else:
                logger.warning(f"产品 {product_name} 没有找到规格选项")
            
            # 返回上一页
            try:
                back_button = self.driver.find_element(By.XPATH, "//*[contains(text(), '返回') or contains(text(), 'Back')]")
                back_button.click()
                time.sleep(2)
            except:
                # 如果没有返回按钮，刷新页面
                self.driver.refresh()
                time.sleep(3)
            
        except Exception as e:
            logger.error(f"处理产品失败: {e}")
    
    def run(self):
        """运行下载器"""
        try:
            logger.info("开始下载奥的斯电梯产品图")
            
            # 设置浏览器
            self.setup_driver()
            
            # 访问网站
            self.driver.get(self.base_url)
            logger.info(f"访问网站: {self.base_url}")
            
            # 等待页面加载
            time.sleep(5)
            
            # 获取所有产品类别
            products = self.get_product_categories()
            
            if not products:
                logger.error("没有找到产品类别")
                return
            
            # 处理每个产品
            for index, product in enumerate(products):
                try:
                    self.process_product(product, index + 1)
                except Exception as e:
                    logger.error(f"处理产品 {index + 1} 时出错: {e}")
                    continue
            
            logger.info("所有产品处理完成")
            
        except Exception as e:
            logger.error(f"下载器运行失败: {e}")
        
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("浏览器已关闭")

def main():
    """主函数"""
    downloader = OtisProductDownloader()
    downloader.run()

if __name__ == "__main__":
    main() 