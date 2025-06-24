#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试规格填写页面的HTML结构
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_specs_page():
    """调试规格填写页面的HTML结构"""
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = None
    try:
        # 启动浏览器
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 30)
        
        logger.info("访问奥的斯网站...")
        driver.get("https://www.otiscreate.com/product-finder/zh/cn")
        time.sleep(10)
        
        # 找到ARISE产品并点击解决方案
        logger.info("查找ARISE产品...")
        product_xpath = "//div[contains(@class, 'product') and .//div[@class='product-name' and contains(text(), 'ARISE')]]"
        product_card = wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
        
        # 点击解决方案按钮
        solution_xpath = ".//div[contains(@class, 'action-buttons')]//div[contains(@class, 'action-items')]//a[@id='create']"
        solution_link = product_card.find_element(By.XPATH, solution_xpath)
        solution_link.click()
        logger.info("✅ 成功点击解决方案按钮")
        
        # 等待规格页面加载
        time.sleep(10)
        
        # 保存当前页面HTML
        page_source = driver.page_source
        with open("specs_page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        logger.info("规格页面HTML已保存到 specs_page_source.html")
        
        # 截图
        driver.save_screenshot("specs_page_screenshot.png")
        logger.info("规格页面截图已保存到 specs_page_screenshot.png")
        
        # 分析页面中的所有输入框
        logger.info("分析页面中的输入框...")
        input_elements = driver.find_elements(By.TAG_NAME, "input")
        logger.info(f"找到 {len(input_elements)} 个输入框:")
        
        for i, input_elem in enumerate(input_elements):
            try:
                input_type = input_elem.get_attribute('type')
                input_name = input_elem.get_attribute('name')
                input_id = input_elem.get_attribute('id')
                input_placeholder = input_elem.get_attribute('placeholder')
                input_value = input_elem.get_attribute('value')
                
                # 尝试找到相关的标签
                label_text = ""
                try:
                    # 通过for属性找标签
                    if input_id:
                        label = driver.find_element(By.XPATH, f"//label[@for='{input_id}']")
                        label_text = label.text.strip()
                except:
                    try:
                        # 通过父元素找标签
                        parent = input_elem.find_element(By.XPATH, "./..")
                        labels = parent.find_elements(By.TAG_NAME, "label")
                        if labels:
                            label_text = labels[0].text.strip()
                    except:
                        pass
                
                logger.info(f"  输入框 {i+1}:")
                logger.info(f"    类型: {input_type}")
                logger.info(f"    名称: {input_name}")
                logger.info(f"    ID: {input_id}")
                logger.info(f"    占位符: {input_placeholder}")
                logger.info(f"    当前值: {input_value}")
                logger.info(f"    关联标签: {label_text}")
                logger.info("    ---")
                
            except Exception as e:
                logger.error(f"分析输入框 {i+1} 时出错: {e}")
        
        # 分析页面中的所有按钮
        logger.info("分析页面中的按钮...")
        button_elements = driver.find_elements(By.TAG_NAME, "button")
        logger.info(f"找到 {len(button_elements)} 个按钮:")
        
        for i, button in enumerate(button_elements):
            try:
                button_text = button.text.strip()
                button_id = button.get_attribute('id')
                button_class = button.get_attribute('class')
                button_type = button.get_attribute('type')
                
                logger.info(f"  按钮 {i+1}:")
                logger.info(f"    文本: '{button_text}'")
                logger.info(f"    ID: {button_id}")
                logger.info(f"    类名: {button_class}")
                logger.info(f"    类型: {button_type}")
                logger.info("    ---")
                
            except Exception as e:
                logger.error(f"分析按钮 {i+1} 时出错: {e}")
        
        # 查找所有包含"下载"、"绘图"等关键词的元素
        logger.info("查找下载相关的元素...")
        download_keywords = ["下载", "绘图", "download", "drawing", "图纸"]
        
        for keyword in download_keywords:
            try:
                elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{keyword}')]")
                if elements:
                    logger.info(f"包含 '{keyword}' 的元素:")
                    for elem in elements:
                        logger.info(f"  标签: {elem.tag_name}, 文本: '{elem.text.strip()}', 类名: '{elem.get_attribute('class')}'")
            except Exception as e:
                logger.error(f"查找关键词 '{keyword}' 时出错: {e}")
        
    except Exception as e:
        logger.error(f"调试过程中出错: {e}")
    finally:
        if driver:
            input("按Enter键关闭浏览器...")
            driver.quit()
            logger.info("浏览器已关闭")

if __name__ == "__main__":
    debug_specs_page() 