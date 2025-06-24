#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量下载奥的斯电梯产品图 (V3.0)
调用修复版的增强型下载器
"""
import json
import os
import time
import logging
from enhanced_auto_downloader import EnhancedOtisDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BatchOtisDownloader:
    def __init__(self, config_file="product_config.json"):
        self.config = self.load_config(config_file)
        self.downloader = None

    def load_config(self, config_file):
        """加载JSON配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"配置文件未找到: {config_file}")
        except json.JSONDecodeError:
            logger.error(f"配置文件格式错误: {config_file}")
        return None

    def run_batch_download(self, product_indices=None):
        """运行批量下载任务"""
        if not self.config:
            logger.error("配置加载失败，无法开始下载。")
            return

        products_to_download = self.config.get("products", [])
        if product_indices is not None:
            products_to_download = [products_to_download[i] for i in product_indices if 0 <= i < len(products_to_download)]

        if not products_to_download:
            logger.warning("没有要下载的产品。")
            return
            
        logger.info(f"===== 开始批量下载 {len(products_to_download)} 个产品 =====")
        
        settings = self.config.get("download_settings", {})
        download_dir = settings.get("download_dir", "otis_products")
        wait_time = settings.get("wait_time_between_products", 10)
        max_retries = settings.get("retry_count", 2)

        self.downloader = EnhancedOtisDownloader(download_dir=download_dir)
        
        success_count = 0
        fail_count = 0

        try:
            for i, product_config in enumerate(products_to_download, 1):
                product_name = product_config.get("name", f"未知产品_{i}")
                specs = product_config.get("specs", {})
                
                logger.info(f"--- 处理产品 {i}/{len(products_to_download)}: {product_name} ---")
                
                is_successful = False
                for attempt in range(max_retries + 1):
                    try:
                        self.downloader.setup_driver() # 为每个任务（或重试）启动新的浏览器实例
                        if self.downloader.run_automation(product_name, specs):
                            success_count += 1
                            is_successful = True
                            break # 成功，跳出重试循环
                        else:
                            logger.warning(f"产品 '{product_name}' 下载尝试 {attempt + 1}/{max_retries + 1} 失败。")
                    except Exception as e:
                        logger.error(f"产品 '{product_name}' 下载尝试 {attempt + 1}/{max_retries + 1} 出现严重错误: {e}")
                    finally:
                        self.downloader.close() # 确保每次尝试后都关闭浏览器

                    if attempt < max_retries:
                        logger.info(f"等待 {wait_time}s 后重试...")
                        time.sleep(wait_time)

                if not is_successful:
                    fail_count += 1
                    logger.error(f"产品 '{product_name}' 在所有尝试后均告失败。")

                if i < len(products_to_download):
                    logger.info(f"等待 {wait_time}s 后开始下一个产品...")
                    time.sleep(wait_time)

        finally:
            logger.info("===== 批量下载任务结束 =====")
            logger.info(f"成功: {success_count}, 失败: {fail_count}, 总计: {len(products_to_download)}")
            if self.downloader:
                self.downloader.close()

def main():
    """交互式主函数"""
    batch_downloader = BatchOtisDownloader()
    if not batch_downloader.config:
        return

    products = batch_downloader.config.get("products", [])
    print("--- 奥的斯产品批量下载器 ---")
    print(f"在配置文件中找到 {len(products)} 个产品:")
    for i, p in enumerate(products):
        print(f"  [{i}] {p.get('name')}")
    
    print("\n请选择操作:")
    print("  1. 下载所有产品")
    print("  2. 下载指定产品 (输入索引)")
    choice = input("请输入你的选择 (1/2): ").strip()
    
    if choice == '1':
        batch_downloader.run_batch_download()
    elif choice == '2':
        idx_input = input("请输入产品索引 (用逗号分隔, 例如: 0,2): ").strip()
        try:
            indices = [int(i.strip()) for i in idx_input.split(',')]
            batch_downloader.run_batch_download(indices)
        except ValueError:
            logger.error("无效的索引格式。请输入数字并用逗号分隔。")
    else:
        print("无效的选择。")

if __name__ == "__main__":
    main() 