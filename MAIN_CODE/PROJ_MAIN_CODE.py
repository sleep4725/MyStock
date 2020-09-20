import os
import yaml
import json
import requests
import time
from bs4 import BeautifulSoup
from openpyxl import load_workbook

from RetSelenium.retSeleniumObj import RetSeleniumObj
from RetXl.RetXlObj import RetXlObj

#
# __author__ : 김준현
#

class PROJ_MAIN_CODE():

    def __init__(self):
        RetXlObj.get_xl_obj()
        self.config_data = PROJ_MAIN_CODE.get_config()
        self.my_stock_list = PROJ_MAIN_CODE.get_my_stock_info()
        self.chrome_obj = RetSeleniumObj.get_selenium_obj()
        self.total_data = list()

    def url_requests(self, searchWord):
        """

        :param searchWord:
        :return:
        """
        req_url = self.config_data["url"]
        u = req_url + "code={c_}".format(c_= "019170")
        print(u)
        ## https://finance.naver.com/search/searchList.nhn?query=%BD%C5%C7%B3%C1%A6%BE%E0
        sess = requests.Session()

        try:

            html = sess.get(url= u)
        except requests.exceptions.ConnectionError as err:
            print(err)
        else:
            if html.status_code == 200 and html.ok:
                self.chrome_obj.get(url= u)
                self.chrome_obj.implicitly_wait(time_to_wait=3)

                # content > div.section.inner_sub > iframe:nth-child(4)

                self.chrome_obj.switch_to.frame(self.chrome_obj.find_elements_by_name(name="day")[1])

                page_source = self.chrome_obj.page_source
                bs_object = BeautifulSoup(page_source, "html.parser")
                result = bs_object.select("table.type2 > tbody > tr")[2:]
                """ 날짜/ 종가/ 전일비/ 시가/ 고가/ 저가/ 거래
                """

                for i in result:
                    key_field = {
                        "날짜": None, "종가": None, "전일비": None, "시가": None, "고가": None, "저가": None, "거래": None
                    }
                    datas = i.select("td")
                    if len(datas) != 1:
                        result = [str(x.text).replace("\n", "").replace("\t", "") for x in datas]
                        key_field["날짜"]  = result[0]
                        key_field["종가"]  = result[1]
                        key_field["전일비"] = result[2]
                        key_field["시가"]  = result[3]
                        key_field["고가"]  = result[4]
                        key_field["저가"]  = result[5]
                        key_field["거래"]  = result[6]
                        self.type_convert(key_field)
                        print(key_field)
                        self.total_data.append(key_field)

                self.xl_file_write()

        finally:
            sess.close()

    def type_convert(self, key_field):
        """

        :param key_field:
        :return:
        """
        for k in key_field.keys():
            if k != "날짜":
                key_field[k] = int(key_field[k].replace(",", ""))

    def xl_file_write(self):
        result = os.path.isfile(RetXlObj.FILE_PATH)
        xl_alpha_key = ["A", "B", "C", "D", "E", "F", "G"]
        xl_num_key = 2

        if result:
            load_wb = load_workbook(filename=RetXlObj.FILE_PATH, data_only=True)
            # 시트 이름으로 불러오기
            load_ws = load_wb["Sheet"]
            for i in self.total_data:
                print(i)
                for k, v in zip(xl_alpha_key, dict(i).values()):
                    load_ws[k + str(xl_num_key)] = v

                xl_num_key += 1

            load_wb.save(filename=RetXlObj.FILE_PATH)
            load_wb.close()

    # 소멸자
    def __del__(self):
        try:
            self.chrome_obj.close()
        except:
            pass
        else:
            print("selenium object close !!")

    @classmethod
    def get_config(cls):
        """

        :return:
        """
        file_path = "../Config/info.yml"
        result = os.path.isfile(path=file_path)

        if result:
            with open(file_path, "r", encoding="utf-8") as fr:
                url_information = yaml.safe_load(fr)
                fr.close()

                return url_information
        else:
            exit(1)

    @classmethod
    def get_my_stock_info(cls):
        """

        :return:
        """
        file_path = "../Config/my_stock_info.json"
        result = os.path.isfile(path=file_path)

        if result:
            with open(file_path, "r", encoding="utf-8") as fr:
                stock_information = json.load(fr)
                fr.close()

                return stock_information
        else:
            exit(1)

if __name__ == "__main__":
    obj = PROJ_MAIN_CODE()
    obj.url_requests(searchWord="신풍제약")
    # https://finance.naver.com/search/searchList.nhn?query=%BD%C5%C7%B3