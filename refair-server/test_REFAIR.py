from REFAIR import intersection


class TestIntersection:
    
    def test_intersection_with_both_lists_empty(self):
        first_list = []
        second_list = []

        result = intersection(first_list, second_list)

        assert result == []

    def test_intersection_with_first_list_empty(self):
        first_list = []
        second_list = ["Feature1", "Feature2"]

        result = intersection(first_list, second_list)

        assert result == []

    def test_intersection_with_second_list_empty(self):
        first_list = ["Feature1", "Feature2"]
        second_list = []

        result = intersection(first_list, second_list)

        assert result == []

    def test_intersection_with_no_element_in_common(self):
        first_list = ["Feature1", "Feature2"]
        second_list = ["Feature3"]

        result = intersection(first_list, second_list)

        assert result == []

    def test_intersection_with_one_element_in_common(self):
        first_list = ["Feature1", "Feature2"]
        second_list = ["Feature1"]

        result = intersection(first_list, second_list)

        assert result == ["Feature1"]

