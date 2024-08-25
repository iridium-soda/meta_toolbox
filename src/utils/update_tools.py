"""
Automatically updates the tools registry upon program startup.
This tool copies the implementation code of tools into the `metagpt/tools/libs` directory within the package.
"""

import importlib.util
from loguru import logger
import os,shutil

def find_lib_path(libname:str):
    spec = importlib.util.find_spec(libname)

    if spec is not None:
        library_dir = os.path.dirname(spec.origin)
        print(library_dir)
        return library_dir  # 输出库的绝对路径
    else:
        logger.error(f"Lib {libname} not found.")
        return None
import os
import shutil

def copy_py_files(src_dir, dest_dir):
    """
    将 src_dir 下所有子目录的 .py 文件复制到 dest_dir。

    @param src_dir: 源目录路径，例如 'src/tools'
    @param dest_dir: 目标目录路径

    @return None
    """
    # 确保目标目录存在
    if not os.path.exists(dest_dir):
        logger.exception(f"{dest_dir} not exist")
        return
    # 遍历源目录下的所有子目录和文件
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            # 检查文件是否以 .py 结尾
            if file.endswith('.py'):
                # 构造完整的文件路径
                src_file = os.path.join(root, file)
                # 将文件复制到目标目录
                shutil.copy(src_file, dest_dir)
                logger.info(f"Copy tool: {src_file} to {dest_dir}")

def update_tools():
    """
    Copy tools to `[package root]/metagpt/tools/libs`
    """
    lib_root_path=find_lib_path("metagpt")
    assert lib_root_path

    try:
        tools_lib_path=os.path.join(lib_root_path,"tools/libs")
        copy_py_files(src_dir="./src/tools",dest_dir=tools_lib_path)
    except Exception as e:
        logger.exception(e)

if __name__=="__main__":
    update_tools()