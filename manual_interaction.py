#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动交互脚本 - 允许用户手动操作页面找到下载绘图按钮
"""

import os
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
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 30)
    
    try:
        print("正在访问奥的斯网站...")
        driver.get("https://www.otiscreate.com/product-finder/zh/cn")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)
        
        print("寻找ARISE产品的解决方案按钮...")
        arise_solution_selectors = [
            "//div[contains(@class, 'product')]//div[contains(text(), 'ARISE')]//ancestor::div[contains(@class, 'product')]//a[@id='create']",
            "//div[contains(., 'ARISE')]//following-sibling::*//a[@id='create']",
            "//div[@class='product-name' and text()='ARISE']//ancestor::div[contains(@class, 'product')]//a[@id='create']"
        ]
        
        arise_solution_button = None
        for selector in arise_solution_selectors:
            try:
                arise_solution_button = driver.find_element(By.XPATH, selector)
                print(f"找到ARISE解决方案按钮: {selector}")
                break
            except:
                continue
        
        if not arise_solution_button:
            print("未找到ARISE解决方案按钮！")
            input("请您手动找到并点击ARISE的解决方案按钮，然后按回车键继续...")
        else:
            print("滚动到ARISE解决方案按钮...")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", arise_solution_button)
            time.sleep(2)
            
            print("点击ARISE解决方案按钮...")
            driver.execute_script("arguments[0].click();", arise_solution_button)
            print("已点击解决方案按钮！")
        
        print("\n" + "="*50)
        print("请您现在手动操作页面：")
        print("1. 如果看到任何表单，请填写相关信息")
        print("2. 寻找'下载绘图'按钮")
        print("3. 当您找到'下载绘图'按钮时，请在控制台输入'found'")
        print("4. 如果需要我点击某个按钮，请输入按钮的文本内容")
        print("5. 输入'quit'退出")
        print("="*50)
        
        while True:
            user_input = input("\n请输入指令 (found/quit/按钮文本): ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'found':
                # 尝试查找并分析"下载绘图"按钮
                print("正在搜索'下载绘图'按钮...")
                download_elements = driver.find_elements(By.XPATH, "//*[contains(., '下载绘图')]")
                
                if download_elements:
                    for i, elem in enumerate(download_elements):
                        try:
                            print(f"\n找到下载绘图元素 {i}:")
                            print(f"  标签: {elem.tag_name}")
                            print(f"  文本: '{elem.text}'")
                            print(f"  类名: {elem.get_attribute('class')}")
                            print(f"  ID: {elem.get_attribute('id')}")
                            print(f"  HTML: {elem.get_attribute('outerHTML')[:300]}")
                            print(f"  可见: {elem.is_displayed()}")
                            print(f"  可点击: {elem.is_enabled()}")
                            
                            if elem.is_displayed() and elem.is_enabled():
                                try_click = input(f"是否尝试点击元素 {i}? (y/n): ")
                                if try_click.lower() == 'y':
                                    try:
                                        driver.execute_script("arguments[0].click();", elem)
                                        print(f"✅ 已点击元素 {i}")
                                        time.sleep(3)
                                        # 检查是否有文件下载
                                        print("请检查是否开始下载文件...")
                                    except Exception as e:
                                        print(f"❌ 点击失败: {e}")
                        except Exception as e:
                            print(f"分析元素 {i} 时出错: {e}")
                else:
                    print("❌ 未找到包含'下载绘图'的元素")
                    
                    # 搜索所有可能的下载按钮
                    print("\n搜索所有可能的下载按钮...")
                    all_buttons = driver.find_elements(By.TAG_NAME, "button")
                    download_buttons = []
                    
                    for button in all_buttons:
                        try:
                            text = button.text.strip()
                            class_name = button.get_attribute('class') or ""
                            if ('下载' in text or 'download' in class_name.lower() or 
                                'btn-download' in class_name):
                                download_buttons.append(button)
                                
                        except:
                            continue
                    
                    if download_buttons:
                        print(f"找到 {len(download_buttons)} 个可能的下载按钮:")
                        for i, btn in enumerate(download_buttons):
                            try:
                                print(f"  按钮 {i}: '{btn.text}' (类: {btn.get_attribute('class')})")
                            except:
                                print(f"  按钮 {i}: 无法读取信息")
                    else:
                        print("❌ 未找到任何下载相关按钮")
            
            else:
                # 尝试点击用户指定的按钮
                try:
                    button = driver.find_element(By.XPATH, f"//*[contains(text(), '{user_input}')]")
                    driver.execute_script("arguments[0].click();", button)
                    print(f"✅ 已点击包含文本'{user_input}'的元素")
                    time.sleep(2)
                except Exception as e:
                    print(f"❌ 找不到或无法点击包含'{user_input}'的元素: {e}")
    
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        input("按回车键关闭浏览器...")
        driver.quit()

if __name__ == "__main__":
    main() 