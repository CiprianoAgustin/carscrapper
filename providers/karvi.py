from bs4 import BeautifulSoup
import logging
import re
import time
from providers.base_provider import BaseProvider

class Karvi(BaseProvider):
    def cars_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 0
        regex = r".*--(\d+)"

        while(True):    
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)

            if page_response.status_code != 200:
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            cars = page_content.find_all('section', class_='overflow-hidden bg-white border rounded-xl border-gray-300 outline-none relative w-full max-w-full min-h-[368px]')
            if len(cars) == 0:
                break

            for car in cars:
                title = car.find('h2').text
                price_section = car.find('div',class_='pb-2 text-xl text-karvi-orange').get_text().strip()
                if price_section is not None:
                    title = title + ' ' + price_section
                href = car.find('a')['href']
                matches = re.search(regex, href)
                print(matches)
                internal_id = matches.group(1)
                    
                yield {
                    'title': title, 
                    'url': self.provider_data['base_url'] + href,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                    }

            page += 1
            page_link = self.provider_data['base_url'] + source + f"p-{page}"
