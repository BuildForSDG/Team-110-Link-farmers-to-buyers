from .src import app
import unittest

class FlaskTestCase(unittest.TestCase):
    def test_reg(self):
        '''Ensure that registration works'''
        tester = app.test_client(self)  # creating the test client
        response = tester.get('/register', content_type='application/json')
        # calling the register route
        self.assertEqual(response.status_code, 400)


    def test_successful_reg(self):
        '''Testing successful registration'''
        tester = app.test_client(self)  # creating the test client
        response = tester.post('/register', data=dict(full_name='admin',
                               phone='0902', email='a', password='password',
                               content_type='application/json'))
        # calling the register route
        self.assertIn(b'New User added', response.data)

if __name__ == "__main__":
    unittest.main()

# if __name__ == "__main__":
#     app.run()
