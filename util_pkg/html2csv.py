import workutil, csv, argparse, sys, urllib.request
from parsel import Selector

def crawl_and_scrape(file_in, csvfile, local):
    #fieldnames = ['system', 'platform', 'processor_model', 'processor_speed', 'processor_cores', 'single_core', 'multi_core']
    fieldnames = ['invoice_id', 'invoice_date', 'order_date', 'order_num', 'po_num', 'amount']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)

    raw_in = ''
    with file_in as f:
        raw_in = f.read()

    if local:
        parse_html_stream_webb(raw_in, writer)
    else:
        urls = raw_in.split('\n')
        for url in urls:
            if url:
                print(f'Downloading content from {url}')

                url_content = ''
                with urllib.request.urlopen(url) as f:
                    url_content = f.read().decode('utf-8')

                parse_html_stream_webb(url_content, writer)

def parse_html_stream(html_str, writer):
    selector = Selector(text=html_str)

    for div in selector.xpath("//div[@class='col-12 list-col']/div/div"):
        sys_name = div.xpath('./div[1]/a/text()').get()

        processor = div.xpath("./div[1]/span[@class='list-col-model']/text()").get().strip().replace('\r', '').split('\n')
        sys_processor_model = processor[0].strip()
        sys_processor_speed = processor[1].strip()
        sys_processor_cores = processor[2].strip()

        sys_platform = div.xpath("./div[3]/span[@class='list-col-text']/text()").get().strip()
        benchmark_single_core = div.xpath("./div[4]/span[@class='list-col-text-score']/text()").get().strip()
        benchmark_multi_core = div.xpath("./div[5]/span[@class='list-col-text-score']/text()").get().strip()

        writer.writerow([sys_name, sys_platform, sys_processor_model, sys_processor_speed, sys_processor_cores, benchmark_single_core, benchmark_multi_core])

def parse_html_stream_webb(html_str, writer):
    selector = Selector(text=html_str)

    items = selector.xpath("//form[@id='invoiceExportCSV']/div[@class='searchDataList']")

    for div in items:
        invoice_id = div.xpath("./div[1]/b/a/text()").get()
        invoice_date = div.xpath("./div[4]/p[1]/text()").get().split(':')[1].strip()

        order_date = div.xpath("./div[4]/p[2]/text()").get().split(':')[1].strip()
        order_num = div.xpath("./div[4]/p[3]/text()").get().split(':')[1].strip()
        po_num = div.xpath("./div[6]/p[1]/text()").get().split(':')[1].strip()

        amount = div.xpath("./div[7]/p[1]/text()")[3].get().strip()

        writer.writerow([invoice_id, invoice_date, order_date, order_num, po_num, amount])

def run_standalone():
    arg_parser = argparse.ArgumentParser(description='Extract data from HTML files or URLs')
    arg_parser.add_argument('-I', dest='file_in', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='input file with a list of webpages to download and parse')
    arg_parser.add_argument('--local', dest='local', action='store_true', help='parse the input file itself (if the input file does not contain a list of links')
    arg_parser.add_argument('-O', dest='file_out', nargs='?', type=argparse.FileType('w'), default=workutil.gen_out_filename('html'), help='output csv file')

    args = arg_parser.parse_args()
    with args.file_out as csvfile:
        record_count = 'x'
        crawl_and_scrape(args.file_in, csvfile, args.local)
        print(f'All done! {record_count} record(s) written to {args.file_out.name}')

if __name__ == '__main__':
    run_standalone()