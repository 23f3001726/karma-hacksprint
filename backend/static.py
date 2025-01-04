from bs4 import BeautifulSoup
import json

def scrape_static_page(soup):
  
  #Extracts specific data from a static webpage and returns it as a JSON object.

  try:
    # Extract data
    page_title = soup.title.string if soup.title else None

    headings = {
        'h1': [h1.text for h1 in soup.find_all('h1')] if soup.find_all('h1') else None,
        'h2': [h2.text for h2 in soup.find_all('h2')] if soup.find_all('h2') else None,
        'h3': [h3.text for h3 in soup.find_all('h3')] if soup.find_all('h3') else None,
        'h4': [h4.text for h4 in soup.find_all('h4')] if soup.find_all('h4') else None,
        'h5': [h5.text for h5 in soup.find_all('h5')] if soup.find_all('h5') else None,
        'h6': [h6.text for h6 in soup.find_all('h6')] if soup.find_all('h6') else None
    }

    links = [(a.text, a['href']) for a in soup.find_all('a')] if soup.find_all('a') else None

    ordered_lists = [[li.text for li in ol.find_all('li')] for ol in soup.find_all('ol')] if soup.find_all('ol') else None
    unordered_lists = [[li.text for li in ul.find_all('li')] for ul in soup.find_all('ul')] if soup.find_all('ul') else None

    html_tags = {}
    for tag in soup.find_all():
      tag_name = tag.name
      attributes = {attr: tag[attr] for attr in tag.attrs}
      if tag_name not in html_tags:
        html_tags[tag_name] = []
      html_tags[tag_name].append(attributes)
    html_tags = html_tags if html_tags else None

    tables = []
    for table in soup.find_all('table'):
      rows = []
      for row in table.find_all('tr'):
        cols = [col.text for col in row.find_all('td')]
        rows.append(cols)
      tables.append(rows)
    tables = tables if tables else None

    forms = []
    for form in soup.find_all('form'):
      fields = []
      for field in form.find_all('input'):
        fields.append({'type': field['type'], 'name': field.get('name'), 'value': field.get('value')})
      forms.append(fields)
    forms = forms if forms else None

    images = [img['src'] for img in soup.find_all('img')] if soup.find_all('img') else None
    videos = [video['src'] for video in soup.find_all('video')] if soup.find_all('video') else None
    audio = [audio['src'] for audio in soup.find_all('audio')] if soup.find_all('audio') else None

    # Create JSON object
    data = {
        'page_title': page_title,
        'headings': headings,
        'links': links,
        'ordered_lists': ordered_lists,
        'unordered_lists': unordered_lists,
        'html_tags': html_tags,
        'tables': tables,
        'forms': forms,
        'images': images,
        'videos': videos,
        'audio': audio
    }

  except Exception as e:
    print(f"Error fetching URL: {e}")
    data = {
        'page_title': None,
        'headings': None,
        'links': None,
        'ordered_lists': None,
        'unordered_lists': None,
        'html_tags': None,
        'tables': None,
        'forms': None,
        'images': None,
        'videos': None,
        'audio': None
    }

  return json.dumps(data, indent=2)