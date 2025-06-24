#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奥的斯电梯产品图下载器 - 高级版本
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
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
import logging
import re

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
            # 使用webdriver-manager自动下载Chrome驱动
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 执行脚本来隐藏自动化特征
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
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
    
    def wait_for_clickable(self, by, value, timeout=10):
        """等待元素可点击"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"等待元素可点击超时: {value}")
            return None
    
    def get_product_categories(self):
        """获取所有产品类别"""
        try:
            # 等待页面加载
            time.sleep(5)
            
            # 尝试多种选择器来找到产品类别
            selectors = [
                ".product-category", ".category-item", "[data-category]",
                ".product-item", ".solution-item", ".category",
                ".elevator-type", ".product-type", ".solution-type",
                "button[onclick*='product']", "a[href*='product']",
                ".card", ".tile", ".item"
            ]
            
            categories = []
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        categories.extend(elements)
                        logger.info(f"使用选择器 '{selector}' 找到 {len(elements)} 个元素")
                        break
                except:
                    continue
            
            # 如果还是没找到，尝试通过文本内容查找
            if not categories:
                text_selectors = [
                    "//*[contains(text(), '乘客电梯')]",
                    "//*[contains(text(), '货梯')]",
                    "//*[contains(text(), '观光电梯')]",
                    "//*[contains(text(), 'Passenger')]",
                    "//*[contains(text(), 'Freight')]",
                    "//*[contains(text(), 'Observation')]"
                ]
                
                for xpath in text_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            categories.extend(elements)
                            logger.info(f"使用XPath '{xpath}' 找到 {len(elements)} 个元素")
                    except:
                        continue
            
            # 去重
            unique_categories = []
            seen_texts = set()
            for category in categories:
                text = category.text.strip()
                if text and text not in seen_texts:
                    unique_categories.append(category)
                    seen_texts.add(text)
            
            logger.info(f"找到 {len(unique_categories)} 个唯一产品类别")
            return unique_categories
            
        except Exception as e:
            logger.error(f"获取产品类别失败: {e}")
            return []
    
    def get_product_specifications(self):
        """获取产品规格选项"""
        try:
            # 常见的规格字段（中英文）
            spec_fields = [
                "楼层数", "载重量", "速度", "井道尺寸", "轿厢尺寸", "提升高度",
                "floors", "capacity", "speed", "hoistway", "car", "height",
                "层数", "重量", "速率", "井道", "轿厢", "高度"
            ]
            
            specifications = {}
            for field in spec_fields:
                try:
                    # 查找输入框或选择框
                    xpath_patterns = [
                        f"//*[contains(text(), '{field}')]",
                        f"//*[contains(@placeholder, '{field}')]",
                        f"//*[contains(@name, '{field}')]",
                        f"//*[contains(@id, '{field}')]",
                        f"//label[contains(text(), '{field}')]/following-sibling::*",
                        f"//label[contains(text(), '{field}')]/parent::*/input",
                        f"//label[contains(text(), '{field}')]/parent::*/select"
                    ]
                    
                    for xpath in xpath_patterns:
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        if elements:
                            specifications[field] = elements
                            break
                            
                except:
                    continue
            
            logger.info(f"找到 {len(specifications)} 个规格字段")
            return specifications
            
        except Exception as e:
            logger.error(f"获取产品规格失败: {e}")
            return {}
    
    def fill_specifications(self, specifications):
        """填写产品规格"""
        try:
            filled_count = 0
            
            for field, elements in specifications.items():
                if elements:
                    element = elements[0]
                    try:
                        if element.tag_name == "input":
                            # 输入框
                            element.clear()
                            # 根据字段类型填写不同的默认值
                            if "楼层" in field or "floors" in field.lower():
                                element.send_keys("10")
                            elif "载重" in field or "capacity" in field.lower():
                                element.send_keys("1000")
                            elif "速度" in field or "speed" in field.lower():
                                element.send_keys("1.75")
                            else:
                                element.send_keys("标准")
                                
                        elif element.tag_name == "select":
                            # 下拉选择框
                            options = element.find_elements(By.TAG_NAME, "option")
                            if len(options) > 1:
                                options[1].click()  # 选择第一个非默认选项
                            elif len(options) == 1:
                                options[0].click()
                                
                        filled_count += 1
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.warning(f"填写规格 {field} 失败: {e}")
                        continue
            
            logger.info(f"成功填写 {filled_count} 个规格字段")
            
        except Exception as e:
            logger.error(f"填写规格失败: {e}")
    
    def find_download_button(self):
        """查找下载按钮"""
        try:
            # 多种可能的下载按钮选择器
            download_selectors = [
                "//*[contains(text(), '下载')]",
                "//*[contains(text(), 'Download')]",
                "//*[contains(@class, 'download')]",
                "//*[contains(@id, 'download')]",
                "//button[contains(@onclick, 'download')]",
                "//a[contains(@href, 'download')]",
                "//*[contains(text(), '导出')]",
                "//*[contains(text(), 'Export')]",
                "//*[contains(text(), '生成')]",
                "//*[contains(text(), 'Generate')]"
            ]
            
            for selector in download_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        # 找到第一个可见的元素
                        for element in elements:
                            if element.is_displayed():
                                return element
                except:
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"查找下载按钮失败: {e}")
            return None
    
    def download_product_drawing(self, product_name):
        """下载产品图纸"""
        try:
            # 查找下载按钮
            download_button = self.find_download_button()
            
            if download_button:
                # 记录下载前的文件数量
                files_before = set(os.listdir(self.download_dir))
                
                # 点击下载按钮
                download_button.click()
                logger.info(f"开始下载产品: {product_name}")
                
                # 等待下载完成
                time.sleep(10)
                
                # 检查是否有新文件下载
                files_after = set(os.listdir(self.download_dir))
                new_files = files_after - files_before
                
                if new_files:
                    logger.info(f"下载完成: {list(new_files)}")
                    return True
                else:
                    logger.warning("没有检测到新下载的文件")
                    return False
            else:
                logger.warning("没有找到下载按钮")
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
            time.sleep(3)
            
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
                # 即使没有规格，也尝试下载
                self.download_product_drawing(product_name)
            
            # 返回上一页
            try:
                back_selectors = [
                    "//*[contains(text(), '返回')]",
                    "//*[contains(text(), 'Back')]",
                    "//*[contains(text(), '上一页')]",
                    "//*[contains(text(), 'Previous')]",
                    "//button[contains(@class, 'back')]",
                    "//a[contains(@class, 'back')]"
                ]
                
                for selector in back_selectors:
                    try:
                        back_button = self.driver.find_element(By.XPATH, selector)
                        if back_button.is_displayed():
                            back_button.click()
                            time.sleep(2)
                            return
                    except:
                        continue
                
                # 如果没有找到返回按钮，尝试浏览器后退
                self.driver.back()
                time.sleep(3)
                
            except Exception as e:
                logger.warning(f"返回上一页失败: {e}")
                # 如果都失败了，刷新页面
                self.driver.refresh()
                time.sleep(5)
            
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
            time.sleep(8)
            
            # 获取所有产品类别
            products = self.get_product_categories()
            
            if not products:
                logger.error("没有找到产品类别")
                # 保存页面源码以便调试
                with open("page_source.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                logger.info("已保存页面源码到 page_source.html")
                return
            
            # 处理每个产品
            for index, product in enumerate(products):
                try:
                    self.process_product(product, index + 1)
                    # 每处理5个产品后稍作休息
                    if (index + 1) % 5 == 0:
                        time.sleep(3)
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