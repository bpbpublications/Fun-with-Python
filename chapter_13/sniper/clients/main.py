from . import __all__


class Main:
    def collect_results(self, phrase):
        all_data = []
        for client in __all__:
            c = client()
            result = c.find_items(phrase)
            if result:
                all_data.extend(result)
        all_data.sort(key=lambda x: float(x.get("price", 0)))
        return all_data
