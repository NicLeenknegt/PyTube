from data.repository.RepositoryDecorator import fetch_request, insert_request, delete_request
from domain.Subscription import Subscription

@fetch_request("select * from subscription")
def fetch_all_subscriptions(cursor) -> [Subscription]:
    fetched_subscriptions:[Subscription] = []
    for row in cursor:
        fetched_subscriptions.append(Subscription(row[0],row[1], row[2]))
    
    return fetched_subscriptions

@insert_request("subscription")
def insert_subscription(sub:Subscription):
    return '( "' + sub.url_name + '","' + sub.url_format + '","' + sub.type + '")'

@fetch_request("select * from subscriptions_w_last_id")
def fetch_all_subs_w_last_id(cursor) -> [Subscription]:
    fetched_subscriptions:[Subscription] = []
    for row in cursor:
        fetched_subscriptions.append(Subscription(row[0],row[1], row[2], row[3]))
    
    return fetched_subscriptions

@delete_request("subscription", "where name = ?")
def delete_sub(cursor, name:str):
    for row in cursor:
        print(row)
    return cursor
