import csv
import typing
from io import BytesIO, TextIOWrapper


class CSVUtil(object):
    reader_class = csv.DictReader
    writer_class = csv.DictWriter

    @classmethod
    def parse(cls, file_path: str, row_handler: typing.Callable):
        if not isinstance(file_path, str):
            raise TypeError("'file_path' must be a string")

        if not callable(row_handler):
            raise TypeError("'row_handler' must be callable")

        with open(file_path, mode="r", encoding="utf-8-sig") as csv_file:
            csv_reader = cls.reader_class(csv_file)
            print(f'Column names are {", ".join(csv_reader.fieldnames)}')
            for row in csv_reader:
                row_handler(row)
            print(f"Processed {csv_reader.line_num - 1} lines.")

    @classmethod
    def binary_to_list(cls, binary: bytes) -> typing.List[typing.Dict[str, str]]:
        csv_bytes = BytesIO(binary)
        with TextIOWrapper(csv_bytes) as csv_file:
            csv_reader = cls.reader_class(csv_file)
            result_list = list(csv_reader)

        return result_list
