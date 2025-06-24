#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用requests分析奥的斯网站
"""

import requests
import time
from bs4 import BeautifulSoup
import json
import re

def analyze_otis_website():
    """分析奥的斯网站"""
    print("开始分析奥的斯网站...")
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # 访问主页
        print("访问奥的斯主页...")
        response = requests.get("https://www.otiscreate.com", headers=headers, timeout=15)
        print(f"主页状态码: {response.status_code}")
        
        # 访问产品查找器页面
        print("访问产品查找器页面...")
        response = requests.get("https://www.otiscreate.com/product-finder/zh/cn", headers=headers, timeout=15)
        print(f"产品查找器页面状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 保存页面内容
            with open("otis_page_requests.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("页面内容已保存到 otis_page_requests.html")
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有按钮
            buttons = soup.find_all('button')
            print(f"\n找到 {len(buttons)} 个按钮:")
            for i, button in enumerate(buttons[:10]):
                text = button.get_text(strip=True)
                if text:
                    print(f"  按钮 {i+1}: {text}")
            
            # 查找所有链接
            links = soup.find_all('a')
            print(f"\n找到 {len(links)} 个链接:")
            for i, link in enumerate(links[:10]):
                text = link.get_text(strip=True)
                href = link.get('href')
                if text:
                    print(f"  链接 {i+1}: {text} -> {href}")
            
            # 查找包含特定文本的元素
            text_patterns = ["电梯", "产品", "下载", "Download", "Product", "Elevator", "Create", "Design"]
            for pattern in text_patterns:
                elements = soup.find_all(text=re.compile(pattern, re.IGNORECASE))
                if elements:
                    print(f"\n包含 '{pattern}' 的元素: {len(elements)} 个")
                    for i, elem in enumerate(elements[:3]):
                        text = elem.strip()
                        if text and len(text) < 100:
                            print(f"  {text}")
            
            # 查找可能的API端点
            scripts = soup.find_all('script')
            api_endpoints = []
            for script in scripts:
                if script.string:
                    # 查找可能的API URL
                    urls = re.findall(r'https?://[^\s"\'<>]+', script.string)
                    for url in urls:
                        if 'api' in url.lower() or 'product' in url.lower():
                            api_endpoints.append(url)
            
            if api_endpoints:
                print(f"\n找到 {len(api_endpoints)} 个可能的API端点:")
                for endpoint in api_endpoints[:5]:
                    print(f"  {endpoint}")
            
            # 查找表单
            forms = soup.find_all('form')
            print(f"\n找到 {len(forms)} 个表单:")
            for i, form in enumerate(forms):
                action = form.get('action')
                method = form.get('method', 'GET')
                print(f"  表单 {i+1}: {method} -> {action}")
                
                # 查找表单中的输入字段
                inputs = form.find_all('input')
                for inp in inputs:
                    name = inp.get('name')
                    input_type = inp.get('type')
                    placeholder = inp.get('placeholder')
                    if name:
                        print(f"    输入: {name} ({input_type}) - {placeholder}")
            
            # 分析页面结构
            print("\n页面结构分析:")
            print(f"  标题: {soup.title.string if soup.title else '无标题'}")
            print(f"  主要div数量: {len(soup.find_all('div'))}")
            print(f"  主要section数量: {len(soup.find_all('section'))}")
            print(f"  主要article数量: {len(soup.find_all('article'))}")
            
            # 查找可能的Angular应用标识
            angular_indicators = []
            for tag in soup.find_all():
                if tag.get('ng-version') or tag.get('ng-app') or tag.get('ng-controller'):
                    angular_indicators.append(tag.name)
            
            if angular_indicators:
                print(f"  检测到Angular应用标识: {set(angular_indicators)}")
            
            # 查找JavaScript文件
            js_files = []
            for script in soup.find_all('script', src=True):
                js_files.append(script['src'])
            
            print(f"\n找到 {len(js_files)} 个JavaScript文件:")
            for js_file in js_files[:5]:
                print(f"  {js_file}")
            
        else:
            print(f"页面访问失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"分析过程中出现错误: {e}")

if __name__ == "__main__":
    analyze_otis_website() 