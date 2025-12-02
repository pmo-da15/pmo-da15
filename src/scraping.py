from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig


async def scrape_md(url: str):
    browser_cfg = BrowserConfig(verbose=False)
    run_cfg = CrawlerRunConfig(
        verbose=False,
        log_console=False,
        exclude_all_images=True,
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url, run_cfg)

    return result.markdown
