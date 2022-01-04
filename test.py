try:
    from library import app
    import unittest

except Exception as e:
    print("Some issue".format(e))

class FlaskTest(unittest.TestCase):

    #Check for reponse 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)

    #check if content returned is text/html
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        
    # check for Data returned    
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        self.assertTrue(b'Most Popular Books' in response.data)

if __name__ == '__main__':
    unittest.main()
