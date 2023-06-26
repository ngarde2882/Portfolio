import unittest
from client3 import getDataPoint, getRatio

class ClientTest(unittest.TestCase):
  def test_getDataPoint_calculatePrice(self):
    quotes = [
      {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]
    """ ------------ Add the assertion below ------------ """
    for quote in quotes:
      dataPoint = (quote["stock"], quote["top_bid"]["price"], quote["top_ask"]["price"], (quote["top_bid"]["price"] + quote["top_ask"]["price"])/2)
      self.assertEqual(getDataPoint(quote), dataPoint)

  def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
    quotes = [
      {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]
    """ ------------ Add the assertion below ------------ """
    for quote in quotes:
      dataPoint = (quote["stock"], quote["top_bid"]["price"], quote["top_ask"]["price"], (quote["top_bid"]["price"] + quote["top_ask"]["price"])/2)
      self.assertEqual(getDataPoint(quote), dataPoint)


  """ ------------ Add more unit tests ------------ """
  def test_getDataPoint_calculatePriceBidEqualToAsk(self):
    quotes = [
      {'top_ask': {'price': 120.48, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]
    for quote in quotes:
      dataPoint = (quote["stock"], quote["top_bid"]["price"], quote["top_ask"]["price"], (quote["top_bid"]["price"] + quote["top_ask"]["price"])/2)
      self.assertEqual(getDataPoint(quote), dataPoint)
  
  def test_getRatio_calculateAGreaterThanB(self):
    prices = {"ABC":119.84, "DEF":119.775}
    self.assertEqual(getRatio(prices['ABC'], prices['DEF']), prices['ABC']/prices['DEF'])
  
  def test_getRatio_calculateALessThanB(self):
    prices = {"ABC":119.64, "DEF":119.78}
    self.assertEqual(getRatio(prices['ABC'], prices['DEF']), prices['ABC']/prices['DEF'])
  
  def test_getRatio_calculateAEqualToB(self):
    prices = {"ABC":119.84, "DEF":119.84}
    self.assertEqual(getRatio(prices['ABC'], prices['DEF']), 1)

  def test_getRatio_calculateBZero(self):
    prices = {"ABC":119.84, "DEF":0}
    self.assertIsNone(getRatio(prices['ABC'], prices['DEF']))
  
  def test_getRatio_calculateAZero(self):
    prices = {"ABC":0, "DEF":119.775}
    self.assertEqual(getRatio(prices['ABC'], prices['DEF']), 0)




if __name__ == '__main__':
    unittest.main()
