# coding: utf-8
# 运行app
from optparse import OptionParser
from apps import temperature

if __name__ == '__main__':
    usage = "usage: -a: app name"
    parser = OptionParser(usage)
    parser.add_option("-a", "--app", dest="app", help="run app")
    (options, args) = parser.parse_args()
    app_name = options.app
    if not app_name:
        parser.error("need input app name")

    if app_name == 'temperature':
        # 气温分析
        temperature.main()
