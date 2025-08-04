from typing import List


def filter_ids(source: List[int], filter_out_data: List[int]) -> List[int]:

    filter_set = set(filter_out_data)  # eliminates redundant duplicates
    return [n for n in source if n not in filter_set]


if __name__ == "__main__":
    source = [1, 2, 3, 4, 5]
    filter_out_data = [2, 4]
    print(filter_ids(source, filter_out_data))