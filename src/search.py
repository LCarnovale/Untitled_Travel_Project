import re

class Search():
    def __init__(self, items):
        self._items = items
        self._most_recent = []

    # Replaces all contiguous non-alphanumeric characters with a space
    # And converts to lower case
    def _cleanString(self, string):
        return re.sub(r'[\W_]+', ' ', string).lower()

    # Returns a list of all ads mentioning at least one keyword in the search
    # Ordered by increasing score:
    #  score = sum of [(2/3) * frequency of keyword in name +
    #                  (1/3) * frequency of keyword in description]
    #          over all keywords
    def keywordSearch(self, search):
        search = self._cleanString(search)
        search = search.split(' ')

        scores = []

        for ad in self._items:
            title_score = 0.0
            body_score = 0.0

            name = ad.getName()
            name = self._cleanString(name)
            name = name.split(' ')

            desc = ad.getDesc()
            desc = self._cleanString(desc)
            desc = desc.split(' ')

            for keyword in search:
                if len(name) != 0:
                    title_score += (2/3) * name.count(keyword)/len(name)
                if len(desc) != 0:
                    body_score += (1/3) * desc.count(keyword)/len(desc)

            if title_score + body_score != 0:
                scores.append((ad, title_score + body_score))

        scores.sort(key=lambda x: -x[1])

        self._most_recent = scores
        return [x[0] for x in scores]