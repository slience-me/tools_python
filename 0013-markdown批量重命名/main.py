# Author: slience_me
# Date: 2026/8/26 22:45
# Blog: https://slienceme.cn
import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path


# Markdown 图片语法：
# ![alt](path)
MARKDOWN_IMAGE_PATTERN = re.compile(
    r'(!\[[^\]]*\]\()([^)]+)(\))'
)


def calculate_file_hash(file_path: Path) -> str:
    """计算文件 SHA256。"""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def generate_unique_filename(
        source_file: Path,
        source_root: Path
) -> str:
    """
    根据源文件的相对路径生成唯一文件名。

    例如：
        docs/guide/install.md
        -> guide__install.md

        docs/api/user.md
        -> api__user.md
    """

    relative_path = source_file.relative_to(source_root)

    parts = list(relative_path.parts)

    # 去掉最后一个文件扩展名
    parts[-1] = Path(parts[-1]).stem

    safe_name = "__".join(parts)

    # 简单处理特殊字符
    safe_name = re.sub(r'[<>:"/\\|?*]', "_", safe_name)

    # 加短 hash，进一步保证唯一性
    path_hash = hashlib.md5(
        str(relative_path).encode("utf-8")
    ).hexdigest()[:8]

    return f"{safe_name}__{path_hash}.md"


def is_remote_path(path: str) -> bool:
    """
    判断是否为远程路径或不需要复制的路径。
    """

    path = path.strip()

    return (
            path.startswith("http://")
            or path.startswith("https://")
            or path.startswith("data:")
            or path.startswith("#")
    )


def clean_image_path(image_path: str) -> str:
    """
    清理 Markdown 图片路径中的 title 等信息。

    例如：
        image.png "title"
        -> image.png
    """

    image_path = image_path.strip()

    # 简单处理 Markdown title
    if " " in image_path:
        image_path = image_path.split(" ", 1)[0]

    return image_path.strip("<>")


def copy_image(
        image_file: Path,
        output_images_dir: Path
) -> str:
    """
    复制图片到 output/images。

    使用 hash 避免不同目录下同名图片冲突。
    """

    file_hash = calculate_file_hash(image_file)[:8]

    new_name = (
        f"{image_file.stem}"
        f"__{file_hash}"
        f"{image_file.suffix.lower()}"
    )

    target_file = output_images_dir / new_name

    if not target_file.exists():
        shutil.copy2(image_file, target_file)

    return new_name


def process_markdown_images(
        content: str,
        source_file: Path,
        source_root: Path,
        output_images_dir: Path,
        copied_images: list
) -> str:
    """
    处理 Markdown 中的图片。

    找到：
        ![alt](./images/test.png)

    将图片复制到：
        output/images/

    并修改 Markdown：

        ![alt](images/test__hash.png)
    """

    def replace_image(match):
        prefix = match.group(1)
        original_path = match.group(2)
        suffix = match.group(3)

        image_path = clean_image_path(original_path)

        # 网络图片 / Base64 不处理
        if is_remote_path(image_path):
            return match.group(0)

        # VuePress 中 /images/test.png
        # 这种路径默认从 source_root 开始寻找
        if image_path.startswith("/"):
            image_file = source_root / image_path.lstrip("/")
        else:
            image_file = source_file.parent / image_path

        try:
            image_file = image_file.resolve()
        except Exception:
            return match.group(0)

        # 图片不存在，保持原样
        if not image_file.exists():
            copied_images.append({
                "source": image_path,
                "status": "not_found"
            })

            return match.group(0)

        # 不是文件
        if not image_file.is_file():
            return match.group(0)

        try:
            new_image_name = copy_image(
                image_file,
                output_images_dir
            )

            copied_images.append({
                "source": str(image_file),
                "output": f"images/{new_image_name}",
                "status": "copied"
            })

            return f"{prefix}images/{new_image_name}{suffix}"

        except Exception as e:
            copied_images.append({
                "source": str(image_file),
                "status": "error",
                "error": str(e)
            })

            return match.group(0)

    return MARKDOWN_IMAGE_PATTERN.sub(
        replace_image,
        content
    )


