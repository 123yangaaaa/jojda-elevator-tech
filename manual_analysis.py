#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动分析奥的斯网站的工具
"""

import requests
import time
from bs4 import BeautifulSoup
import json
import re

def manual_analysis():
    """手动分析奥的斯网站"""
    print("=== 奥的斯电梯产品查找器网站分析 ===")
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print("\n1. 访问产品查找器页面...")
        response = requests.get("https://www.otiscreate.com/product-finder/zh/cn", headers=headers, timeout=15)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ 页面访问成功")
            
            # 保存页面内容
            with open("manual_analysis.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("✓ 页面内容已保存到 manual_analysis.html")
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print("\n2. 页面基本信息:")
            print(f"   标题: {soup.title.string if soup.title else '无标题'}")
            print(f"   字符数: {len(response.text)}")
            
            print("\n3. JavaScript文件分析:")
            scripts = soup.find_all('script', src=True)
            for i, script in enumerate(scripts):
                src = script['src']
                print(f"   {i+1}. {src}")
                if 'main' in src:
                    print(f"      → 这可能是主要的应用文件")
            
            print("\n4. 页面结构分析:")
            print(f"   <iaa-root> 标签: {'是' if soup.find('iaa-root') else '否'}")
            print(f"   Angular 应用: {'是' if soup.find(attrs={'ng-version'}) else '否'}")
            
            print("\n5. 可能的API端点:")
            # 查找可能的API URL
            api_patterns = [
                r'https?://[^\s"\'<>]*api[^\s"\'<>]*',
                r'https?://[^\s"\'<>]*product[^\s"\'<>]*',
                r'https?://[^\s"\'<>]*elevator[^\s"\'<>]*'
            ]
            
            found_apis = []
            for pattern in api_patterns:
                urls = re.findall(pattern, response.text, re.IGNORECASE)
                found_apis.extend(urls)
            
            if found_apis:
                unique_apis = list(set(found_apis))
                for i, api in enumerate(unique_apis[:5]):
                    print(f"   {i+1}. {api}")
            else:
                print("   未找到明显的API端点")
            
            print("\n6. 下载策略分析:")
            print("   基于分析结果，建议的下载策略:")
            print("   ✓ 使用Selenium WebDriver（因为这是Angular应用）")
            print("   ✓ 等待页面完全加载（15-20秒）")
            print("   ✓ 查找动态生成的产品元素")
            print("   ✓ 模拟用户交互填写规格")
            print("   ✓ 点击下载按钮获取图纸")
            
            print("\n7. 技术挑战:")
            print("   ⚠️ 需要匹配的ChromeDriver版本")
            print("   ⚠️ 页面内容动态加载")
            print("   ⚠️ 可能需要处理登录")
            print("   ⚠️ 下载频率限制")
            
            print("\n8. 解决方案建议:")
            print("   1. 手动下载匹配的ChromeDriver")
            print("   2. 使用无头浏览器模式")
            print("   3. 添加随机延迟避免检测")
            print("   4. 实现错误重试机制")
            
        else:
            print(f"✗ 页面访问失败: {response.status_code}")
            
    except Exception as e:
        print(f"✗ 分析过程中出现错误: {e}")

if __name__ == "__main__":
    manual_analysis() 