import os
import re

def fix_all_imports(root_dir='backend'):
    # 修复简单的导入语句
    import_patterns = [
        (r'from app\.', 'from backend.app.'),
        (r'import app\.', 'import backend.app.')
    ]
    
    fixed_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for pattern, replacement in import_patterns:
                    new_content = re.sub(pattern, replacement, new_content)
                
                if new_content != content:
                    print(f"修复导入语句: {filepath}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_files.append(filepath)
    
    return fixed_files

if __name__ == '__main__':
    fixed = fix_all_imports()
    print(f"共修复了 {len(fixed)} 个文件的导入路径问题。")
    print("完成！请重新启动应用程序。") 