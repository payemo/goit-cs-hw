import asyncio
import aiofiles
from aiopath import AsyncPath
import logging
from datetime import datetime

from pathlib import Path
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def read_folder(src_folder: AsyncPath, dest_folder: AsyncPath):
    tasks = []
    async for path in src_folder.rglob('*'):
        if await path.is_file():
            tasks.append(copy_file(path, dest_folder))
    await asyncio.gather(*tasks)

async def copy_file(src_file: AsyncPath, dest_folder: AsyncPath):
    try:
        file_ext = src_file.suffix.lstrip('.').lower()
        if not file_ext:
            file_ext = "unknown"
        output_folder = dest_folder / file_ext
        await output_folder.mkdir(parents=True, exist_ok=True)

        output_file = output_folder / src_file.name
        async with aiofiles.open(src_file, mode='rb') as src:
            content = await src.read()
            async with aiofiles.open(output_file, mode='wb') as dst:
                await dst.write(content)
        logger.info(f"Copied: {src_file} -> {output_file}")

    except Exception as e:
        logger.error(f"Error during the copying: {e}")

def main():
    parser = ArgumentParser(description="Asynchronous files sorting by extension.")
    parser.add_argument("--source", type=str, help="Path to the source folder.")
    parser.add_argument("--output", type=str, help="Path to the destination folder.")

    args = parser.parse_args()

    src_folder = AsyncPath(args.source)
    dest_folder = AsyncPath(args.output)

    async def run():
        if not await src_folder.exists() or not src_folder.is_dir():
            logger.error("Specified folder does not exist.")
            return
    
        if not await dest_folder.exists():
            await dest_folder.mkdir(parents=True)

        start_time = datetime.now()
        logger.info(f"Start sorting: {start_time.strftime("%Y-%m-%d %H:%M:%S")}")

        await read_folder(src_folder, dest_folder)

        end_time = datetime.now()
        logger.info(f"Finish sorting: {end_time.strftime("%Y-%m-%d %H:%M:%S")}")
        logger.info(f"Total time: {end_time - start_time}")

    asyncio.run(run())

if __name__ == '__main__':
    main()