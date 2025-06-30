"""Import threading."""
from threading import Thread

from streaming import emulate_of_data, handling_of_data


def main():
    """Run threads."""
    dataset_path_input = 'portugal_listinigs.csv'
    dateset_path_output = 'portugal_listings_out.csv'
    Thread(target=emulate_of_data, args=(dataset_path_input,),
           daemon=True).start()
    Thread(target=handling_of_data(dateset_path_output)).start()


if __name__ == '__main__':
    main()
