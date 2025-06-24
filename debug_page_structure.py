#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
页面结构分析脚本 - 分析奥的斯网站的实际页面结构
"""

import os
import time
import json
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

class PageStructureAnalyzer:
    def __init__(self):
        self.base_url = "https://www.otiscreate.com/product-finder/zh/cn"
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """设置Chrome浏览器"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            logger.info("Chrome浏览器启动成功")
            return True
        except Exception as e:
            logger.error(f"启动浏览器失败: {e}")
            return False
    
    def analyze_page_structure(self, product_name="ARISE"):
        """分析页面结构"""
        try:
            logger.info(f"开始分析产品 '{product_name}' 的页面结构...")
            
            # 访问网站
            self.driver.get(self.base_url)
            time.sleep(5)
            
            # 查找并点击产品
            logger.info(f"查找产品: {product_name}")
            product_xpath = f"//div[contains(@class, 'product') and .//div[@class='product-name' and contains(text(), '{product_name}')]]"
            product_card = self.wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
            logger.info(f"找到产品卡: {product_name}")
            
            # 保存点击前的页面
            self.save_page_state("before_click")
            
            # 点击解决方案按钮
            solution_xpath = ".//div[contains(@class, 'action-buttons')]//div[contains(@class, 'action-items')]//a[@id='create']"
            solution_link = product_card.find_element(By.XPATH, solution_xpath)
            solution_link.click()
            logger.info("已点击解决方案按钮")
            
            # 等待页面加载
            time.sleep(10)
            
            # 保存点击后的页面
            self.save_page_state("after_click")
            
            # 分析页面结构
            self.analyze_form_elements()
            self.analyze_buttons()
            self.analyze_text_content()
            
            return True
            
        except Exception as e:
            logger.error(f"分析页面结构时出错: {e}")
            return False
    
    def save_page_state(self, prefix):
        """保存页面状态"""
        try:
            # 保存HTML
            page_source = self.driver.page_source
            with open(f"{prefix}_page.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            
            # 保存截图
            self.driver.save_screenshot(f"{prefix}_page.png")
            logger.info(f"已保存 {prefix} 页面状态")
        except Exception as e:
            logger.error(f"保存页面状态失败: {e}")
    
    def analyze_form_elements(self):
        """分析表单元素"""
        logger.info("=" * 50)
        logger.info("分析表单元素...")
        logger.info("=" * 50)
        
        # 查找所有输入元素
        input_elements = self.driver.find_elements(By.XPATH, "//input | //select | //textarea")
        logger.info(f"找到 {len(input_elements)} 个输入元素")
        
        form_data = []
        for i, elem in enumerate(input_elements):
            try:
                info = {
                    "index": i,
                    "tag": elem.tag_name,
                    "type": elem.get_attribute("type"),
                    "name": elem.get_attribute("name"),
                    "id": elem.get_attribute("id"),
                    "placeholder": elem.get_attribute("placeholder"),
                    "class": elem.get_attribute("class"),
                    "value": elem.get_attribute("value"),
                    "visible": elem.is_displayed(),
                    "enabled": elem.is_enabled(),
                    "location": elem.location,
                    "size": elem.size
                }
                form_data.append(info)
                
                if elem.is_displayed():
                    logger.info(f"可见输入 {i+1}: {info}")
                    
            except Exception as e:
                logger.error(f"分析输入元素 {i} 时出错: {e}")
        
        # 保存到文件
        with open("form_elements_analysis.json", "w", encoding="utf-8") as f:
            json.dump(form_data, f, ensure_ascii=False, indent=2)
    
    def analyze_buttons(self):
        """分析按钮元素"""
        logger.info("=" * 50)
        logger.info("分析按钮元素...")
        logger.info("=" * 50)
        
        # 查找所有按钮和链接
        button_elements = self.driver.find_elements(By.XPATH, "//button | //a | //input[@type='submit'] | //input[@type='button']")
        logger.info(f"找到 {len(button_elements)} 个按钮/链接元素")
        
        button_data = []
        for i, elem in enumerate(button_elements):
            try:
                text = elem.text.strip()
                info = {
                    "index": i,
                    "tag": elem.tag_name,
                    "text": text,
                    "id": elem.get_attribute("id"),
                    "class": elem.get_attribute("class"),
                    "href": elem.get_attribute("href"),
                    "onclick": elem.get_attribute("onclick"),
                    "visible": elem.is_displayed(),
                    "enabled": elem.is_enabled(),
                    "location": elem.location,
                    "size": elem.size
                }
                button_data.append(info)
                
                if elem.is_displayed() and text:
                    logger.info(f"可见按钮 {i+1}: {info}")
                    
            except Exception as e:
                logger.error(f"分析按钮元素 {i} 时出错: {e}")
        
        # 保存到文件
        with open("button_elements_analysis.json", "w", encoding="utf-8") as f:
            json.dump(button_data, f, ensure_ascii=False, indent=2)
    
    def analyze_text_content(self):
        """分析文本内容"""
        logger.info("=" * 50)
        logger.info("分析文本内容...")
        logger.info("=" * 50)
        
        # 查找包含特定关键词的文本
        keywords = ['载重', '速度', '高度', '宽度', '深度', 'kg', 'm/s', 'mm', '下载', '绘图', '生成', '创建']
        
        text_data = []
        for keyword in keywords:
            try:
                elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{keyword}')]")
                logger.info(f"包含 '{keyword}' 的元素: {len(elements)} 个")
                
                for i, elem in enumerate(elements):
                    try:
                        text = elem.text.strip()
                        if text:
                            info = {
                                "keyword": keyword,
                                "index": i,
                                "tag": elem.tag_name,
                                "text": text,
                                "id": elem.get_attribute("id"),
                                "class": elem.get_attribute("class"),
                                "visible": elem.is_displayed(),
                                "location": elem.location
                            }
                            text_data.append(info)
                            
                            if elem.is_displayed():
                                logger.info(f"可见文本 '{keyword}' {i+1}: {text}")
                                
                    except Exception as e:
                        logger.error(f"分析文本元素时出错: {e}")
                        
            except Exception as e:
                logger.error(f"查找关键词 '{keyword}' 时出错: {e}")
        
        # 保存到文件
        with open("text_content_analysis.json", "w", encoding="utf-8") as f:
            json.dump(text_data, f, ensure_ascii=False, indent=2)
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            logger.info("浏览器已关闭")

def main():
    analyzer = PageStructureAnalyzer()
    try:
        if analyzer.setup_driver():
            analyzer.analyze_page_structure("ARISE")
            input("按Enter键关闭浏览器...")
    except Exception as e:
        logger.error(f"主程序运行失败: {e}")
    finally:
        analyzer.close()

if __name__ == "__main__":
    main() 