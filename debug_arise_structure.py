#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门调试ARISE产品的HTML结构
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

def debug_arise_structure():
    """调试ARISE产品的HTML结构"""
    
    # 设置Chrome选项
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
        
        # 等待页面加载
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(10)
        
        # 查找ARISE产品卡片
        logger.info("查找ARISE产品卡片...")
        product_xpath = "//div[contains(@class, 'product') and .//div[@class='product-name' and contains(text(), 'ARISE')]]"
        product_card = wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
        logger.info("✅ 找到ARISE产品卡片")
        
        # 获取产品卡片的完整HTML
        card_html = product_card.get_attribute('outerHTML')
        logger.info("产品卡片HTML结构:")
        print("=" * 80)
        print(card_html)
        print("=" * 80)
        
        # 尝试不同的选择器
        selectors_to_try = [
            ".//div[@class='action-buttons']//a[@id='create']",
            ".//div[contains(@class, 'action-buttons')]//a[@id='create']",
            ".//div[@class='action-buttons']//div[@class='action-items']//a[@id='create']",
            ".//div[contains(@class, 'action-buttons')]//div[@class='action-items']//a[@id='create']",
            ".//div[contains(@class, 'action-buttons')]//div[contains(@class, 'action-items')]//a[@id='create']",
            ".//a[@id='create']",
            ".//a[contains(@class, 'action-link') and @id='create']"
        ]
        
        for i, selector in enumerate(selectors_to_try, 1):
            try:
                element = product_card.find_element(By.XPATH, selector)
                logger.info(f"✅ 选择器 {i} 成功: {selector}")
                logger.info(f"   元素HTML: {element.get_attribute('outerHTML')}")
                break
            except:
                logger.info(f"❌ 选择器 {i} 失败: {selector}")
        
        # 查找所有链接
        all_links = product_card.find_elements(By.TAG_NAME, "a")
        logger.info(f"产品卡片中找到 {len(all_links)} 个链接:")
        for i, link in enumerate(all_links):
            href = link.get_attribute('href')
            id_attr = link.get_attribute('id')
            class_attr = link.get_attribute('class')
            text = link.text.strip()
            logger.info(f"  链接 {i+1}: id='{id_attr}', class='{class_attr}', text='{text}', href='{href}'")
        
    except Exception as e:
        logger.error(f"调试过程中出错: {e}")
    finally:
        if driver:
            driver.quit()
            logger.info("浏览器已关闭")

if __name__ == "__main__":
    debug_arise_structure() 