import scrapy


# Execute this spider by calling
# scrapy runspider -o /path/to/output.csv -a username=USERNAME -a password=PASSWORD webb_spider.py
class WebbSpider(scrapy.Spider):

    name = 'webb_invoices'
    username = ''
    password = ''

    def start_requests(self):
        return [scrapy.FormRequest("https://ordering.fwwebb.com/wobf/login.process",
                                   formdata={'CUSTID': self.username, 'UPASSWORD': self.password,
                                             '@NEXT': 'https://ordering.fwwebb.com/'},
                                   callback=self.logged_in)]

    def logged_in(self, response, **kwargs):
        return [scrapy.Request("https://ordering.fwwebb.com/wobf/paybycredit", callback=self.parse_statement)]

    def parse_statement(self, response, **kwargs):
        dropdown_ids = ["Current", "30Days", "60Days", "90Days", "120Days"]
        dropdowns = map(lambda d: response.xpath(f"//*[@id='{d}']"), dropdown_ids)
        for dropdown in dropdowns:
            # Two rows correspond to one invoice
            invoice = {}
            rows = dropdown.xpath(".//tr")
            for i, row in enumerate(rows):
                if i % 2 == 0:
                    invoice['invoice_id'] = row.xpath("./th/div[1]/a/text()").get()
                    invoice['balance'] = row.xpath("./th/div[2]/text()").get().split(':')[1].strip()
                else:
                    invoice['invoice_date'] = row.xpath("./td/div[1]/p/text()").get().split(':')[1].strip()
                    invoice['order_num'] = row.xpath("./td/div[2]/p/text()").get().split(':')[1].strip()
                    invoice['job_name'] = row.xpath("./td/div[3]/p/text()").get().split(':')[1].strip()
                    invoice['po_num'] = row.xpath("./td/div[4]/p/text()").get().split(':')[1].strip()
                    yield invoice

    def parse(self, response, **kwargs):
        pass
