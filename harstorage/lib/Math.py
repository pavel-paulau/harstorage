import math

class Aggregator():

    """
    Test results aggregation

    """

    def __init__(self):
        None

    def average(self, results):
        """
        @parameter results - a list of test results

        @return - the average value
        """

        try:
            num = len( results )
            total_sum = sum(results)
            return int(round(total_sum / num, 0))
        except TypeError:
            return "n/a"

    def minimum(self, results):
        """
        @parameter results - a list of test results

        @return - the minimum value
        """

        return min(results)

    def maximum(self, results):
        """
        @parameter results - a list of test results

        @return - the maximum value
        """

        return max(results)

    def percentile(self, results, percent, key=lambda x:x):
        """
        @parameter results - a list of test results
        @parameter percent - a float value from 0.0 to 1.0
        @parameter key - optional key function to compute value from each element of N.

        @return - the percentile
        """

        data = sorted(results)

        k = (len(data) - 1) * percent
        f = math.floor(k)
        c = math.ceil(k)

        if f == c:
            return key(data[int(k)])
        else:
            try:
                return key(data[int(f)]) * (c - k) + key(data[int(c)]) * (k - f)
            except TypeError:
                return "n/a"

class Histogram():

    """
    Statistical histograms based on Sturges rule

    """

    def __init__(self, data):
        """
        Initialize histogram parameters
        """

        self.data = sorted(data)
        self.size = len(self.data)
        self.classes = round(1.0 + 3.32 * math.log10(self.size))
        self.max_value = max(self.data)
        self.min_value = min(self.data)
        self.step = (self.max_value - self.min_value) / self.classes

        self.classes = min(float(len(self._borders())), self.classes)
        self.step = (self.max_value - self.min_value) / self.classes

    def _borders(self):
        """
        Class (column) borders
        """

        borders = set()

        step = self.min_value + self.step

        borders.add(self.data[0])

        for value in self.data:
            if value >= step:
                borders.add(value)
                step += self.step
        return borders

    def midpoints(self):
        """
        Class (column) midpoints
        """

        midpoints = list()

        for klass in range(int(self.classes)):
            midpoint = self.min_value + self.step * (klass + 0.5)
            midpoints.append(round(midpoint, 1))

        return midpoints

    def frequencies(self):
        """
        Class (column) frequencies
        """

        freq = list()

        for i in range(int(self.classes)):
            freq.append(0)

        step = self.min_value + self.step

        index = 0

        for value in self.data:
            if value < step:
                freq[index] += 1
            else:
                step += self.step
                if value == self.max_value:
                    step += 1
                try:
                    freq[index+1] += 1
                except:
                    freq[index] += 1
                index += 1

        return freq