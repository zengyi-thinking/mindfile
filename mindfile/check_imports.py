import os
import re

def check_imports(root_dir='backend'):
    pattern = re.compile(r'from\s+app\.|import\s+app\.')
    issues = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    if matches:
                        issues.append((filepath, matches))
    
    return issues

if __name__ == '__main__':
    issues = check_imports()
    if issues:
        print("发现导入问题:")
        for filepath, matches in issues:
            print(f"文件: {filepath}")
            for match in matches:
                print(f"  - {match}")
        print("\n请将上述导入修改为从'backend.app'开始")
    else:
        print("没有发现导入问题!") 