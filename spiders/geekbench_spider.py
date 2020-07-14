import scrapy

class GeekbenchSpider(scrapy.Spider):
    name = 'benchmarks'
    start_urls = [
        'https://browser.geekbench.com/v5/cpu/search?q=Macbook+Pro+2020+i5-1038NG7',
    ]

    def parse(self, response):
        for entry in response.xpath("//div[@class='col-12 list-col']/div/div"):
            sys_name = entry.xpath('./div[1]/a/text()').get()

            processor = entry.xpath("./div[1]/span[@class='list-col-model']/text()").get().strip().replace('\r', '').split('\n')
            sys_processor_model = processor[0].strip()
            sys_processor_speed = processor[1].strip()
            sys_processor_cores = processor[2].strip()

            sys_platform = entry.xpath("./div[3]/span[@class='list-col-text']/text()").get().strip()
            benchmark_single_core = entry.xpath("./div[4]/span[@class='list-col-text-score']/text()").get().strip()
            benchmark_multi_core = entry.xpath("./div[5]/span[@class='list-col-text-score']/text()").get().strip()

            yield {
                'system': sys_name, 'platform': sys_platform, 'processor_model': sys_processor_model, 'processor_speed': sys_processor_speed,
                'processor_cores': sys_processor_cores, 'single_core': benchmark_single_core, 'multi_core': benchmark_multi_core
            }

        #next_page = response.css('li.next a::attr("href")').get()
        #if next_page is not None:
        #    yield response.follow(next_page, self.parse)