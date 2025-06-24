#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试配置文件和下载器功能
"""

import json
import os
from batch_downloader import BatchOtisDownloader

def test_config_file():
    """测试配置文件"""
    print("=" * 50)
    print("测试配置文件")
    print("=" * 50)
    
    # 检查配置文件是否存在
    if not os.path.exists("product_config.json"):
        print("❌ 配置文件 product_config.json 不存在")
        return False
    
    # 尝试加载配置文件
    try:
        with open("product_config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✅ 配置文件加载成功")
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        return False
    
    # 检查配置结构
    if "products" not in config:
        print("❌ 配置文件中缺少 'products' 字段")
        return False
    
    if "download_settings" not in config:
        print("❌ 配置文件中缺少 'download_settings' 字段")
        return False
    
    print("✅ 配置文件结构正确")
    
    # 显示产品信息
    products = config["products"]
    print(f"📦 找到 {len(products)} 个产品配置:")
    
    for i, product in enumerate(products):
        name = product.get("name", "未知产品")
        product_type = product.get("product_type", "电梯")
        specs = product.get("specs", {})
        
        print(f"  {i}: {name} ({product_type})")
        for key, value in specs.items():
            print(f"    {key}: {value}")
        print()
    
    return True

def test_batch_downloader():
    """测试批量下载器"""
    print("=" * 50)
    print("测试批量下载器")
    print("=" * 50)
    
    try:
        batch_downloader = BatchOtisDownloader()
        print("✅ 批量下载器创建成功")
        
        # 测试列出产品
        print("\n📋 产品列表:")
        batch_downloader.list_products()
        
        return True
    except Exception as e:
        print(f"❌ 批量下载器测试失败: {e}")
        return False

def test_dependencies():
    """测试依赖包"""
    print("=" * 50)
    print("测试依赖包")
    print("=" * 50)
    
    try:
        import selenium
        print("✅ selenium 已安装")
    except ImportError:
        print("❌ selenium 未安装，请运行: pip install selenium")
        return False
    
    try:
        import webdriver_manager
        print("✅ webdriver-manager 已安装")
    except ImportError:
        print("❌ webdriver-manager 未安装，请运行: pip install webdriver-manager")
        return False
    
    return True

def main():
    """主测试函数"""
    print("🚀 开始测试奥的斯下载器")
    print()
    
    # 测试依赖包
    deps_ok = test_dependencies()
    print()
    
    # 测试配置文件
    config_ok = test_config_file()
    print()
    
    # 测试批量下载器
    downloader_ok = test_batch_downloader()
    print()
    
    # 总结
    print("=" * 50)
    print("测试总结")
    print("=" * 50)
    
    if deps_ok and config_ok and downloader_ok:
        print("🎉 所有测试通过！下载器可以正常使用")
        print()
        print("使用方法:")
        print("1. 运行单个产品下载: python enhanced_auto_downloader.py")
        print("2. 运行批量下载: python batch_downloader.py")
        print("3. 使用启动脚本: start_downloader.bat")
    else:
        print("❌ 部分测试失败，请检查上述错误信息")
    
    print()
    input("按回车键退出...")

if __name__ == "__main__":
    main() 