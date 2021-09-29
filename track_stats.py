import json
import pandas


def create_table():
    stats_df = pandas.DataFrame(columns=ref_list["columns"])
    print(stats_df.columns)


if __name__ == "__main__":
    with open("lists.json") as f:
        ref_list = json.load(f)

    create_table()