from pathlib import Path
from playwright.sync_api import sync_playwright

output = Path("Web_IMG")
output.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for name, viewport in (("website-desktop", {"width": 1440, "height": 1000}), ("website-mobile", {"width": 390, "height": 844})):
        page = browser.new_page(viewport=viewport, device_scale_factor=1)
        page.goto("http://127.0.0.1:5174/", wait_until="networkidle")
        page.evaluate("""async () => {
          for (let y = 0; y < document.body.scrollHeight; y += 500) {
            window.scrollTo(0, y);
            await new Promise(resolve => setTimeout(resolve, 60));
          }
          window.scrollTo(0, 0);
          await new Promise(resolve => setTimeout(resolve, 200));
        }""")
        page.screenshot(path=str(output / f"{name}.png"), full_page=True)
        page.close()
    browser.close()
