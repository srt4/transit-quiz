__author__ = 'spencert'


class StringSimilarityComparator:

    def get_string_similarity(self, first, second):
        """
        Calculates the similarity between two strings, case-insensitive. The similarity is calculated as a percentage of
        words which occur in both strings, with the length (in words) of the shortest string used as the denominator.

        :param first: The first string to compare.
        :param second: The second string to compare.
        :return: The similarity, as a percentage (0 to 1), between the two strings.
        """

        first_words = first.split(" ")
        second_words = second.split(" ")

        larger = first_words if len(first_words) >= len(second_words) else second_words
        smaller = first_words if len(first_words) < len(second_words) else second_words

        larger = self.__lowercase_list_of_words(larger)
        smaller = self.__lowercase_list_of_words(smaller)

        numerator = 0
        denominator = len(smaller)

        for word in smaller:
            if word in larger:
                numerator += 1

        print str(numerator) + " / " + str(denominator)
        return numerator / float(denominator)

    def __lowercase_list_of_words(self, mixed_case_list):
        return [x.lower() for x in mixed_case_list]
