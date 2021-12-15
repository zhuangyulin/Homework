#https://so.gushiwen.cn/guwen/default.aspx?p=?   1-20
import scrapy
from scrapy.selector import Selector

class gujiSpider(scrapy.Spider):
    name = 'gujibook'
    allowed_domains = ['so.gushiwen.cn']

    start_urls = ['https://so.gushiwen.cn/guwen/default.aspx?p={}'.format(i) for i in range(1,21)]


    def parse(self, response):
        lis = response.xpath("//div[@class=\"sonspic\"]")
        for li in lis:
            booktitle = li.xpath("./div[1]/p[1]/a[1]//text()").extract_first()
            if booktitle:
                item = {}
                item['booktitle'] = booktitle
                bookhref = li.xpath("./div[1]/p[1]/a[1]/@href").extract_first()
                bookhref = "https://so.gushiwen.cn" + bookhref
                item['bookhref'] = bookhref
                brief = li.xpath("./div[1]/p[2]/text()").extract_first()
                item['brief'] = brief
                yield scrapy.Request(bookhref, callback=self.parse_detail, dont_filter=True, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta["item"]
        judge = response.xpath("//div[@class=\'bookcont\']/div[1]/strong/text()").extract()
        messagetitle = []
        if len(judge) != 0:
            div_list = response.xpath("//div[@class=\"bookcont\"]/div[2]/span").extract()
            for i in div_list:
                str1 = ''
                messagetitle.append(Selector(text=i).xpath("//a/text()").extract()[0])
                for j in messagetitle:
                    str1 = str1 + j + '；'
                item['messagetitle'] = str1
        else:
            div_list = response.xpath("//div[@class=\'bookcont\']/ul/span").extract()
            for i in div_list:
                str1 = ''
                messagetitle.append(Selector(text=i).xpath("//a/text()").extract()[0])
                for j in messagetitle:
                    str1 = str1 + j + '；'
                item['messagetitle'] = str1
        yield item

