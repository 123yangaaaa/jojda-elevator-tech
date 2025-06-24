#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试脚本
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def test_arise_selection():
    """测试ARISE产品选择"""
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        # 启动浏览器
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 30)
        
        print("访问奥的斯网站...")
        driver.get("https://www.otiscreate.com/product-finder/zh/cn")
        time.sleep(10)
        
        # 查找ARISE产品
        print("查找ARISE产品...")
        product_xpath = "//div[contains(@class, 'product') and .//div[@class='product-name' and contains(text(), 'ARISE')]]"
        product_card = wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
        print("✅ 找到ARISE产品卡片")
        
        # 查找解决方案按钮
        print("查找解决方案按钮...")
        solution_xpath = ".//div[contains(@class, 'action-buttons')]//div[contains(@class, 'action-items')]//a[@id='create']"
        solution_link = product_card.find_element(By.XPATH, solution_xpath)
        print("✅ 找到解决方案按钮")
        
        # 点击解决方案按钮
        print("点击解决方案按钮...")
        solution_link.click()
        print("✅ 成功点击解决方案按钮")
        
        time.sleep(5)
        print("🎉 测试成功完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    test_arise_selection() 