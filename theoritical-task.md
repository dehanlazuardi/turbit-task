# Theoritical Task

### 1. What is Factory Pattern?

Factory pattern is design pattern to allow adding new implementation without changing too much the existing code. Therefore the code will be easier to maintain and reusable.

### 2. How would you design a generic CSV importer for multiple CSV files? Each CSV file contains three columns with data (date, power, wind speed). The column headers are slightly different for each file. The date format and time zone is also different for each file.

assumption: 
 - example of date difference: USA format v.s. EU format
 - example of column difference: use capital in the first letter v.s. all lower case

To address this issue, we can use factory pattern when parsing the data (implemented in the code below). First we specify the correct parser that we want to use to parse the column name and the date time data. Then object factory (ColumnParserFactory, TimeDateParserFactory) will provide the correct parser. Finally we can parse the data correctly in the parse.py. If we want to add new parser code, we can add the new parser and register them.  

```python
# csv.py

# CSV object 
class CSV:
    def __init__(self, csv_path):
        # read the data
        self._data = read_raw_data(csv_path)

    def register_col_parser(self, column_parser):
        # register new parse and init the parser
        self._col_parser = column_parser(self._data)

    def register_time_date_parser(self, time_date_parser):
        # register new parse and init the parser
        self._time_date_parser = time_date_parser(self._data)

    def parse_data(self):
        # parse the data
        self._data = self._col_parser.parse().get_data()
        self._data = self._time_date_parser.parse().get_data()
    
    def save_data(self):
        # save parsed data
```

```python
# column_parser.py

# column parsers implementation
class ColumnParserTypeA:
    def __init__(self, data):
        self._data = None

    def parse(self):
        # parse the column
    
    def get_data(self):
        # return data 
        
class ColumnParserTypeB:
    def __init__(self, data):
        self._data = None

    def parse(self):
        # parse the column
    
    def get_data(self):
        # return data 

# column parser factory
class ColumnParserFactory:
    def __init__(self):
        self._parsers = {}

    def register_format(self, column_format, parser):
        # record parser
        self._parsers[column_format] = parser

    def get_CSV_parser(self, column_format):
        # return parser if parser is not exist raise value error
        parser = self._parsers.get(column_format)
        if parser == None:
            raise ValueError(column_format)
        return parser
```

```python
# time_date_parser.py

# time date parsers implementation
class TimeDateParserTypeA:
    def __init__(self, data):
        self._data = None

    def parse(self):
        # parse the time date
    
    def get_data(self):
        # return data 
        
class TimeDateParserTypeB:
    def __init__(self, data):
        self._data = None

    def parse(self):
        # parse the time date
    
    def get_data(self):
        # return data 

# time date parser factory
class TimeDateParserFactory:
    def __init__(self):
        self._parsers = {}

    def register_format(self, time_date_format, parser):
        # record parser
        self._parsers[time_date_format] = parser

    def get_CSV_parser(self, time_date_format):
        # return parser if parser is not exist raise value error
        parser = self._parsers.get(time_date_format)
        if parser == None:
            raise ValueError(time_date_format)
        return parser
```

```python
# parse.py

# register column parsers
column_factory = ColumnParserFactory()
column_factory.register_format('col_type_A', ColumnParserTypeA)
column_factory.register_format('col_type_B', ColumnParserTypeB)

# register time date parsers
time_date_factory = TimeDateParserFactory()
time_date_factory.register_format('time_date_type_A', TimeDateParserTypeA)
time_date_factory.register_format('time_date_type_B', TimeDateParserTypeB)


if __name__ == "__main__":
    # get format name from args
    column_format = args.column_format
    time_date_format = args.time_date_format

    # request parser from the parser factory
    column_parser = column_factory.get_CSV_parser(column_format)
    date_time_parser = time_date_factory.get_CSV_parser(time_date_format)

    # parse and save the csv
    csv_object.register_col_parser(column_parser)
    csv_object.register_time_date_parser(date_time_parser)
    csv_object.parse_data()
    csv_object.save_data()
```


### 3. How would you find and fix a bug which occurs only for some data points in some date ranges?
- bug assumption: Bug when cleaning the data, there are several weird result.

- solution: Audit the data first according to a certain criteria, then group/filter the data based on that criteria resulting 2 groups. Frist group is for data that meet all of the filter criteria. Second group is for data which dont meet the criteria. Observe the second group pattern and find the cause of the bug from the group 2, it could be data related or code related.