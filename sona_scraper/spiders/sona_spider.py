import os
import scrapy
from scrapy.item import Item, Field
from scrapy.http import FormRequest, Request
from scrapy.spiders import Spider
from scrapy.utils.response import open_in_browser
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from twilio.rest import Client
import schedule
import time

settings = get_project_settings()

twilio_sid = settings.get('TWILIO_SID')
twilio_token = settings.get('TWILIO_TOKEN')

sona_user = settings.get('SONA_USER')
sona_pass= settings.get('SONA_PASS')

phone_numbers = settings.get('PHONE_NUMBERS')

class SonaSpider(scrapy.Spider):
    name = "sona"

    start_urls = ['https://wlu-ls.sona-systems.com/Default.aspx']

    # LOGIN TO SONA
    def parse(self, response):
        formdata = {'ctl00$ContentPlaceHolder1$userid': sona_user,
                'ctl00$ContentPlaceHolder1$pw': sona_pass }
        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        clickdata={'name': 'ctl00$ContentPlaceHolder1$default_auth_button'},
                                        callback=self.view_available_studies)

    def view_available_studies(self, response):
        available_studies_url = 'https://wlu-ls.sona-systems.com/all_exp_participant.aspx'
        yield Request(available_studies_url, callback=self.timeslots_available)

    def timeslots_available(self,response):
        for url in response.xpath('//td[1]//a//@href').extract():
            yield Request('https://wlu-ls.sona-systems.com/' + url, callback=self.timeslots_for_study)

    def timeslots_for_study(self,response):
        abstract_text = response.xpath('//tr[5]//td[2]//span/text()').extract()[0]
        available = response.xpath('//tr[position() = last()]//a//@href').extract()

        # Ensures that survey is available and it is a credit survey
        if available and '$' not in abstract_text:
            open_in_browser(response)
            print available[0]
            yield Request('https://wlu-ls.sona-systems.com/' + available[0], callback=self.timeslot_sign_up)

    def timeslot_sign_up(self,response):
        open_in_browser(response)
        button_text = response.xpath('//tr//td[3]//a/text()').extract()[0]

        if button_text == 'Sign Up ':
            client = Client(twilio_sid, twilio_token)

            for phone_number in phone_numbers:
                client.messages.create(
                    to=phone_number,
                    from_="+15068044270",
                    body="New assignment available"
                )

            sign_up_url = response.xpath('//tr//td[3]//a//@href').extract()[0]

            yield Request('https://wlu-ls.sona-systems.com/' + sign_up_url, callback=self.sign_up_form)

    def sign_up_form(self,response):
        yield FormRequest.from_response(response,
                                        clickdata={'name': 'ctl00$ContentPlaceHolder1$Submit_Button'},
                                        callback=self.sign_up_confirmation)

    def sign_up_confirmation(self,response):
        open_in_browser(response)
