import os
import re

def fix_pydantic_imports(root_dir='backend'):
    replacements = [
        (r'from pydantic import .*BaseSettings.*', 'from pydantic_settings import BaseSettings'),
        (r'@validator', '@field_validator'),
        (r'class Config:', 'model_config ='),
        (r'orm_mode = True', '"from_attributes": True'),
    ]
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for pattern, replacement in replacements:
                    new_content = re.sub(pattern, replacement, new_content)
                
                if new_content != content:
                    print(f"修复文件: {filepath}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == '__main__':
    fix_pydantic_imports()
    print("完成！请检查修改是否正确。") 