import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from url3 import urls

for index, url in enumerate(urls):
    # url = 'https://algo.monster' + list.find('a')['href']
    # filename = list.text.replace('/', '-').replace('\\', '-')  # Sanitize filename       

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text.replace('<pre>', '<div>').replace('</pre>', '</div>'), 'html.parser')

        footer_div = soup.find('div', class_='CallToGetPremium_container__an75T')
        footer_ps = soup.find_all('p', class_='RequestClarification_bodytext__5sGkF')
        footer_div.decompose()

        for footer_p in footer_ps:
            footer_p.decompose()
        code_blocks = soup.find_all('code')

        for block in code_blocks:
            # Replace code blocks with Markdown code fence (```) syntax
            # This is a simplistic approach and may need adjustment based on your HTML structure
            spans = block.find_all('span')
            for span in spans:
                span_text = span.text
                span.replace_with(span_text) 
            if len(spans) > 0:
                code_text = block.get_text()
                markdown_code_block = f"python\n{code_text}\n"
                block.replace_with(markdown_code_block)               
        # soup.prettify()
        markdown_content = md(str(soup.find('main')), heading_style="ATX") + '---\n'
        with open('all3.md', 'a', encoding='utf-8') as file:
            file.write(markdown_content)
        print(url)
    else:
        print("Failed to retrieve the content")

