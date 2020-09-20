import pandas as pd
import os

import altair as alt
import altair_viewer
import ipython_genutils
class ReadData:

    def __init__(self):
        self.file_path = "../ResultXlFile/result.xlsx"

    def target_file_read(self):
        """

        :return:
        """
        result = os.path.isfile(self.file_path)

        if result:
            ws = pd.read_excel(open(self.file_path, "rb"), sheet_name="Sheet")
            df = pd.DataFrame({
                "날짜": ws["날짜"],
                "종가": ws["종가"],
                "시가": ws["시가"]
            })

            chart = alt.Chart(df, width=800, height=500,title="신풍제약-시세").mark_bar(
                font="consolas",
                fontSize=16
            ).encode(
                x="날짜",
                y="종가"
            )

            rule = alt.Chart(df).mark_rule(color="red").encode(
                y = "mean(종가)"
            )

            (chart+rule).save("./test.html")

if __name__ == "__main__":
    obj = ReadData()
    obj.target_file_read()