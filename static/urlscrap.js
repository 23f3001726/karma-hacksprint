// Show loading spinner
function showLoading() {
    document.getElementById('loading').style.display = 'flex';
  }
  
  // Hide loading spinner
  function hideLoading() {
    document.getElementById('loading').style.display = 'none';
  }
  
  // Function to handle the scraping request
  async function scrapeWebsite() {
    const url = document.getElementById('urlInput').value;
  
    if (!url) {
      alert("Please enter a URL");
      return;
    }
  
    showLoading();  // Show the spinner when the request starts
  
    try {
      const response = await fetch('/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
  
      const jsonData = await response.json();
      
      if (jsonData.static === undefined) {
        throw new Error('Invalid response: No static flag');
      }
  
      if (jsonData.static) {
        displayStaticPage(jsonData);
      } else {
        displayDynamicPage(jsonData);
      }
  
    } catch (error) {
      document.getElementById('jsonOutput').innerHTML = `<div class="error">Error: ${error.message}</div>`;
    } finally {
      hideLoading();  // Hide the spinner when the request finishes
    }
  }
  
  // Function to display static page JSON
  function displayStaticPage(data) {
    let outputHtml = '<h3>Static Page Data</h3>';
    outputHtml += formatJsonData(data);
    document.getElementById('jsonOutput').innerHTML = outputHtml;
  }
  
  // Function to display dynamic page JSON
  function displayDynamicPage(data) {
    let outputHtml = '<h3>Dynamic Page Data</h3>';
    outputHtml += formatJsonData(data);
    document.getElementById('jsonOutput').innerHTML = outputHtml;
  }
  
  // Function to format JSON data into HTML (with dropdowns for nested data)
  function formatJsonData(data) {
    let html = '';
  
    for (let key in data) {
      if (data[key] !== null && data[key] !== "None") {
        html += createDropdown(key, data[key]);
      }
    }
  
    return html;
  }
  
  // Function to create dropdown for each JSON key-value pair
  function createDropdown(key, value) {
    let html = `<div class="json-section">`;
    html += `<strong>${formatTitle(key)}</strong>`;
  
    if (typeof value === 'boolean') {
      html += `<span>: ${value ? 'Yes' : 'No'}</span>`;
    } else if (Array.isArray(value)) {
      html += renderArray(value);
    } else if (typeof value === 'object') {
      html += renderObject(value);
    } else {
      html += `<span>: ${formatValue(value)}</span>`;
    }
  
    html += `</div>`;
    return html;
  }
  
  // Function to format the title (key) to be more human-friendly
  function formatTitle(title) {
    // Replace underscores or camelCase with spaces and capitalize first letters
    return title.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
  }
  
  // Function to format values for better readability
  function formatValue(value) {
    if (typeof value === 'string' && value.length > 100) {
      return `${value.substring(0, 100)}...`; // Truncate long strings
    }
    return value;
  }
  
  // Function to render array values with dropdowns if necessary
  function renderArray(arr) {
    let html = `<div class="dropdown">`;
    html += `<button class="dropdown-btn">Show List (${arr.length} items)</button>`;
    html += `<div class="dropdown-content hidden">`;
    arr.forEach(item => {
      html += `<div class="nested">${JSON.stringify(item)}</div>`;
    });
    html += `</div>`;
    html += `</div>`;
    return html;
  }
  
  // Function to render nested object values with dropdowns
  function renderObject(obj) {
    let html = `<div class="dropdown">`;
    html += `<button class="dropdown-btn">Show Object</button>`;
    html += `<div class="dropdown-content hidden">`;
    for (let key in obj) {
      if (obj[key] !== null && obj[key] !== "None") {
        html += createDropdown(key, obj[key]);
      }
    }
    html += `</div>`;
    html += `</div>`;
    return html;
  }
  
  // Add event listener for dropdown buttons
  document.addEventListener('click', function (e) {
    if (e.target && e.target.matches('.dropdown-btn')) {
      const content = e.target.nextElementSibling;
      if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
      } else {
        content.classList.add('hidden');
      }
    }
  });
   