from plugins.fscan.fscan import FscanPlugin

def test_parse():
    content = '\r\n124.221.120.144:22 open'
    FscanPlugin.parse(content)