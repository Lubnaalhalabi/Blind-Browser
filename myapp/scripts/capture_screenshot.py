import asyncio
from pyppeteer import launch
import os

async def capture_screenshot(url, output_path):
    try:
        # Launch the browser in headless mode
        browser = await launch(
            # executablePath='C:/Users/ASUS/Desktop/blindbrowser/chrome-win/chrome.exe',
            executablePath=os.path.join('chrome-win', 'chrome.exe'),
            headless=True,  # Ensures the browser runs without a GUI
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        page = await browser.newPage()
        
        # Navigate to the page
        await page.goto(url, {'waitUntil': 'networkidle0'})      
                
        # Capture a full-page screenshot
        await page.screenshot({'path': output_path, 'fullPage': True})
        
        # Close the browser
        await browser.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # local_html_path = 'file:///C:/Users/ASUS/Desktop/blindbrowser/myapp/static/saved_html/result.html'
    # output_path = 'C:/Users/ASUS/Desktop/blindbrowser/myapp/static/Images/segmented_image.png'
    # Relative paths
    local_html_path = os.path.join(base_dir, 'myapp', 'static', 'saved_html', 'result.html')
    output_path = os.path.join(base_dir, 'myapp', 'static', 'Images', 'segmented_image.png')
    
    # Convert HTML file path to an absolute path and replace backslashes with forward slashes
    abs_local_html_path = os.path.abspath(local_html_path).replace("\\", "/")
    
    # Construct the file URL
    file_url = f'file:///{abs_local_html_path}'
    
    try:
        # Run the async function in the event loop
        asyncio.run(capture_screenshot(file_url, output_path))
    except Exception as e:
        print(f"An error occurred during main execution: {e}")
