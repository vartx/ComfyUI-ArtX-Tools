"""
ComfyUI ArtX Tools Plugin
用于列出models目录和管理GitHub安装
"""

__version__ = "1.0.0"

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', '__version__']

# 插件信息
WEB_DIRECTORY = "./web"
__author__ = "ArtX"
__description__ = "ComfyUI插件：路径内容列表和GitHub安装器"