def process_markdown_file(
        source_file: Path,
        source_root: Path,
        output_markdown_dir: Path,
        output_images_dir: Path
) -> dict:
    """处理单个 Markdown 文件。"""

    output_filename = generate_unique_filename(
        source_file,
        source_root
    )

    output_file = (
            output_markdown_dir /
            output_filename
    )

    copied_images = []

    # 尝试 UTF-8
    try:
        content = source_file.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError:
        content = source_file.read_text(
            encoding="utf-8-sig"
        )

    # 处理图片
    processed_content = process_markdown_images(
        content=content,
        source_file=source_file,
        source_root=source_root,
        output_images_dir=output_images_dir,
        copied_images=copied_images
    )

    # 写入输出
    output_file.write_text(
        processed_content,
        encoding="utf-8"
    )

    return {
        "id": hashlib.md5(
            str(source_file.relative_to(source_root))
            .encode("utf-8")
        ).hexdigest(),

        "source": str(
            source_file.relative_to(source_root)
        ),

        "output": str(
            Path("markdown") / output_filename
        ),

        "source_hash": calculate_file_hash(
            source_file
        ),

        "images": copied_images
    }


def find_markdown_files(source_root: Path):
    """递归查找所有 Markdown 文件。"""

    extensions = {
        ".md",
        ".markdown"
    }

    files = []

    for file_path in source_root.rglob("*"):
        if (
                file_path.is_file()
                and file_path.suffix.lower() in extensions
        ):
            files.append(file_path)

    return sorted(files)


def create_output_directories(output_root: Path):
    """创建输出目录。"""

    markdown_dir = (
            output_root / "markdown"
    )

    images_dir = (
            output_root / "images"
    )

    markdown_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    images_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return markdown_dir, images_dir


def save_manifest(
        output_root: Path,
        source_root: Path,
        documents: list
):
    """生成 manifest.json。"""

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "source_root": str(
            source_root.resolve()
        ),
        "document_count": len(documents),
        "documents": documents
    }

    manifest_file = (
            output_root / "manifest.json"
    )

    manifest_file.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "VuePress Markdown "
            "知识库预处理工具"
        )
    )

    parser.add_argument(
        "source",
        help="Markdown 源目录"
    )

    parser.add_argument(
        "output",
        help="输出目录"
    )

    args = parser.parse_args()

    source_root = Path(args.source)

    output_root = Path(args.output)

    if not source_root.exists():
        print(
            f"错误：源目录不存在："
            f"{source_root}"
        )
        return

    if not source_root.is_dir():
        print(
            f"错误：source 必须是目录："
            f"{source_root}"
        )
        return

    print("=" * 60)
    print("VuePress Markdown 知识库预处理工具")
    print("=" * 60)

    print(
        f"源目录："
        f"{source_root.resolve()}"
    )

    print(
        f"输出目录："
        f"{output_root.resolve()}"
    )

    # 创建目录
    markdown_dir, images_dir = (
        create_output_directories(
            output_root
        )
    )

    # 查找 Markdown
    markdown_files = find_markdown_files(
        source_root
    )

    print(
        f"\n发现 Markdown 文件："
        f"{len(markdown_files)} 个"
    )

    documents = []

    for index, source_file in enumerate(
            markdown_files,
            start=1
    ):
        print(
            f"[{index}/{len(markdown_files)}] "
            f"处理："
            f"{source_file.relative_to(source_root)}"
        )

        try:
            result = process_markdown_file(
                source_file=source_file,
                source_root=source_root,
                output_markdown_dir=markdown_dir,
                output_images_dir=images_dir
            )

            documents.append(result)

        except Exception as e:
            print(
                f"  处理失败：{e}"
            )

    # 保存 manifest
    save_manifest(
        output_root=output_root,
        source_root=source_root,
        documents=documents
    )

    print("\n" + "=" * 60)
    print("处理完成")
    print("=" * 60)

    print(
        f"Markdown 数量："
        f"{len(documents)}"
    )

    print(
        f"输出目录："
        f"{output_root.resolve()}"
    )

    print(
        f"索引文件："
        f"{output_root / 'manifest.json'}"
    )


if __name__ == "__main__":
    main()
