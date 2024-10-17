from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from random import randint

import pandas as pd


def trim_column_name(column_name: str):
    new_column_name = column_name.replace(' ', '_')
    new_column_name = new_column_name.replace('-', '_')

    if not new_column_name.isalnum():
        column_name_characters = list(new_column_name)
        column_name_characters_filtered = [
            char for char in column_name_characters if (char.isalnum() or char == '_')]
    new_column_name = ''.join(column_name_characters_filtered)

    return new_column_name


def parse_csv(csv_file_df):
    table_array = []
    csv_file_df = csv_file_df.rename(trim_column_name, axis='columns')

    for column_name, column_data in csv_file_df.items():
        table_array.append({column_name: column_data.to_list()})

    return table_array


def get_intersections(table_array):
    iterative_table = []
    iterative_table.append(table_array[0])

    next_table = []

    for i in range(1, len(table_array)):
        next_column = table_array[i]
        reverse_subtraction_set = set(list(next_column.values())[0])
        for column in iterative_table:
            intersection_set = set(list(column.values())[0]) & set(list(next_column.values())[0])
            intersection_col = {f"{list(column.keys())[0]}_{list(next_column.keys())[0]}": list(intersection_set)}

            subtraction_set = list(set(list(column.values())[0]) - set(list(next_column.values())[0]))
            subtraction_col = {f"{list(column.keys())[0]}": subtraction_set}

            reverse_subtraction_set = reverse_subtraction_set - intersection_set

            next_table.append(intersection_col)
            next_table.append(subtraction_col)
        reverse_subtraction_col = {f"{list(next_column.keys())[0]}": list(reverse_subtraction_set)}

        next_table.append(reverse_subtraction_col)
        iterative_table = next_table.copy()
        next_table.clear()

    return iterative_table


def export_csv(table, filename):
    dict_for_export = {}
    for column in table:
        if len(list(column.values())[0]) > 0:
            dict_for_export[list(column.keys())[0]] = list(column.values())[0]
    export_df = pd.DataFrame.from_dict(dict_for_export, orient="index")
    export_df = export_df.transpose()
    export_path = f"files/result_{filename}"
    export_df.to_csv(export_path, index=False)
    global result_path
    result_path = export_path



origins = ["http://localhost:8080",
           "http://localhost",
           "http://localhost:8080/"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

result_path = ""

def load_sandwiches():
    with open("sandwiches.txt", "r", encoding="utf-8") as source_file:
        current_sandwich = ""
        sandwich_list = []

        for line in source_file:
            if line == "\n":
                sandwich_list.append(current_sandwich)
                current_sandwich = ""
                continue
            current_sandwich += line
    return sandwich_list


def random_sandwich(sandwich_list):
    return sandwich_list[randint(0, len(sandwich_list) - 1)]


loaded_sandwiches = load_sandwiches()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/file/upload-csv")
async def load_csv(file: UploadFile):
    uploaded_csv = pd.read_csv(file.file, sep=';', dtype="string")
    export_csv(get_intersections(parse_csv(uploaded_csv)), file.filename)
    return file

@app.get("/file/download")
def download_file():
    global result_path
    filename = result_path.split(sep='/')[-1]
    headers = {'content-disposition': f'attachment; filename="{filename}"'}
    return FileResponse(result_path, headers=headers)


@app.get("/sammiches")
def get_sandwich():
    return {"sandwich": random_sandwich(loaded_sandwiches)}



