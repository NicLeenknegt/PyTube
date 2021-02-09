from view.ListView import show_list
from data.repository.SubscriptionRepository import fetch_all_subscriptions
from data.repository.SelectionListRepository import save_sub_to_selection_list
from command.ICommand import ICommand

class ShowSubscriptionsCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 1:
            raise ValueError("illegal format: pytube [--subs|-u]")
    
    def run(self, *argv):
        subs:[Subscription] = fetch_all_subscriptions()
        save_sub_to_selection_list(subs)
        show_list(subs)

    def get_short_option(self) -> str:
        return "-u"

    def get_long_option(self) -> str:
        return "--subs"

