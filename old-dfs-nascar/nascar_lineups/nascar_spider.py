import pandas as pd, numpy as np
import scrapy


class NascarSpider(scrapy.Spider):
    name = "projections"

    def start_requests(self):
        start_urls = ['file:///home/ubuntu/environment/dfs/dfs-nascar/current_projections']
            
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')[-1]
        
        for player in response.css('div.salaryboxTop'):
            yield {
                'player_name': player.css('span.playername::text').get().lstrip(),
                'lovecount': player.css('div.lovehatecount::text').getall()[1],
                'hatecount': player.css('div.lovehatecount::text').getall()[2],
                'owned': player.css('span.ownershipProjected::text').get(),
                'player_id': int(player.css('span.playername').attrib['data-playerid'])
            }
