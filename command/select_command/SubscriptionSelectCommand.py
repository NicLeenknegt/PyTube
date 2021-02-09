from command.ICommand import ICommand
from data.repository.SelectionListRepository import save_videos_to_selection_list
from data.repository.VideoRepository import fetch_all_videos_of_subscription
from view.ListView import show_list
from domain.Video import Video
from domain.Subscription import Subscription

class SubscriptionSelectCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 3:
            raise ValueError("internal error: SubscriptionSelectCommand receives wrong arguments from SelectCommand")     

    def run(self, *argv):
        index:int = argv[0]
        result:[Subscription] = argv[1]

        vids:[Video] = fetch_all_videos_of_subscription(None, result[index].url_name)
        save_videos_to_selection_list(vids)                
        show_list(vids)

    def get_short_option(self) -> str:
        return None

    def get_long_option(self) -> str:
        return "subscription"

