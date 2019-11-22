import requests
import re
from datetime import datetime
import time

class Airbnb_Navigator:
    def seed_roots(self):
        return ['https://www.airbnb.com.au/s/New-South-Wales/homes']

    def next_roots(self, prev_root):
        if 'items_offset' in prev_root:
            prev_offset = prev_root.split('=')[-1]
            new_offset = str(int(prev_offset) + 18)
            return [prev_root.replace('items_offset='+prev_offset, 'items_offset='+new_offset)]

        return ['https://www.airbnb.com.au/s/New-South-Wales/homes?section_offset=5&items_offset=18']

    # Unpack a search result page, getting the urls of all the results
    def read_pages_from_route(self, root_path):
        landing = requests.get(root_path)
        html = str(landing.content)

        pages = []
        for section in html.split('href="/rooms/')[1:]:
            new_url = 'https://www.airbnb.com.au/rooms/'
            new_url += section.split('"')[0]
            if '/plus/' not in new_url:
                pages.append(new_url)

        print('Child read', len(pages), 'pages from', root_path)

        return pages

    # Go to a specific search result page, and get the info
    def visit_page(self, page_path):
        print('Visiting page', page_path)

        landing = requests.get(page_path)
        html = str(landing.content)

        i = 0
        while i < 10:
            if html.split('"lat":')[1].split(',')[0] != 'null':
                break
            print('Retrying due to null location...')
            time.sleep(1)

            landing = requests.get(page_path)
            html = str(landing.content)

            i += 1

        if i == 10:
            raise Exception('Couldn\'t get location')

        try:
            name = html.split('id="summary"')[1]
            name = name.split('</h1>')[0][:-7]
            name = name.split('>')[-1]
        except:
            print('Newname')
            name = html.split('"listingTitle":"')[1].split('"')[0]

        try:
            location = html.split('data-location="')[1].split('"')[0]
        except:
            location = html.split(' for Rent in ')[1].split('"')[0]
            #location = html.split('"id":"neighborhood-preview_')[1].split('"title":"')[1].split('"')[0]

        poster_url = 'https://www.airbnb.com.au'
        try:
            poster_url += html.split('id="summary"')[1].split('</a>')[0].split('href="')[1].split('"')[0]
        except:
            poster_url += '/users/' + html.split('href="/users/')[1].split('"')[0]

        bedCount = re.search(r'>([0-9]+) beds?</div>', html)
        bedCount = bedCount.group(1) if bedCount else 0


        bathCount = re.search(r'>([0-9]+) baths?</div>', html)
        bathCount = bathCount.group(1) if bathCount else 0

        # This could be better
        carCount = 1 if 'Free parking on premises' else 0

        description = 'Description not found'
        try:
            description = html.split('id="details"')[1].split('</span>')[0].split('<span>')[-1]
            description = description.replace('\\n', '\n')
        except IndexError as e:
            description = html.split('section.htmlDescription":')[1].split('"htmlText":"')[1].split('"')[0]
            description = description.replace('\\\\u003cbr />', '\n')
            description = description.replace('\\\\u003c/b>', '')
            description = description.replace('\\\\u003cb>', '')

        rate = re.search(r'for \$([0-9\.]+)\.', html)
        rate = rate.group(1) if rate else 0

        # Airbnb places dont advertise a global max/min stay
        minStay = '1' 
        maxStay = '1000'

        try:
            details = html.split('"additional_house_rules":"')[1].split('","')[0]
            details = details.replace('\\\\n', '\n')
        except IndexError:
            details = ''

        lat = html.split('"lat":')[1].split(',')[0]
        lng = html.split('"lng":')[1].split(',')[0]

        images = []
        for img in html.split('<img')[1:]:
            img = img.split('>')[0].split('src="')[1].split('"')[0]
            if '/user' not in img:
                images.append(img)

        dates = []
        api_key = html.split('"api_config"')[1].split('"key":"')[1].split('"')[0]
        page_num = page_path.split('/rooms/')[1].split('?')[0]
        for month in ['11', '12']:
            date_path = 'https://www.airbnb.com.au/api/v2/homes_pdp_availability_calendar?currency=AUD&key='+api_key+'&locale=en-AU&listing_id='+page_num+'&month='+month+'&year=2019'
            print('Grabbing dates:', date_path)

            date_landing = requests.get(date_path)
            date_html = str(date_landing.content)

            for date in date_html.split('"date":"')[1:]:
                if '"available":true' in date:
                    minStay = int(date.split('"min_nights":')[1].split(',')[0]) + 1
                    maxStay = int(date.split('"max_nights":')[1].split(',')[0]) + 1

                    date = date.split('"')[0]
                    dates.append(datetime.strptime(date, '%Y-%m-%d'))
        
        return {
            'name':         name,

            'location':     location,
            'lat':          lat,
            'lng':          lng,

            'bedCount':     bedCount,
            'bathCount':    bathCount,
            'carCount':     carCount,
            'description':  description,

            'rate':         rate,
            'minStay':      minStay,
            'maxStay':      maxStay,
            'details':      details,

            'images':       images,
            'dates':        dates,

            'ad_url':       page_path,
            'poster_url':   poster_url
        }