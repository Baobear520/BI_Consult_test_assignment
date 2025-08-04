import unittest
from main import filter_ids


class FilteredListTestCase(unittest.TestCase):
    def setUp(self):
        self.recom_ids = [2, 3, 1]
        self.seen_ids = [3, 10, 20]
        self.filtered_ids = filter_ids(self.recom_ids, self.seen_ids)
    
    def test_correct_filtering(self):
        self.assertEqual(self.filtered_ids, [2, 1])
    
    def test_maintains_order(self):
        # Test that order is preserved from original list
        self.assertEqual(self.filtered_ids.index(2), 0)
        self.assertEqual(self.filtered_ids.index(1), 1)
    
    def test_excluded_elements(self):
        for item in self.seen_ids:
            self.assertNotIn(item, self.filtered_ids)
    
    def test_empty_lists(self):
        self.assertEqual(filter_ids([], []), [])
        self.assertEqual(filter_ids([1, 2, 3], []), [1, 2, 3])
        self.assertEqual(filter_ids([], [1, 2, 3]), [])

    def test_no_overlap(self):
        self.assertEqual(filter_ids([1, 2, 3], [4, 5, 6]), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
