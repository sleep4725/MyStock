from openpyxl import Workbook

class RetXlObj():

    FILE_PATH = "../ResultXlFile/result.xlsx"

    @classmethod
    def get_xl_obj(cls):
        wb_obj = Workbook()
        ws_obj = wb_obj.active
        CELL_LIST = [chr(x)+str(1) for x in range(ord("A"), ord("H"))]
        CELL_KEY  = ["날짜", "종가", "전일비", "시가", "고가", "저가", "거래"]

        for k, v in zip(CELL_LIST, CELL_KEY):
            ws_obj[k] = v

        try:

            wb_obj.save(filename=RetXlObj.FILE_PATH)
        except:
            print("excel file save fail !!")
            exit(1)
        else:
            print("excel file save success !!")
        finally:
            wb_obj.close()