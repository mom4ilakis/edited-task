import argparse
import asyncio
import uuid
from urllib.parse import urlparse
from pathlib import Path

from playwright.async_api import async_playwright, Error


async def take_screenshot(page, save_path: Path):
    await page.screenshot(path=save_path, full_page=True)


def verify_url(url: str):
    parsed = urlparse(url)
    assert parsed.scheme != "", "scheme is missing from URL"


async def craw(target_url: str, links_to_follow: int, db_id: uuid.UUID, output_folder: Path):
    output_folder = output_folder / f"{db_id}"

    output_folder.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(target_url, wait_until="load")
            await take_screenshot(page, output_folder / "start.png")
            links = await page.eval_on_selector_all("a",
                                                    f"elements => elements.slice(0,{links_to_follow}).map(e=>e.href)")
            for i, link in enumerate(links, start=1):
                await page.goto(link, wait_until="load")
                await take_screenshot(page, output_folder / f"{i}.png")
        except Error as e:
            print(e)
            raise RuntimeError(f"Could not craw page: {target_url}")
        finally:
            await browser.close()


def main(target_url: str, links_to_follow: int, db_id: uuid.UUID, output_folder: Path):
    verify_url(url)
    asyncio.run(craw(target_url, links_to_follow, db_id, output_folder))


parser = argparse.ArgumentParser(prog='pythonPlaywrightSpider', description="A python playwright scraper")
parser.add_argument("url", type=str, help="URL to scrape")
parser.add_argument("--links_to_follow", type=int, help="Links to follow")
parser.add_argument("--id", type=uuid.UUID, help="If from database")
parser.add_argument("--screenshots-folder", type=Path, default=Path("screenshots"),
                    help="Directory to save screenshots in")
if __name__ == '__main__':
    args = parser.parse_args()

    url = args.url
    db_id: uuid.UUID = args.id
    links_to_follow: int = args.links_to_follow
    screenshots_folder: Path = args.screenshots_folder
    try:
        main(url, links_to_follow, db_id, screenshots_folder)
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
