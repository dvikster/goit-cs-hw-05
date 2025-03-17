import argparse
import asyncio
import logging
import shutil
from pathlib import Path

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path: Path, destination_folder: Path):
    try:
        extension = file_path.suffix[1:] if file_path.suffix else 'no_extension'
        target_folder = destination_folder / extension
        target_folder.mkdir(parents=True, exist_ok=True)

        destination_path = target_folder / file_path.name
        await asyncio.to_thread(shutil.copy2, file_path, destination_path)  # Асинхронне копіювання
        logging.info(f"Файл {file_path} скопійовано до {destination_path}")
    except Exception as e:
        logging.error(f"Помилка під час копіювання файлу {file_path}: {e}")

async def read_folder(source_folder: Path, destination_folder: Path):
    tasks = []
    try:
        for item in source_folder.rglob('*'):
            if item.is_file():
                tasks.append(asyncio.create_task(copy_file(item, destination_folder)))
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Помилка під час читання папки {source_folder}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням.")
    parser.add_argument('source_folder', type=Path, nargs='?', default=Path("D:/ms/source"), help="Шлях до вихідної папки")
    parser.add_argument('destination_folder', type=Path, nargs='?', default=Path("D:/ms/destination"), help='Шлях до папки призначення')
    args = parser.parse_args()
    
    asyncio.run(read_folder(args.source_folder, args.destination_folder))

if __name__ == "__main__":
    main()

