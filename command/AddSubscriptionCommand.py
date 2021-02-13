from controller.SubscriptionController import load_all_videos
from data.repository.SubscriptionRepository import insert_subscription, delete_sub
from command.ICommand import ICommand
from domain.web_driver.SimpleDriver import SimpleDriver
from domain.content_filter.Youtube2020Filter import Youtube2020Filter
from domain.content_converter.YTVideoConverter import YTVideoConverter
from domain.Subscription import Subscription
from sqlite3 import OperationalError, IntegrityError

class AddSubscriptionCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 2:
            raise ValueError("illegal format: pytube [--add-sub|-a] url")
        if "https://www.youtube.com/" not in argv[1]: 
            raise ValueError("illegal argument: given argument is not a supported url")
    
    def run(self, *argv):
        
        url:str = argv[1]

        driver = SimpleDriver()
        content_filter = Youtube2020Filter()
        content_converter = YTVideoConverter()
        url_name:str
        if "/c/" in url:
            url_name = url[len("https://www.youtube.com/c/"):-len("/videos")]
            sub:Subscription = Subscription(url_name, "https://www.youtube.com/c/{0}/videos", "CHANNEL")
        elif "/user/" in url:
            url_name = url[len("https://www.youtube.com/user/"):-len("/videos")]
            sub:Subscription = Subscription(url_name, "https://www.youtube.com/user/{0}/videos", "USER")
        else:
            raise ValueError("unsupported error: the given url is not supported in this version")
        sub.set_filter(content_filter)
        sub.set_driver(driver)
        sub.set_converter(content_converter)

        try:        
            insert_subscription(sub)
        except OperationalError:
            raise ValueError("database failure: something went wrong while inserting a new subscription")
        except IntegrityError as err:
            raise ValueError("database failure: there already exists a subscription with name \"{}\"".format(sub.url_name))

        try:
            load_all_videos(sub)
        except:
            # remove sub if loading videos fails
            delete_sub(sub.name)
            raise

    def get_short_option(self) -> str:
        return "-a"

    def get_long_option(self) -> str:
        return "--add-sub"

