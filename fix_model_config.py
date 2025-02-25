import os
import re

def fix_model_config(root_dir='backend'):
    pattern = re.compile(r'model_config =\s+\"from_attributes\": True')
    replacement = 'model_config = {\n        "from_attributes": True\n    }'
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = pattern.sub(replacement, content)
                if new_content != content:
                    print(f"修复文件: {filepath}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == '__main__':
    fix_model_config()
    print("完成！请检查修改是否正确。") 