import os
import json
import subprocess
import shutil
import tempfile
from pathlib import Path
import folder_paths


class PathListNode:
    """列出ComfyUI相对路径下的所有目录和文件"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "relative_path": ("STRING", {
                    "default": "models",
                    "multiline": False
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path_content",)
    FUNCTION = "list_path_content"
    CATEGORY = "ArtX Tools"
    OUTPUT_NODE = True
    
    def list_path_content(self, relative_path):
        try:
            print(f"[ArtX Tools] 开始处理路径: {relative_path}")
            
            # 获取ComfyUI基础路径
            base_path = folder_paths.base_path
            print(f"[ArtX Tools] ComfyUI基础路径: {base_path}")
            
            # 构建完整路径
            full_path = os.path.join(base_path, relative_path)
            print(f"[ArtX Tools] 完整路径: {full_path}")
            
            if not os.path.exists(full_path):
                error_msg = f"路径不存在: {full_path}"
                print(f"[ArtX Tools] 错误: {error_msg}")
                return (error_msg,)
            
            if not os.path.isdir(full_path):
                error_msg = f"路径不是目录: {full_path}"
                print(f"[ArtX Tools] 错误: {error_msg}")
                return (error_msg,)
            
            # 列出所有内容
            directories = []
            files = []
            
            print(f"[ArtX Tools] 开始扫描目录内容...")
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                if os.path.isdir(item_path):
                    directories.append(item)
                    print(f"[ArtX Tools] 发现目录: {item}")
                else:
                    files.append(item)
                    print(f"[ArtX Tools] 发现文件: {item}")
            
            # 排序
            directories.sort()
            files.sort()
            
            print(f"[ArtX Tools] 扫描完成 - 目录: {len(directories)} 个, 文件: {len(files)} 个")
            
            # 格式化输出
            result = f"路径内容列表: {relative_path}\n"
            result += f"完整路径: {full_path}\n\n"
            
            if directories:
                result += f"📁 目录 ({len(directories)} 个):\n"
                result += "\n".join([f"  📁 {dir_name}" for dir_name in directories])
                result += "\n\n"
            
            if files:
                result += f"📄 文件 ({len(files)} 个):\n"
                result += "\n".join([f"  📄 {file_name}" for file_name in files])
                result += "\n\n"
            
            if not directories and not files:
                result += "目录为空\n"
            
            result += f"总计: {len(directories)} 个目录, {len(files)} 个文件"
            
            print(f"[ArtX Tools] 输出结果长度: {len(result)} 字符")
            return (result,)
            
        except Exception as e:
            error_msg = f"列出路径内容时出错: {str(e)}"
            print(f"[ArtX Tools] 异常: {error_msg}")
            import traceback
            print(f"[ArtX Tools] 异常详情:\n{traceback.format_exc()}")
            return (error_msg,)


class GitHubInstallerNode:
    """从GitHub URL安装ComfyUI插件或模型"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "github_url": ("STRING", {
                    "default": "https://github.com/vartx/repository-name",
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
    OUTPUT_NODE = True
    
    def install_from_github(self, github_url, install_type):
        try:
            print(f"[ArtX Tools] 开始GitHub安装: {github_url}")
            print(f"[ArtX Tools] 安装类型: {install_type}")
            
            # 验证GitHub URL格式
            if not github_url.startswith("https://github.com/"):
                error_msg = "错误：请提供有效的GitHub URL (https://github.com/...)"
                print(f"[ArtX Tools] {error_msg}")
                return (error_msg,)
            
            # 提取仓库信息
            url_parts = github_url.replace("https://github.com/", "").split("/")
            if len(url_parts) < 2:
                error_msg = "错误：GitHub URL格式不正确"
                print(f"[ArtX Tools] {error_msg}")
                return (error_msg,)
            
            owner = url_parts[0]
            repo = url_parts[1]
            print(f"[ArtX Tools] 仓库所有者: {owner}, 仓库名: {repo}")
            
            # 确定安装目录
            if install_type == "custom_nodes":
                base_path = os.path.join(folder_paths.base_path, "custom_nodes")
            else:  # models
                base_path = folder_paths.models_dir
            
            install_path = os.path.join(base_path, repo)
            print(f"[ArtX Tools] 安装路径: {install_path}")
            
            # 检查目录是否已存在
            if os.path.exists(install_path):
                error_msg = f"目录已存在: {install_path}\n如需重新安装，请先删除该目录"
                print(f"[ArtX Tools] {error_msg}")
                return (error_msg,)
            
            # 克隆仓库
            result = f"开始从 {github_url} 安装到 {install_type}...\n"
            print(f"[ArtX Tools] 开始克隆仓库...")
            
            try:
                # 使用git clone
                cmd = ["git", "clone", github_url, install_path]
                print(f"[ArtX Tools] 执行命令: {' '.join(cmd)}")
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                print(f"[ArtX Tools] Git返回码: {process.returncode}")
                if process.stdout:
                    print(f"[ArtX Tools] Git输出: {process.stdout}")
                if process.stderr:
                    print(f"[ArtX Tools] Git错误: {process.stderr}")
                
                if process.returncode == 0:
                    result += f"✅ 成功克隆到: {install_path}\n"
                    print(f"[ArtX Tools] 克隆成功")
                    
                    # 检查是否有requirements.txt或pyproject.toml
                    req_files = [
                        os.path.join(install_path, "requirements.txt"),
                        os.path.join(install_path, "pyproject.toml")
                    ]
                    
                    for req_file in req_files:
                        if os.path.exists(req_file):
                            result += f"📋 发现依赖文件: {os.path.basename(req_file)}\n"
                            result += "提示：可能需要手动安装依赖\n"
                            print(f"[ArtX Tools] 发现依赖文件: {req_file}")
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
                            print(f"[ArtX Tools] 发现说明文件: {readme_file}")
                            break
                    
                    result += f"\n🎉 安装完成！重启ComfyUI以加载新插件。"
                    
                else:
                    error_msg = process.stderr if process.stderr else "未知错误"
                    result += f"❌ 克隆失败: {error_msg}"
                    print(f"[ArtX Tools] 克隆失败: {error_msg}")
                    
            except subprocess.TimeoutExpired:
                error_msg = "❌ 安装超时（5分钟），请检查网络连接"
                result += error_msg
                print(f"[ArtX Tools] {error_msg}")
            except FileNotFoundError:
                error_msg = "❌ 未找到git命令，请确保已安装git"
                result += error_msg
                print(f"[ArtX Tools] {error_msg}")
            except Exception as e:
                error_msg = f"❌ 安装过程中出错: {str(e)}"
                result += error_msg
                print(f"[ArtX Tools] {error_msg}")
                import traceback
                print(f"[ArtX Tools] 异常详情:\n{traceback.format_exc()}")
            
            return (result,)
            
        except Exception as e:
            error_msg = f"GitHub安装器出错: {str(e)}"
            print(f"[ArtX Tools] {error_msg}")
            import traceback
            print(f"[ArtX Tools] 异常详情:\n{traceback.format_exc()}")
            return (error_msg,)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "PathListNode": PathListNode,
    "GitHubInstallerNode": GitHubInstallerNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PathListNode": "📁 路径内容列表",
    "GitHubInstallerNode": "🚀 GitHub安装器",
}
