#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试下载按钮脚本 - 详细分析页面上的所有按钮
"""

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """设置Chrome浏览器"""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 下载设置
    download_dir = os.path.join(os.getcwd(), "otis_solutions")
    os.makedirs(download_dir, exist_ok=True)
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def analyze_all_buttons(driver, stage_name):
    """分析页面上的所有按钮"""
    print(f"\n=== 分析阶段: {stage_name} ===")
    
    # 查找所有按钮
    buttons = driver.find_elements(By.TAG_NAME, "button")
    links = driver.find_elements(By.TAG_NAME, "a")
    inputs = driver.find_elements(By.XPATH, "//input[@type='submit' or @type='button']")
    
    all_elements = []
    
    # 分析按钮
    for i, button in enumerate(buttons):
        try:
            element_info = {
                "type": "button",
                "index": i,
                "text": button.text.strip(),
                "class": button.get_attribute("class"),
                "id": button.get_attribute("id"),
                "type_attr": button.get_attribute("type"),
                "data_hover": button.get_attribute("data-hover"),
                "visible": button.is_displayed(),
                "enabled": button.is_enabled(),
                "innerHTML": button.get_attribute("innerHTML")[:200] if button.get_attribute("innerHTML") else ""
            }
            all_elements.append(element_info)
            
            if "下载" in element_info["text"] or "download" in element_info["class"].lower():
                print(f"🎯 发现下载相关按钮 {i}: {element_info}")
                
        except Exception as e:
            print(f"分析按钮 {i} 时出错: {e}")
    
    # 分析链接
    for i, link in enumerate(links):
        try:
            element_info = {
                "type": "link", 
                "index": i,
                "text": link.text.strip(),
                "class": link.get_attribute("class"),
                "id": link.get_attribute("id"),
                "href": link.get_attribute("href"),
                "visible": link.is_displayed(),
                "innerHTML": link.get_attribute("innerHTML")[:200] if link.get_attribute("innerHTML") else ""
            }
            all_elements.append(element_info)
            
            if "下载" in element_info["text"] or "download" in element_info["class"].lower():
                print(f"🎯 发现下载相关链接 {i}: {element_info}")
                
        except Exception as e:
            print(f"分析链接 {i} 时出错: {e}")
    
    # 分析输入框
    for i, input_elem in enumerate(inputs):
        try:
            element_info = {
                "type": "input",
                "index": i,
                "value": input_elem.get_attribute("value"),
                "class": input_elem.get_attribute("class"),
                "id": input_elem.get_attribute("id"),
                "type_attr": input_elem.get_attribute("type"),
                "visible": input_elem.is_displayed(),
                "enabled": input_elem.is_enabled()
            }
            all_elements.append(element_info)
            
            if "下载" in (element_info["value"] or ""):
                print(f"🎯 发现下载相关输入 {i}: {element_info}")
                
        except Exception as e:
            print(f"分析输入 {i} 时出错: {e}")
    
    # 保存详细信息
    with open(f"button_analysis_{stage_name}.json", "w", encoding="utf-8") as f:
        json.dump(all_elements, f, ensure_ascii=False, indent=2)
    
    print(f"总共找到 {len(buttons)} 个按钮, {len(links)} 个链接, {len(inputs)} 个输入")
    return all_elements

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 30)
    
    try:
        print("访问奥的斯网站...")
        driver.get("https://www.otiscreate.com/product-finder/zh/cn")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)
        
        # 分析初始页面
        print("=== 分析初始页面的按钮 ===")
        analyze_all_buttons(driver, "initial")
        driver.save_screenshot("debug_initial_page.png")
        
        # 寻找ARISE产品的解决方案按钮
        print("\n寻找ARISE产品...")
        arise_solution_button = None
        
        # 多种方式寻找ARISE解决方案按钮
        selectors = [
            "//div[contains(@class, 'product')]//div[contains(text(), 'ARISE')]//ancestor::div[contains(@class, 'product')]//a[@id='create']",
            "//div[contains(., 'ARISE')]//following-sibling::*//a[@id='create']",
            "//div[@class='product-name' and text()='ARISE']//ancestor::div[contains(@class, 'product')]//a[@id='create']"
        ]
        
        for selector in selectors:
            try:
                arise_solution_button = driver.find_element(By.XPATH, selector)
                print(f"✅ 找到ARISE解决方案按钮: {selector}")
                break
            except:
                continue
        
        if not arise_solution_button:
            print("❌ 未找到ARISE解决方案按钮")
            return
        
        # 滚动到按钮并点击
        print("滚动到ARISE解决方案按钮...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", arise_solution_button)
        time.sleep(2)
        
        print("点击ARISE解决方案按钮...")
        driver.execute_script("arguments[0].click();", arise_solution_button)
        time.sleep(15)  # 等待15秒让页面充分加载
        
        # 分析点击后的页面
        print("\n=== 分析点击解决方案后的页面 ===")
        analyze_all_buttons(driver, "after_solution_click")
        driver.save_screenshot("debug_after_solution_click.png")
        
        # 检查iframe
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"\n找到 {len(iframes)} 个iframe")
        
        for i, iframe in enumerate(iframes):
            try:
                print(f"\n--- 切换到iframe {i} ---")
                driver.switch_to.frame(iframe)
                analyze_all_buttons(driver, f"iframe_{i}")
                driver.save_screenshot(f"debug_iframe_{i}.png")
                driver.switch_to.default_content()
            except Exception as e:
                print(f"处理iframe {i} 时出错: {e}")
                driver.switch_to.default_content()
        
        # 尝试寻找任何包含"下载绘图"的元素
        print("\n=== 搜索包含'下载绘图'的所有元素 ===")
        download_elements = driver.find_elements(By.XPATH, "//*[contains(., '下载绘图')]")
        for i, elem in enumerate(download_elements):
            try:
                print(f"元素 {i}: 标签={elem.tag_name}, 文本='{elem.text}', 类={elem.get_attribute('class')}")
                print(f"  HTML: {elem.get_attribute('outerHTML')[:300]}")
            except Exception as e:
                print(f"分析下载绘图元素 {i} 时出错: {e}")
        
        input("按回车键继续（这样您可以手动检查页面）...")
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 