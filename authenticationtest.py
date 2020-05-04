from user import app
import unittest
import json
import  base64

class JunitTest(unittest.TestCase):
   def test_authentication_req (self):
    tester = app.test_client(self)
    app.config['TESTING'] = True
    # valid_credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
    # response = self.app.get('/user', headers={'Authorization': 'Basic ' + valid_credentials})
    #data1 = '{“name”: “Shovon”, “balance”: 100}'
    # response = tester.get('/user7', data = data1)
    # print("Testing scenario: Cannot get user details without  basic authentication")
    # print("status_code:")
    # print(response.status_code)
    # self.assertEqual(response.status_code,200)
    data = {"email_address": 'karpe99999@yahoo.com', "first_name": 'admin', "password":'Network!7!', "last_name":'jj'}
    # {
    #
    # 	"email_address": "karpe@yahoo.com",
    # 	"first_name": "user",
    # 	"id": "f6921112-000d-4df5-937f-68788512c606",
    # 	"password": "Network!7!",
    # 	"last_name": "lname7"
    # }

    #response = tester.post("/auth/register", data={"username":, "password": "password"})
    response = tester.post(
        "/user", data=json.dumps(data)
    )
    print(response.status_code)
    valid_credentials = base64.b64encode(b'karpe99999@yahoo.com:Network!7!').decode('utf-8')
    response1 = tester.get('/user', headers={'Authorization': 'Basic ' + valid_credentials})
    print(response1.status_code)
    #varo = response.status_code

class JunitTest1(unittest.TestCase):
   def test_create_user (self):
    tester = app.test_client(self)
    app.config['TESTING'] = True

    data = {"email_address": 'karpe99999@yahoo.com', "first_name": 'admin', "password":'Network!7!', "last_name":'jj'}

    response = tester.post(
        "/user", data=json.dumps(data)
    )
    print(response)
    self.assertEqual(response.status_code, 200)

    #varo = response.status_code

class JunitTest2(unittest.TestCase):
   def test_read_user (self):
    tester = app.test_client(self)
    app.config['TESTING'] = True

    valid_credentials = base64.b64encode(b'karpe99999@yahoo.com:Network!7!').decode('utf-8')
    response = tester.get('/user', headers={'Authorization': 'Basic ' + valid_credentials})
    print(response)
    self.assertEqual(response.status_code, 200)
    #varo = response.status_code


class JunitTest3(unittest.TestCase):
   def test_update_user (self):
    tester = app.test_client(self)
    app.config['TESTING'] = True
    data = {"email_address": 'karpe99999@yahoo.com', "first_name": 'admin', "password": 'Network!7!', "last_name": 'jj'}
    valid_credentials = base64.b64encode(b'karpe99999@yahoo.com:Network!7!').decode('utf-8')
    response = tester.put('/user', data=json.dumps(data), headers={'Authorization': 'Basic ' + valid_credentials})
    print(response)
    self.assertEqual(response.status_code, 204)
    #varo = response.status_code

class JunitTest4(unittest.TestCase):
   def test_create_user1 (self):

    app.config['TESTING'] = True

    #data = {"email_address": 'karpe99999@yahoo.com', "first_name": 'admin', "password":'Network!7!', "last_name":'jj'}
    # data = {
    #     "vendor": "Northeastern University",
    #     "bill_date": "2020-01-06",
    #     "due_date": "2020-01-12",
    #     "amount_due": 7000.51,
    #     "categories": [
    #         "college",
    #         "ye",
    #         "spring2020"
    #     ],
    #     "paymentStatus": "paiid77"
    # }
    # valid_credentials = base64.b64encode(b'karpe99999@yahoo.com:Network!7!').decode('utf-8')
    # response = tester.post(
    #     "/bill", data=json.dumps(data), headers={'Authorization': 'Basic ' + valid_credentials}
    # )
    # print(response)
    # self.assertEqual(response.status_code, 200)













if __name__ == '__main__':
    # unittest.main()
    print("create results")
    suite = unittest.TestLoader().loadTestsFromTestCase(JunitTest1)
    unittest.TextTestRunner().run(suite)
    # print("read results")
    # suite = unittest.TestLoader().loadTestsFromTestCase(JunitTest2)
    # unittest.TextTestRunner().run(suite)
    # print("update results")
    # suite = unittest.TestLoader().loadTestsFromTestCase(JunitTest3)
    # unittest.TextTestRunner().run(suite)
    # print("******************************************************************************************")
    # # print("create bill")
    # # suite = unittest.TestLoader().loadTestsFromTestCase(JunitTest4)
    # # unittest.TextTestRunner().run(suite)