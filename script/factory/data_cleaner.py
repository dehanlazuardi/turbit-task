from .data_clean import cleaner_factory

class DataCleaner:
    def clean(self, data, name: str):
        cleaner = cleaner_factory.get(name)
        cleaner.add_data(data)
        cleaner.clean()
        return cleaner.get_result()