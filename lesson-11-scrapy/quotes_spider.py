import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page_number = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page_number
        with open(filename, 'wb') as f:
            f.write(response.body)
            
        # extract quote, author, tags and store data in csv file
        import csv
        file_csv = 'quotes-%s.csv' % page_number
        with open(file_csv, 'w') as f_csv:
            csv_writer = csv.writer(f_csv, lineterminator='\n', quoting=csv.QUOTE_ALL)
            for quote in response.css('div.quote'):
                txt = quote.css('span.text::text').extract_first()
                author = quote.css('small.author::text').extract_first()
                tags = quote.css('div.tags a.tag::text').extract()
                tags_str = " : ".join(tags)
                csv_writer.writerow([author,txt,tags_str])

        # follow the link
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)