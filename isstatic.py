from bs4 import BeautifulSoup

def is_static_page(response):
  """
  Checks if a webpage is static by analyzing its content.

  Args:
    url: The URL of the webpage to check.

  Returns:
    True if the page appears to be static, False otherwise.
  """

  try:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check for common indicators of dynamic content
    if soup.find('script'):  # Presence of JavaScript
      return False
    if soup.find('iframe'):  # Presence of iframes (often load external content)
      return False
    if soup.find('noscript'):  # Content only available with JavaScript
      return False
    if 'data-ajax' in str(soup):  # Common attribute for AJAX requests
      return False

    # Check for common indicators of static content
    if soup.find('meta', {'http-equiv': 'X-UA-Compatible'}):  # Browser compatibility meta tag
      return True
    if soup.find('meta', {'name': 'viewport'}):  # Mobile viewport meta tag
      return True

    # Basic heuristic based on content size (may not always be accurate)
    if len(response.content) < 10000:  # Adjust this threshold as needed
      return True

    return False  # Default to assuming dynamic if no strong indicators

  except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    return None
