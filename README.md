# ComfyUI ArtX Tools

一个简单实用的ComfyUI插件，提供models目录管理和GitHub安装功能。

## 功能特性

### 📁 Models目录列表
- 列出ComfyUI `models` 目录下的所有子目录
- 显示目录数量和路径信息
- 无需输入参数，直接运行

### 🚀 GitHub安装器
- 直接从GitHub URL安装ComfyUI插件或模型
- 支持安装到 `custom_nodes` 或 `models` 目录
- 自动检测依赖文件和说明文档
- 提供详细的安装反馈

## 安装方法

1. 将此插件下载到ComfyUI的 `custom_nodes` 目录
2. 重启ComfyUI
3. 在节点菜单中找到 "ArtX Tools" 分类

## 使用方法

### Models目录列表节点
1. 添加 "📁 Models目录列表" 节点
2. 连接输出到任何能显示字符串的节点
3. 运行工作流即可查看models目录结构

### GitHub安装器节点
1. 添加 "🚀 GitHub安装器" 节点
2. 输入GitHub仓库URL（如：`https://github.com/abculr/repository-name`）
3. 选择安装类型：
   - `custom_nodes`: 安装ComfyUI插件
   - `models`: 安装模型文件
4. 运行节点开始安装

## 依赖要求

- Python >= 3.8
- Git（用于GitHub安装功能）
- ComfyUI

## 注意事项

- GitHub安装需要网络连接
- 安装新插件后需要重启ComfyUI
- 确保有足够的磁盘空间
- 某些仓库可能需要额外的依赖安装

## 许可证

MIT License
