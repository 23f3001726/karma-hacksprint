import json
from playwright.sync_api import sync_playwright

def check_infinite_scrolling(page):
    try:
        # Check if infinite scrolling is implemented by detecting an element that triggers new content loading
        scrollable_element = page.locator('body')

        # Try scrolling to the bottom
        initial_scroll_height = page.evaluate('document.body.scrollHeight')
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_timeout(2000)  # Wait for any new content to load
        new_scroll_height = page.evaluate('document.body.scrollHeight')

        # If the scroll height changes after scrolling, it indicates infinite scrolling is likely
        if new_scroll_height > initial_scroll_height:
            return True
        return False
    
    except Exception as e:
        print(f"Error in check_infinite_scrolling: {str(e)}")
        return False



def check_single_page_app(page):
    try:
        # SPA can be detected if the page URL does not change upon navigating or loading new content
        initial_url = page.url
        page.evaluate('window.history.pushState(null, null, "/new-page")')  # Simulate URL change
        page.wait_for_timeout(2000)  # Wait for content to load
        new_url = page.url

        # If the URL changes without reloading the page, it's a SPA
        if new_url != initial_url:
            return False  # URL changed, so it's not a SPA (traditional multi-page site)
        return True  # URL stayed the same, indicating SPA
    
    except Exception as e:
        print(f"Error in check_infinite_scrolling: {str(e)}")
        return False



def scrape_dynamic_website(url):
    # Initialize Playwright and launch a browser in headless mode
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Can also use p.firefox or p.webkit
        page = browser.new_page()
        page.goto(url)
        # Start scraping the data
        data = {}
        # 1. Get Page Title
        data['title'] = page.title() or 'None'
        # 2. Get Headings (h1, h2, h3, h4, h5, h6)
        headings = {}
        for i in range(1, 7):
            heading_elements = page.locator(f'h{i}')
            headings[f'h{i}'] = [el.text_content() for el in heading_elements.all()]
        data['headings'] = headings
        # 3. Get All Links
        links = [el.get_attribute('href') for el in page.locator('a').all()]
        data['links'] = links or 'None'
        # 4. Get Ordered and Unordered Lists
        ordered_lists = [el.text_content() for el in page.locator('ol').all()]
        unordered_lists = [el.text_content() for el in page.locator('ul').all()]
        data['ordered_lists'] = ordered_lists or 'None'
        data['unordered_lists'] = unordered_lists or 'None'
        # 5. Get Labels
        labels = [el.text_content() for el in page.locator('label').all()]
        data['labels'] = labels or 'None'
        # 6. Get Image URLs and Alt Text
        images = []
        for img in page.locator('img').all():
            img_url = img.get_attribute('src')
            alt_text = img.get_attribute('alt')
            images.append({'src': img_url, 'alt': alt_text})
        data['images'] = images or 'None'
        # 7. Get Table Data
        tables = []
        for table in page.locator('table').all():
            table_data = []
            rows = table.locator('tr')
            for row in rows.all():
                row_data = [cell.text_content() for cell in row.locator('td').all()]
                table_data.append(row_data)
            tables.append(table_data)
        data['tables'] = tables or 'None'
        # 8. Get Form Data
        forms = []
        for form in page.locator('form').all():
            form_data = {}
            inputs = form.locator('input, textarea, select, button')
            for input_element in inputs.all():
                name = input_element.get_attribute('name')
                value = input_element.get_attribute('value')
                form_data[name] = value
            forms.append(form_data)
        data['forms'] = forms or 'None'
        # 9. Get Metadata (meta tags)
        metadata = {}
        for meta in page.locator('meta').all():
            name = meta.get_attribute('name') or meta.get_attribute('property')
            content = meta.get_attribute('content')
            if name and content:
                metadata[name] = content
        data['metadata'] = metadata or 'None'
        # 10. Get Video Data (URLs, Titles, Descriptions)
        videos = []
        for video in page.locator('video').all():
            video_url = video.get_attribute('src')
            video_title = video.get_attribute('title')
            video_description = video.get_attribute('description')
            videos.append({
                'url': video_url,
                'title': video_title,
                'description': video_description
            })
        data['videos'] = videos or 'None'
        # 11. Get Audio Data (URLs, Titles, Descriptions)
        audios = []
        for audio in page.locator('audio').all():
            audio_url = audio.get_attribute('src')
            audio_title = audio.get_attribute('title')
            audio_description = audio.get_attribute('description')
            audios.append({
                'url': audio_url,
                'title': audio_title,
                'description': audio_description
            })
        data['audios'] = audios or 'None'
        # 12. Get JavaScript Generated Content (Basic Example)
        js_content = page.evaluate('document.body.innerText')
        data['js_generated_content'] = js_content or 'None'
        # Check if the page supports infinite scrolling
        data['infinite_scrolling'] = check_infinite_scrolling(page)
        # Check if the page is a Single Page Application (SPA)
        data['single_page_app'] = check_single_page_app(page)
        # Close the browser
        browser.close()
        return json.dumps(data, indent = 2)
