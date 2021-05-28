import scrapy


class WebbSpider(scrapy.Spider):
    name = 'webb_invoices'
    start_urls = [
        'file:///Users/brighambyerly/Downloads/statement.html',
    ]

    def parse(self, response, **kwargs):
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
