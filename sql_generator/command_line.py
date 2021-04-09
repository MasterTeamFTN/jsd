from os.path import dirname, join
from utils import str2bool
import argparse


class CommandLine:
    def __init__(self):
        this_folder = dirname(__file__)

        defaultSqlOutput = join(join(this_folder, 'srcgen'), "create_db_schema.sql")
        defaultDotOutput = join(join(this_folder, 'srcgen'), 'er_diagram.dot')

        parser = argparse.ArgumentParser(description='Process file locations and types.')
        parser.add_argument('-srcSg', '--sourceSgFile',
                            action="store", dest="sourceFile",
                            help="parh to file where source sg script is stored")
        parser.add_argument('-sql', '--sqlOutputPath',
                            action="store", dest="sqlFile",
                            help="path to file where generated sql script should be stored", default=defaultSqlOutput)
        parser.add_argument('-dot', '--dotOutputPath',
                            action="store", dest="dotFile",
                            help="path to file where generated dot file should be stored", default=defaultDotOutput)
        parser.add_argument("--dot-only", type=str2bool, nargs='?',
                            const=True, default=False, action="store", dest="dotOnly",
                            help="Specify if you only want dot output file.")
        parser.add_argument("--sql-only", type=str2bool, nargs='?',
                            const=True, default=False, action="store", dest="sqlOnly",
                            help="Specify if you only want sql output file.")
        self.args = parser.parse_args()

        # if self.args.sourceFile:
        #     print("You have used '-srcSg' or '--sourceSgFile' with argument: {0}".format(self.args.sourceFile))
        # if self.args.sqlFile:
        #     print("You have used '-sql' or '--sqlOutputPath' with argument: {0}".format(self.args.sqlFile))
        # if self.args.dotFile:
        #     print("You have used '-dot' or '--dotOutputPath' with argument: {0}".format(self.args.dotFile))
        # if self.args.dotOnly:
        #     print("You have used '--dot-only' with argument: {0}".format(self.args.dotOnly))
        # if self.args.sqlOnly:
        #     print("You have used '--sql-only' with argument: {0}".format(self.args.sqlOnly))

        if self.args.dotOnly and self.args.sqlOnly:
            raise argparse.ArgumentTypeError("You can not use '--dot-only' and '--sql-only' together. Use eighter one or none")
