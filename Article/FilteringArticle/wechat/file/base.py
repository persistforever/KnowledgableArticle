# -*- encoding = gb18030 -*-
""" Basic class of File Operator """


class BaseFileOperator :

    def reading(self, file_name) :
        """ Read file from file_name(on the disk) to the data_list(in the memory). """
        self.data_list = []
        return self.data_list

    def writing(self, data_list, file_name) :
        """ Write data_list(in the memory) to the file(on the disk) named file_name. """