#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试产品选择功能
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

def test_product_selection():
    """测试产品选择功能"""
    
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
        
        # 测试查找 ARISE 产品
        logger.info("测试查找 ARISE 产品...")
        try:
            # 使用修复后的XPath
            product_xpath = "//div[contains(@class, 'product') and .//div[@class='product-name' and contains(text(), 'ARISE')]]"
            product_card = wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
            logger.info("✅ 成功找到 ARISE 产品卡片")
            
            # 查找解决方案链接
            solution_link_xpath = ".//div[contains(@class, 'action-buttons')]//div[contains(@class, 'action-items')]//a[@id='create']"
            solution_link = product_card.find_element(By.XPATH, solution_link_xpath)
            logger.info("✅ 成功找到 ARISE 的解决方案按钮")
            
            # 测试点击
            driver.execute_script("arguments[0].scrollIntoView(true);", solution_link)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", solution_link)
            logger.info("✅ 成功点击 ARISE 的解决方案按钮")
            
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"❌ ARISE 产品测试失败: {e}")
        
        # 测试查找 Gen3 MRL 产品
        logger.info("测试查找 Gen3 MRL 产品...")
        try:
            driver.get("https://www.otiscreate.com/product-finder/zh/cn")
            time.sleep(10)
            
            product_xpath = "//div[contains(@class, 'product') and .//div[@class='product-name' and contains(text(), 'Gen3 MRL')]]"
            product_card = wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
            logger.info("✅ 成功找到 Gen3 MRL 产品卡片")
            
            solution_link_xpath = ".//div[contains(@class, 'action-buttons')]//div[contains(@class, 'action-items')]//a[@id='create']"
            solution_link = product_card.find_element(By.XPATH, solution_link_xpath)
            logger.info("✅ 成功找到 Gen3 MRL 的解决方案按钮")
            
        except Exception as e:
            logger.error(f"❌ Gen3 MRL 产品测试失败: {e}")
        
        logger.info("🎉 产品选择功能测试完成！")
        
    except Exception as e:
        logger.error(f"测试过程中出错: {e}")
    finally:
        if driver:
            driver.quit()
            logger.info("浏览器已关闭")

if __name__ == "__main__":
    test_product_selection() 