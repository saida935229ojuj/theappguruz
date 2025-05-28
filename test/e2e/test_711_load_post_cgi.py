import pytest
import os

from TestHttpdConf import HttpdConf


class TestStore:

    @pytest.fixture(autouse=True, scope='class')
    def _class_scope(self, env):
        env.setup_data_1k_1m()
        HttpdConf(env).add_vhost_cgi(proxy_self=True, h2proxy_self=True).install()
        assert env.apache_restart() == 0
        yield
        assert env.apache_stop() == 0

    def check_h2load_ok(self, env, r, n):
        assert 0 == r["rv"]
        r = env.h2load_status(r)
        assert n == r["h2load"]["requests"]["total"]
        assert n == r["h2load"]["requests"]["started"]
        assert n == r["h2load"]["requests"]["done"]
        assert n == r["h2load"]["requests"]["succeeded"]
        assert n == r["h2load"]["status"]["2xx"]
        assert 0 == r["h2load"]["status"]["3xx"]
        assert 0 == r["h2load"]["status"]["4xx"]
        assert 0 == r["h2load"]["status"]["5xx"]
    
    # test POST on cgi, where input is read
    def test_710_10(self, env):
        url = env.mkurl("https", "test1", "/echo.py")
        n = 100
        m = 5
        conn = 1
        fname = "data-100k"
        args = [ env.H2LOAD, "-n", "%d" % (n), "-c", "%d" % (conn), "-m", "%d" % (m), 
            "--base-uri=https://%s:%s" % (env.HTTPD_ADDR, env.HTTPS_PORT),
            "-d", os.path.join(env.GEN_DIR, fname),  
            url ]
        r = env.run( args ) 
        self.check_h2load_ok(env, r, n)

    # test POST on cgi via http/1.1 proxy, where input is read
    def test_710_11(self, env):
        url = env.mkurl("https", "test1", "/proxy/echo.py")
        n = 100
        m = 5
        conn = 1
        fname = "data-100k"
        args = [ env.H2LOAD, "-n", "%d" % (n), "-c", "%d" % (conn), "-m", "%d" % (m), 
            "--base-uri=https://%s:%s" % (env.HTTPD_ADDR, env.HTTPS_PORT),
            "-d", os.path.join(env.GEN_DIR, fname),  
            url ]
        r = env.run( args ) 
        self.check_h2load_ok(env, r, n)

    # test POST on cgi via h2proxy, where input is read
    def test_710_12(self, env):
        url = env.mkurl("https", "test1", "/h2proxy/echo.py")
        n = 100
        m = 5
        conn = 1
        fname = "data-100k"
        args = [ env.H2LOAD, "-n", "%d" % (n), "-c", "%d" % (conn), "-m", "%d" % (m), 
            "--base-uri=https://%s:%s" % (env.HTTPD_ADDR, env.HTTPS_PORT),
            "-d", os.path.join(env.GEN_DIR, fname),  
            url ]
        r = env.run( args ) 
        self.check_h2load_ok(env, r, n)


