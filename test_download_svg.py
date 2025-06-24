#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Download.svg图标按钮
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """设置Chrome浏览器"""
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 30)
    
    try:
        print("访问奥的斯网站...")
        driver.get("https://www.otiscreate.com/product-finder/zh/cn")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)
        
        print("点击ARISE解决方案按钮...")
        arise_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
            "//div[contains(., 'ARISE')]//ancestor::div[contains(@class, 'product')]//a[@id='create']")))
        driver.execute_script("arguments[0].click();", arise_button)
        time.sleep(10)
        
        print("搜索包含Download.svg的按钮...")
        
        # 搜索Download.svg图标
        download_svg_selectors = [
            "//img[contains(@src, 'Download.svg')]",
            "//img[contains(@src, '/assets/img/Download.svg')]",
            "//*[contains(@src, 'Download.svg')]"
        ]
        
        for selector in download_svg_selectors:
            try:
                images = driver.find_elements(By.XPATH, selector)
                print(f"\n使用选择器 {selector} 找到 {len(images)} 个Download.svg图标:")
                
                for i, img in enumerate(images):
                    try:
                        print(f"\n  图标 {i}:")
                        print(f"    src: {img.get_attribute('src')}")
                        print(f"    alt: {img.get_attribute('alt')}")
                        print(f"    可见: {img.is_displayed()}")
                        
                        # 查找父级按钮
                        parent_button = img.find_element(By.XPATH, "./ancestor::button[1]")
                        print(f"    父级按钮文本: '{parent_button.text}'")
                        print(f"    父级按钮类: {parent_button.get_attribute('class')}")
                        print(f"    父级按钮类型: {parent_button.get_attribute('type')}")
                        print(f"    父级按钮可见: {parent_button.is_displayed()}")
                        print(f"    父级按钮可点击: {parent_button.is_enabled()}")
                        
                        if "下载绘图" in parent_button.text:
                            print(f"    🎯 这就是'下载绘图'按钮！")
                            
                            # 尝试点击
                            try:
                                driver.execute_script("arguments[0].click();", parent_button)
                                print(f"    ✅ 成功点击下载绘图按钮！")
                                time.sleep(5)
                                return True
                            except Exception as e:
                                print(f"    ❌ 点击失败: {e}")
                        
                    except Exception as e:
                        print(f"    分析图标 {i} 时出错: {e}")
                        
            except Exception as e:
                print(f"使用选择器 {selector} 时出错: {e}")
        
        # 如果没找到，搜索所有按钮中包含Download.svg的
        print("\n搜索所有包含Download.svg的按钮...")
        buttons_with_download_svg = driver.find_elements(By.XPATH, "//button[.//img[contains(@src, 'Download.svg')]]")
        
        print(f"找到 {len(buttons_with_download_svg)} 个包含Download.svg的按钮:")
        for i, button in enumerate(buttons_with_download_svg):
            try:
                print(f"\n  按钮 {i}:")
                print(f"    文本: '{button.text}'")
                print(f"    类: {button.get_attribute('class')}")
                print(f"    类型: {button.get_attribute('type')}")
                print(f"    可见: {button.is_displayed()}")
                print(f"    HTML: {button.get_attribute('outerHTML')[:200]}")
                
                if "下载绘图" in button.text and button.is_displayed():
                    print(f"    🎯 找到下载绘图按钮！尝试点击...")
                    driver.execute_script("arguments[0].click();", button)
                    print(f"    ✅ 点击成功！")
                    time.sleep(5)
                    break
                    
            except Exception as e:
                print(f"    分析按钮 {i} 时出错: {e}")
        
        input("按回车键继续...")
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 