from app import app
import unittest
import os
import tempfile

class BasicTestCase(unittest.TestCase):

  def test_index(self):
    """initial test to ensure flask was set up correctly"""
    tester = app.app.test_client(self)
    response = tester.get('/', content_type = 'html/text')
    self.assertEqual(response.status_code, 404)

  def test_database(self):
    """this ensures that there is a path existing to the database, that the database exists"""
    tester = os.path.exists('flaskr.db')
    self.assertTrue(tester)

class FlaskrTestCase(unittest.TestCase):

  def setUp(self):
    """Set up a blank temp db before each test"""
    self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True
    self.app = app.app.test_client()
    app.init_db()

  def tearDown(self):
    """Delete blank temp db after each test"""
    os.close(self.db_fd)
    os.unlink(app.app.config['DATABASE'])

  def login(self, username, password):
    """Login helper function"""
    return self.app.post('/login', data=dict(
        username=username,
        password=password
    ),follow_redirects=True)

  def logout(self):
    """logout helper function"""
    return self.app.get('/logout', follow_redirects=True)

# Assert functions

  def test_empty_db(self):
    """ensure database contains no data"""
    rv = self.app.get('/')
    assert b'No entries in here so far' in rv.data

  def test_login_logout(self):
    """test login and logout using the helper functions defined above"""
    rv = self.login(app.app.config['USERNAME'], app.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = self.logout()
    assert b'You were logged out' in rv.data
    rv = self.login(app.app.config['USERNAME'] + 'x', app.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = self.login(app.app.config['USERNAME'], app.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data

    def test_messages(self):
      """Ensure a user can post messages"""
      self.login(app.app.config['USERNAME'], app.app.config['PASSWORD'])
      rv = self.app.post('/add', data=dict(
          title = '<Hello>',
          text= '<strong>HTML<strong> allowed here'
      ), follow_redirects=True)
      assert b'No entries in here so far' not in rv.data
      assert b'&lt;Hello&gt;' in rv.data
      assert b'<strong>HTML<strong> allowed here' in rv.data


if __name__ == '__main__':
  unittest.main()
