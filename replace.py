import os
import re
import shutil

# ===== 配置 =====
PROJECT_PATH = "."  # 当前项目目录

# 是否创建备份文件
ENABLE_BACKUP = True

# dot shorthand 映射规则
REPLACEMENTS = [
    # Alignment shortcuts
    (r'(?<![A-Za-z0-9_])\.centerRight', 'Alignment.centerRight'),
    (r'(?<![A-Za-z0-9_])\.centerLeft', 'Alignment.centerLeft'),
    (r'(?<![A-Za-z0-9_])\.topLeft', 'Alignment.topLeft'),
    (r'(?<![A-Za-z0-9_])\.topRight', 'Alignment.topRight'),
    (r'(?<![A-Za-z0-9_])\.bottomLeft', 'Alignment.bottomLeft'),
    (r'(?<![A-Za-z0-9_])\.bottomRight', 'Alignment.bottomRight'),

    # EdgeInsets symmetric shorthand
    (r'(?<![A-Za-z0-9_])\.symmetric\(', 'EdgeInsets.symmetric('),

    # BoxShape transparency shorthand (如果存在)
    (r'(?<![A-Za-z0-9_])\.transparency', 'BoxShape.rectangle'),
]

def fix_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original = content

        for pattern, replacement in REPLACEMENTS:
            content = re.sub(pattern, replacement, content)

        if content != original:
            if ENABLE_BACKUP:
                backup_path = file_path + ".bak"
                if not os.path.exists(backup_path):
                    shutil.copy2(file_path, backup_path)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Fixed: {file_path}")

    except Exception as e:
        print(f"Skip {file_path}: {e}")

def scan_project():
    for root, _, files in os.walk(PROJECT_PATH):
        for file in files:
            if file.endswith(".dart"):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    scan_project()
    print("✅ Dot-shorthand auto fix completed.")

