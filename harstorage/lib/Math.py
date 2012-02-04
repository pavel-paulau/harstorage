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
        self.max_value = max(self.data)
        self.min_value = min(self.data)
        
        if self.min_value != self.max_value:
            self.classes = round(1.0 + 3.32 * math.log10(self.size))
        else:
            self.classes = 1
        self.step = (self.max_value - self.min_value) / self.classes

    def ranges(self, reduced=False):
        ranges = list()

        for klass in range(int(self.classes)):
            range_l = int(self.min_value + self.step * klass)
            range_r = int(self.min_value + self.step * (klass + 1))

            if reduced:
                try:
                    order = 1 + int(100 / self.step)
                except:
                    order = 1

                range_l = round(range_l / 1000.0, order)
                range_r = round(range_r / 1000.0, order)

            ranges.append(str(range_l) + " - " + str(range_r))

        return ranges

    def frequencies(self):
        """
        Class (column) frequencies
        """

        frequencies = list()

        for index in range(int(self.classes)):
            frequencies.append(0)

        step = self.min_value + self.step

        index = 0

        for value in self.data:
            if value <= step:
                frequencies[index] += 1
            else:
                while value > step + 1:
                    step += self.step
                    index += 1
                try:
                    frequencies[index+1] += 1
                except:
                    frequencies[index] += 1
 
        for index in range(int(self.classes)):
            frequencies[index] = round(frequencies[index] * 100.0 / self.size, 1)

        return frequencies