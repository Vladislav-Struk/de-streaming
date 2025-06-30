"""Import os."""
import os
import queue
import time

import pandas as pd

aggregated_data = pd.DataFrame()
streams = queue.Queue()
emulating_of_data = False

COUNT_OF_RECORDS = 5
FREQUENCY_OF_EMULATING = 1
TIME_OF_DELAYING = 30
COUNT_OF_RECORDING = 40


def emulate_of_data(dataset: str):
    """Emulating of datas."""
    print('Начало эмуляции записей:')
    set_of_records = pd.read_csv(dataset, nrows=COUNT_OF_RECORDING)
    j = 0
    for i in range(0, len(set_of_records), COUNT_OF_RECORDS):
        j = j+1
        print(f'Эмуляция {j}-х {COUNT_OF_RECORDS} записей')
        records = set_of_records.iloc[i:i+COUNT_OF_RECORDS]
        for _, record in records.iterrows():
            streams.put(record.to_dict())
        time.sleep(FREQUENCY_OF_EMULATING)
    global emulating_of_data
    emulating_of_data = True


def grouping_of_data(dataset):
    """Group of datas."""
    filtered = dataset[(dataset['Price'] >= 5000) |
                       (dataset['LivingArea'] >= 20)]
    filtered.loc[:, 'Avg_price_per_square'] = filtered.apply(lambda x:
                                                             1/x['Price'],
                                                             axis=1)
    group_set = filtered.groupby(['Type', 'District'])
    group_set = group_set.agg(avg_price=('Price', 'mean'),
                              avg_living_area=('LivingArea', 'mean'),
                              advertisement_count=('Price', 'count'),
                              avg_price_per_square=('Avg_price_per_square',
                                                    'mean'))
    return group_set


def handling_of_data(path_to_file: str):
    """Aggregate of datas and writing to csv-file."""
    buffer = []
    global aggregated_data
    while not (emulating_of_data and streams.empty()):
        record_of_streams = streams.get()
        buffer.append(record_of_streams)
        buffer_frame = pd.DataFrame(buffer)
        aggregated_data = pd.concat([aggregated_data,
                                     grouping_of_data(buffer_frame)])
        aggregated_data = aggregated_data.groupby(['Type', 'District'])
        aggregated_data = aggregated_data.agg({'avg_price': 'mean',
                                               'avg_living_area': 'mean',
                                               'advertisement_count': 'count',
                                               'avg_price_per_square': 'mean'})
        if not aggregated_data.empty and os.path.exists(path_to_file):
            aggregated_data.to_csv('portugal_listings_out.csv', mode='a',
                                   header=False)
        else:
            aggregated_data.to_csv('portugal_listings_out.csv', mode='w',
                                   header=True)
        time.sleep(TIME_OF_DELAYING)
