#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试奥的斯网站结构
用于分析网站的元素和结构
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json

def test_website_structure():
    """测试网站结构"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # 启动浏览器
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("正在访问奥的斯网站...")
        driver.get("https://www.otiscreate.com/product-finder/zh/cn")
        
        # 等待页面加载
        time.sleep(10)
        
        print("页面标题:", driver.title)
        print("当前URL:", driver.current_url)
        
        # 保存页面源码
        with open("otis_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("页面源码已保存到 otis_page_source.html")
        
        # 查找所有按钮
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"\n找到 {len(buttons)} 个按钮:")
        for i, button in enumerate(buttons[:10]):  # 只显示前10个
            try:
                text = button.text.strip()
                if text:
                    print(f"  按钮 {i+1}: {text}")
            except:
                pass
        
        # 查找所有链接
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"\n找到 {len(links)} 个链接:")
        for i, link in enumerate(links[:10]):  # 只显示前10个
            try:
                text = link.text.strip()
                href = link.get_attribute("href")
                if text:
                    print(f"  链接 {i+1}: {text} -> {href}")
            except:
                pass
        
        # 查找所有输入框
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\n找到 {len(inputs)} 个输入框:")
        for i, input_elem in enumerate(inputs[:10]):  # 只显示前10个
            try:
                placeholder = input_elem.get_attribute("placeholder")
                name = input_elem.get_attribute("name")
                id_attr = input_elem.get_attribute("id")
                print(f"  输入框 {i+1}: placeholder='{placeholder}', name='{name}', id='{id_attr}'")
            except:
                pass
        
        # 查找包含特定文本的元素
        text_patterns = ["电梯", "产品", "下载", "Download", "Product", "Elevator"]
        for pattern in text_patterns:
            elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{pattern}')]")
            if elements:
                print(f"\n包含 '{pattern}' 的元素 ({len(elements)} 个):")
                for i, elem in enumerate(elements[:5]):  # 只显示前5个
                    try:
                        text = elem.text.strip()
                        tag = elem.tag_name
                        class_name = elem.get_attribute("class")
                        print(f"  {tag}.{class_name}: {text}")
                    except:
                        pass
        
        # 查找可能的下载按钮
        download_patterns = [
            "//*[contains(text(), '下载')]",
            "//*[contains(text(), 'Download')]",
            "//*[contains(@class, 'download')]",
            "//*[contains(@id, 'download')]",
            "//button[contains(@onclick, 'download')]",
            "//a[contains(@href, 'download')]"
        ]
        
        print("\n可能的下载按钮:")
        for pattern in download_patterns:
            elements = driver.find_elements(By.XPATH, pattern)
            if elements:
                print(f"  使用模式 '{pattern}' 找到 {len(elements)} 个元素")
                for i, elem in enumerate(elements[:3]):  # 只显示前3个
                    try:
                        text = elem.text.strip()
                        tag = elem.tag_name
                        print(f"    {tag}: {text}")
                    except:
                        pass
        
        print("\n测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    test_website_structure() 