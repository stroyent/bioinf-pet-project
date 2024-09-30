import pandas as pd


csv_file_df = pd.read_csv("test_example_missing_col_2.csv", sep=';')


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


table_array = parse_csv(csv_file_df)
table_array
