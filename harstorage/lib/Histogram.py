import math

class Histogram():

    """
    Statistical histograms based on Sturges rule

    """

    def __init__(self, data):
        """
        Initialize histogram parameters
        """

        self.data       = sorted(data)
        self.size       = len(self.data)
        self.classes    = round(1.0 + 3.32 * math.log10(self.size))
        self.max_value  = max(self.data)
        self.min_value  = min(self.data)
        self.step       = (self.max_value - self.min_value) / self.classes

        self.classes    = min(float(len(self._borders())), self.classes)
        self.step       = (self.max_value - self.min_value) / self.classes



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