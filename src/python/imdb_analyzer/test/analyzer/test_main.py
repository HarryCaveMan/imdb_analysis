# insert analyzer package root
import sys,os
file_dir = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,os.path.abspath(file_dir+'../../..'))

def test_main():
    import analyzer.__main__ as pkg_main