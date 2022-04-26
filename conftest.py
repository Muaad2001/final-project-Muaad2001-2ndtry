# https://stackoverflow.com/questions/49028611/pytest-cannot-find-module
# https://stackoverflow.com/a/49033954/10852609
'''
What happens here: when pytest discovers a conftest.py, it modifies sys.path 
so it can import stuff from the conftest module. So, since now an empty conftest.py is found in rootdir, 
pytest will be forced to append it to sys.path. 
The side effect of this is that this flaskr module becomes importable.
'''
