import pandas as pd
import os


# write list to csv file
def list_write_csv(path, column_title, list_to_write):
    dataframe_to_write = pd.DataFrame(list_to_write, columns=[column_title])
    with open(path, 'a') as f:
        # if csv file is empty
        if os.stat(path).st_size == 0:
            dataframe_to_write.to_csv(path, index=False)
        else:
            data = pd.read_csv(path, low_memory=False)
            data[column_title] = dataframe_to_write
            data.to_csv(path, index=False)

