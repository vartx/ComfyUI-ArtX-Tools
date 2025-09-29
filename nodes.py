import os
import json
import subprocess
import shutil
import tempfile
from pathlib import Path
import folder_paths


class ModelsListNode:
    """列出ComfyUI models目录下的所有子目录"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {}
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("models_list",)
    FUNCTION = "list_models"
    CATEGORY = "ArtX Tools"
    
    def list_models(self):
        try:
            # 获取ComfyUI的models路径
            models_path = folder_paths.models_dir
            
            if not os.path.exists(models_path):
                return (f"Models目录不存在: {models_path}",)
            
            # 列出所有子目录
            directories = []
            for item in os.listdir(models_path):
                item_path = os.path.join(models_path, item)
                if os.path.isdir(item_path):
                    directories.append(item)
            
            directories.sort()  # 按字母顺序排序
            
            if not directories:
                return ("Models目录为空",)
            
            # 格式化输出
            result = f"Models目录 ({models_path}) 包含以下子目录:\n"
            result += "\n".join([f"- {dir_name}" for dir_name in directories])
            result += f"\n\n总计: {len(directories)} 个目录"
            
            return (result,)
            
        except Exception as e:
            return (f"列出models目录时出错: {str(e)}",)


class GitHubInstallerNode:
    """从GitHub URL安装ComfyUI插件或模型"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "github_url": ("STRING", {
                    "default": "https://github.com/abculr/repository-name",
                    "multiline": False
                }),
                "install_type": (["custom_nodes", "models"], {
                    "default": "custom_nodes"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("install_result",)
    FUNCTION = "install_from_github"
    CATEGORY = "ArtX Tools"
    
    def install_from_github(self, github_url, install_type):
        try:
            # 验证GitHub URL格式
            if not github_url.startswith("https://github.com/"):
                return ("错误：请提供有效的GitHub URL (https://github.com/...)",)
            
            # 提取仓库信息
            url_parts = github_url.replace("https://github.com/", "").split("/")
            if len(url_parts) < 2:
                return ("错误：GitHub URL格式不正确",)
            
            owner = url_parts[0]
            repo = url_parts[1]
            
            # 确定安装目录
            if install_type == "custom_nodes":
                base_path = os.path.join(folder_paths.base_path, "custom_nodes")
            else:  # models
                base_path = folder_paths.models_dir
            
            install_path = os.path.join(base_path, repo)
            
            # 检查目录是否已存在
            if os.path.exists(install_path):
                return (f"目录已存在: {install_path}\n如需重新安装，请先删除该目录",)
            
            # 克隆仓库
            result = f"开始从 {github_url} 安装到 {install_type}...\n"
            
            try:
                # 使用git clone
                cmd = ["git", "clone", github_url, install_path]
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if process.returncode == 0:
                    result += f"✅ 成功克隆到: {install_path}\n"
                    
                    # 检查是否有requirements.txt或pyproject.toml
                    req_files = [
                        os.path.join(install_path, "requirements.txt"),
                        os.path.join(install_path, "pyproject.toml")
                    ]
                    
                    for req_file in req_files:
                        if os.path.exists(req_file):
                            result += f"📋 发现依赖文件: {os.path.basename(req_file)}\n"
                            result += "提示：可能需要手动安装依赖\n"
                            break
                    
                    # 检查README
                    readme_files = [
                        os.path.join(install_path, "README.md"),
                        os.path.join(install_path, "readme.md"),
                        os.path.join(install_path, "README.txt")
                    ]
                    
                    for readme_file in readme_files:
                        if os.path.exists(readme_file):
                            result += f"📖 发现说明文件: {os.path.basename(readme_file)}\n"
                            break
                    
                    result += f"\n🎉 安装完成！重启ComfyUI以加载新插件。"
                    
                else:
                    error_msg = process.stderr if process.stderr else "未知错误"
                    result += f"❌ 克隆失败: {error_msg}"
                    
            except subprocess.TimeoutExpired:
                result += "❌ 安装超时（5分钟），请检查网络连接"
            except FileNotFoundError:
                result += "❌ 未找到git命令，请确保已安装git"
            except Exception as e:
                result += f"❌ 安装过程中出错: {str(e)}"
            
            return (result,)
            
        except Exception as e:
            return (f"GitHub安装器出错: {str(e)}",)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "ModelsListNode": ModelsListNode,
    "GitHubInstallerNode": GitHubInstallerNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ModelsListNode": "📁 Models目录列表",
    "GitHubInstallerNode": "🚀 GitHub安装器",
}
