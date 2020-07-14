import scrapy

class WebbSpider(scrapy.Spider):
    name = 'webb_invoices'
    start_urls = [
        'file:///path/to/file.html',
    ]

    def parse(self, response):
        for invoice in response.xpath("//form[@id='invoiceExportCSV']/div[@class='searchDataList']"):
            invoice_id = invoice.xpath("./div[1]/b/a/text()").get()
            invoice_date = invoice.xpath("./div[4]/p[1]/text()").get().split(':')[1].strip()

            order_date = invoice.xpath("./div[4]/p[2]/text()").get().split(':')[1].strip()
            order_num = invoice.xpath("./div[4]/p[3]/text()").get().split(':')[1].strip()
            po_num = invoice.xpath("./div[6]/p[1]/text()").get().split(':')[1].strip()

            amount = invoice.xpath("./div[7]/p[1]/text()")[3].get().strip()

            yield {
                'invoice_id': invoice_id, 'invoice_date': invoice_date, 'order_date': order_date,
                'order_num': order_num, 'po_num': po_num, 'amount': amount
            }

        #next_page = response.css('li.next a::attr("href")').get()
        #if next_page is not None:
        #    yield response.follow(next_page, self.parse)