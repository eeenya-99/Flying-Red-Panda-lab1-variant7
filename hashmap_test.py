import unittest
from hypothesis import given,  strategies

from hashmap import HashMap


def is_even(value):
    if (not type(value) is str) and (value % 2 == 0):
        return value % 2 == 0
    return False


class TestFoo(unittest.TestCase):

    def test_init(self):
        hm = HashMap(size=45)
        self.assertEqual(hm.bucket_size, 45)

        hm = HashMap({2: 'abc', 'omiga': 43, 7: 'cba', 'ocean': 66})
        hKey = hm.hashFuction(2)
        self.assertEqual(hm.bucket[hKey].value, 'abc')
        # hm.hashFuction(7) == hm.hashFuction(2)
        self.assertEqual(hm.bucket[hKey].next.value, 'cba')

        hKey = hm.hashFuction('omiga')
        self.assertEqual(hm.bucket[hKey].value, 43)
        # hm.hashFuction('omiga') == hm.hashFuction('ocean')
        self.assertEqual(hm.bucket[hKey].next.value, 66)

    def test_hashFuction(self):
        hm = HashMap()
        self.assertEqual(hm.hashFuction(2), 9)
        self.assertEqual(hm.hashFuction(7), 9)
        self.assertEqual(hm.hashFuction('omiga'), 1)
        self.assertEqual(hm.hashFuction(2.14), 9)

    def test_add(self):
        hm = HashMap()
        hm.add(2, 'abc')
        self.assertEqual(hm.access_member(2), 'abc')
        hm.add(2, 100)
        self.assertEqual(hm.access_member(2), 100)

    def test_remove(self):
        hm = HashMap({2: 'abc', 'omiga': 43, 7: 'cba', 'ocean': 66, 12: 'bca'})
        hm.remove(17)
        self.assertEqual(len(hm.key_existed), 5)

        hm.remove(12)
        self.assertEqual(len(hm.key_existed), 4)

        hm.remove('omiga')
        # hm.hashFuction('omiga') == hm.hashFuction('ocean')
        hKey = hm.hashFuction('omiga')
        self.assertEqual(hm.bucket[hKey].key, 'ocean')
        self.assertEqual(hm.bucket[hKey].value, 66)
        self.assertEqual(hm.bucket[hKey].next, None)

        # key 9 doesn't exist
        hm.remove(9)
        hKey = hm.hashFuction(9)
        self.assertEqual(hm.bucket[hKey], hm.bucket_init)

    def test_access_size(self):
        hm = HashMap({2: 'abc', 'omiga': 43, 7: 'cba', 'ocean': 66})
        self.assertEqual(hm.access_size(), 4)
        hm.remove('ocean')
        self.assertEqual(hm.access_size(), 3)

    def test_access_member(self):
        hm = HashMap({2: 'abc', 'omiga': 43, 7: 'cba'})
        self.assertEqual(hm.access_member(7), 'cba')
        self.assertEqual(hm.access_member(100), None)

    def test_dict_to_hash(self):
        hm = HashMap()
        dict = {'omiga': 43, 7: 'cba', 'ocean': 66, 8: 'hello'}
        hm.dict_to_hash(dict)
        self.assertEqual(hm.access_member(7), 'cba')
        self.assertEqual(hm.access_size(), 4)

        hm.dict_to_hash({4: 'four'})
        self.assertEqual(hm.access_member(4), 'four')
        self.assertEqual(hm.access_size(), 5)

    def test_hash_to_dict(self):
        hm = HashMap()
        hm.add('omiga', 10)
        hm.add(2, 'abc')
        hm.add('omiga', 1000)
        hm.add('ocean', 2000)
        self.assertEqual(len(hm.key_existed), 3)
        self.assertEqual(
            hm.hash_to_dict(),
            {'omiga': 1000, 2: 'abc', 'ocean': 2000})

        hm = HashMap()
        self.assertEqual(
            hm.hash_to_dict(), {})

    def test_filter(self):
        # test: function is None
        dict = {'a': 3.14, 'b': 43, 'c': 22, 'd': 66, 'e': 'hello'}
        hm = HashMap(dict)
        hm.filter()
        self.assertEqual(hm.hash_to_dict(), dict)

        # test: even
        hm = HashMap(dict)
        hm.filter(is_even)
        self.assertEqual(hm.hash_to_dict(), {'c': 22, 'd': 66})

        # test: the first letter of the value is not 'n'/'c'/'t'
        dict = {'a': 'tiger', 'b': 'rabbit',
                'c': 'cat', 'd': 'dog', 'e': 'duck'}
        hm = HashMap(dict)
        hm.filter(lambda x: x[0] in 'nct')
        self.assertEqual(hm.hash_to_dict(), {'a': 'tiger', 'c': 'cat'})

    def test_map(self):
        # test: function is None
        hm = HashMap({'a': 3.14, 'b': 43, 'c': 22, 'd': 66, 'e': 'hello'})
        hm.map()
        self.assertEqual(
            hm.hash_to_dict(),
            {'a': 3.14, 'b': 43, 'c': 22, 'd': 66, 'e': 'hello'})

        # test: same dictionary with same function
        hm1 = HashMap({1: 'a', 2: 'b'})
        hm2 = HashMap({2: 'b', 1: 'a'})
        self.assertEqual(hm1.hash_to_dict(), hm2.hash_to_dict())
        hm1.map(ord)
        hm2.map(ord)
        self.assertEqual(hm1.hash_to_dict(), {1: 97, 2: 98})
        self.assertEqual(hm1.hash_to_dict(), hm2.hash_to_dict())

        # test: function : str
        hm = HashMap({'a': 3.14, 'b': 43, 'c': 22, 'd': 66, 'e': 'hello'})
        hm.map(str)
        self.assertEqual(
            hm.hash_to_dict(),
            {'a': '3.14', 'b': '43', 'c': '22', 'd': '66', 'e': 'hello'})

        # test: function : lambda x: x+2
        hm = HashMap({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
        hm.map(lambda x: x+2)
        self.assertEqual(
            hm.hash_to_dict(), {'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7})

    def test_reduce(self):
        hm = HashMap({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
        hmReduce = hm.reduce(lambda x, y: x+y, 0)
        self.assertEqual(hmReduce, 15)

        hm = HashMap({1: 'Hello', 2: 'This', 3: 'Is', 4: 'A', 5: 'Dictionary'})
        hmReduce = hm.reduce(lambda x, y: x+y, '')
        self.assertEqual(hmReduce, 'HelloThisIsADictionary')

    def test_iter(self):
        dict = {'a': 3.14, 'b': 43, 'c': 22, 'd': 66, 'e': 'hello'}
        hm = HashMap(dict)
        res_out = {}
        res_in = {}
        for node_out in hm:
            for node_in in hm:
                res_in[node_in.key] = node_in.value
            self.assertEqual(dict, res_in)
            res_in.clear()

            res_out[node_out.key] = node_out.value
        self.assertEqual(dict, res_out)

        res = {}
        for node in hm:
            res[node.key] = node.value
        self.assertEqual(dict, res)

    @given(
        dictA=strategies.dictionaries(
            strategies.integers(), strategies.integers()),
        dictB=strategies.dictionaries(
            strategies.integers(), strategies.integers()),
        dictC=strategies.dictionaries(
            strategies.integers(), strategies.integers()),
        )
    def test_monoid_associativity(self, dictA, dictB, dictC):
        hmA1 = HashMap(dictA)
        hmB1 = HashMap(dictB)
        hmC1 = HashMap(dictC)
        hmA2 = HashMap(dictA)
        hmB2 = HashMap(dictB)
        hmC2 = HashMap(dictC)
        # (a•b)•c = a•(b•c)
        hmA1.concat(hmB1)
        hmA1.concat(hmC1)
        # (a•b)•c = a•(b•c)
        hmB2.concat(hmC2)
        hmA2.concat(hmB2)
        self.assertEqual(hmA1.hash_to_dict(), hmA2.hash_to_dict())

    @given(dict=strategies.dictionaries(
        strategies.integers(), strategies.integers()))
    def test_monoid_identify(self, dict):
        hmA = HashMap(dict)
        hmB = HashMap(dict)
        hm = HashMap({0: 'test'})
        hm.empty()
        # a•e = a
        hmA.concat(hm)
        self.assertEqual(hmA.hash_to_dict(), dict)
        # e•a = a
        hm.concat(hmB)
        self.assertEqual(hm.hash_to_dict(), dict)
