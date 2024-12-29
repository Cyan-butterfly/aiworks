import os
from pathlib import Path

# 定义文件和文件夹的图标映射
ICONS = {
    "folder": "📁",
    "file": "📦",
    "python": "🐍",
    "docker": "🐳",
    "image": "🖼️",
    "video": "🎥",
    "notebook": "📓",
    "script": "📝",
    "config": "⚙️",
    "doc": "📝",
    "ppt": "📽",
    "pdf": "📄",
    "other": "📦"
}

def get_icon(file_path: Path) -> str:
    """
    根据文件类型返回相应的图标。
    可以根据需要自行增加、修改或删除判断条件。
    """
    if file_path.is_dir():
        return ICONS["folder"]
    
    suffix = file_path.suffix.lower()
    name = file_path.name.lower()

    if suffix == ".py":
        return ICONS["python"]
    elif suffix in [".md", ".txt", ".rst"]:
        return ICONS["file"]
    elif suffix in [".png", ".jpg", ".jpeg", ".gif"]:
        return ICONS["image"]
    elif suffix in [".mp4", ".avi", ".mov", ".mkv"]:
        return ICONS["video"]
    elif suffix == ".ipynb":
        return ICONS["notebook"]
    elif name in ["dockerfile", "docker-compose.yml", "docker-compose.yaml"]:
        return ICONS["docker"]
    elif suffix in [".yaml", ".yml"]:
        return ICONS["config"]
    elif suffix in [".doc", ".docx"]:
        return ICONS["doc"]
    elif suffix in [".ppt", ".pptx"]:
        return ICONS["ppt"]
    elif suffix in [".pdf"]:
        return ICONS["pdf"]
    else:
        return ICONS["other"]

def generate_markdown(
    dir_path: Path, 
    indent: int = 0, 
    exclude_dirs=None, 
    exclude_files=None, 
    visited=None
) -> str:
    """
    递归生成带有图标和格式化的 Markdown 目录结构。

    参数：
    - dir_path (Path): 要遍历的目录路径
    - indent (int): 缩进层级，用于生成嵌套列表
    - exclude_dirs (list): 要排除的目录列表
    - exclude_files (list): 要排除的文件列表
    - visited (set): 已访问过的目录集合，防止重复遍历
    """
    if exclude_dirs is None:
        exclude_dirs = []
    if exclude_files is None:
        exclude_files = []
    if visited is None:
        visited = set()

    markdown = ""
    resolved_dir = dir_path.resolve()

    # 如果已访问过该目录，直接返回空字符串，避免重复
    if resolved_dir in visited:
        return markdown
    visited.add(resolved_dir)

    # 获取当前目录下的所有项，并按照“文件夹优先、名称排序”进行排序
    items = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

    for item in items:
        # 排除指定的目录和文件
        if item.is_dir() and item.name in exclude_dirs:
            continue
        if item.is_file() and item.name in exclude_files:
            continue

        icon = get_icon(item)
        # 如果是文件夹，则在名称后加“/”以示区分
        if item.is_dir():
            line = "  " * indent + f"- {icon} **{item.name}**/"
            markdown += line + "\n"
            # 递归遍历子目录
            markdown += generate_markdown(
                item, 
                indent=indent + 1, 
                exclude_dirs=exclude_dirs, 
                exclude_files=exclude_files, 
                visited=visited
            )
        else:
            line = "  " * indent + f"- {icon} **{item.name}**"
            markdown += line + "\n"
    return markdown

def main():
    base_dir = Path.cwd()

    # 可以根据需要排除不想展示的目录和文件
    exclude_dirs = [".git", "__pycache__", ".idea", ".vscode", "node_modules"]
    exclude_files = ["generate_directory_structure.py"]  # 您想隐藏的文件

    directory_structure = generate_markdown(
        dir_path=base_dir,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files
    )

    output_file = base_dir / "DIRECTORY_STRUCTURE.md"
    with output_file.open("w", encoding="utf-8") as f:
        f.write("# 项目目录结构\n\n")
        f.write(directory_structure)

    print(f"目录结构已生成并写入到 {output_file}")

if __name__ == "__main__":
    main()
