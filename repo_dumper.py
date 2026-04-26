import os
import json

def create_repo_dump(root_dir='.', output_file='qca_dump.json'):
    repo_data = []
    
    # Дозволені розширення (щоб не тягнути бінарники, картинки чи exe-шники)
    allowed_extensions = {'.md', '.txt', '.cs', '.php', '.py', '.json', '.yaml', '.yml', '.sh'}
    
    print(f"[*] Сканування репозиторію: {os.path.abspath(root_dir)}")

    for subdir, dirs, files in os.walk(root_dir):
        # Ігноруємо системні та приховані папки
        if '.git' in subdir or '__pycache__' in subdir:
            continue
            
        for file in files:
            # Ігноруємо сам файл дампа і скрипт дампера
            if file in [output_file, 'repo_dumper.py']:
                continue

            ext = os.path.splitext(file)[1].lower()
            
            # Беремо файли з дозволеними розширеннями АБО файли без розширення (як LICENSE)
            if ext in allowed_extensions or ext == '':
                file_path = os.path.join(subdir, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Зберігаємо відносний шлях та вміст
                    repo_data.append({
                        "file_path": os.path.relpath(file_path, root_dir).replace('\\', '/'),
                        "content": content
                    })
                    print(f"  [+] Додано: {file_path}")
                except Exception as e:
                    print(f"  [!] Пропущено (помилка читання): {file_path} -> {e}")

    # Записуємо в JSON
    print(f"\n[*] Пакування в {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(repo_data, f, ensure_ascii=False, indent=2)
        
    print(f"[V] Готово! Зібрано {len(repo_data)} файлів. Можна годувати ШІ! ))))))))")

if __name__ == '__main__':
    create_repo_dump()