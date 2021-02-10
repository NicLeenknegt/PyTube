import abc

class ICommand(metaclass=abc.ABCMeta):

    def execute(self, *argv):
        self.validate_input(*argv)
        self.run(*argv)

    @abc.abstractmethod
    def validate_input(self, *argv):
        raise NotImplementedError

    @abc.abstractmethod
    def run(self, *argv):
        raise NotImplementedError

    @abc.abstractmethod
    def get_short_option(self) -> str:
        return None

    @abc.abstractmethod
    def get_long_option(self) -> str:
        return None

    def get_options(self) -> [str]:
        options:[str] = []
        if self.get_short_option() is not None:
            options.append(self.get_short_option())
        if self.get_long_option() is not None:
            options.append(self.get_long_option())

        return options
