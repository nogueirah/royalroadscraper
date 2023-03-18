import scrapy
from epub_file import EpubBook

novelSearch = "ashes of heaven book one"

class RoyalRoad(scrapy.Spider):
    name = "royalroad"

    epub_file = None
        
    def start_requests(self):
        url = "https://www.royalroad.com/fictions/search?title=" + novelSearch.replace(' ', '+')
        yield scrapy.Request(url, callback=self.parse_novel)

    def parse_novel(self, response):
        novel_link = response.xpath("/html/body/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div/h2/a/@href").get()
        if novel_link is not None:
            print(response.urljoin(novel_link))
            yield scrapy.Request(response.urljoin(novel_link), callback=self.parse_novel_chapter)
        else:
            print("Novel not found")

    def parse_novel_chapter(self, response):
        novel_chapter = response.xpath("/html/body/div[3]/div/div/div/div[1]/div/div[1]/div[3]/a/@href").get()
        if novel_chapter is not None:
            title = response.xpath("/html/body/div[3]/div/div/div/div[1]/div/div[1]/div[2]/div/h1/text()").get()
            author = response.xpath("/html/body/div[3]/div/div/div/div[1]/div/div[1]/div[2]/div/h4/span[2]/a/text()").get()
            self.epub_file = EpubBook(title, author)
            yield scrapy.Request(response.urljoin(novel_chapter))            
        else:
            print("First chapter not found")

    def parse(self, response):
        chapter_title = response.xpath("/html/body/div[3]/div/div/div/div/div[1]/div/div[2]/h1/text()").get()
        chapter_content = response.xpath("/html/body/div[3]/div/div/div/div/div[3]/div[2]/div[2]").get()
        
        self.epub_file.new_chapter(chapter_title, chapter_content)      
        
        chapter_next = response.xpath("/html/body/div[3]/div/div/div/div/div[3]/div[2]/div[1]/div[2]/a/@href").get()              
        
        if chapter_next is not None:
            yield scrapy.Request(response.urljoin(chapter_next))  
        else:
            self.epub_file.write_file()
            