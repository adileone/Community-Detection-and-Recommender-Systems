from birdy.twitter import UserClient
import json

ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''


client = UserClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_SECRET)


def getFollowTimelines(screen_name, file_name, follow, ids=None, num=1):
    
    if((follow != 'followers') & (follow != 'following') & (follow != 'all')):
        return 'followers? following? all?'
        
    if ((ids == None) & (follow=='followers')) :
        follow_ids=client.api.followers.ids.get(screen_name=screen_name)
        ids = follow_ids.data['ids']
        print('number of',follow,': ', len(ids))
    
    if ((ids == None) & (follow=='following')) :
        follow_ids=client.api.friends.ids.get(screen_name=screen_name)
        ids = follow_ids.data['ids']
        print('number of',follow,': ', len(ids))
        
    if ((ids == None) & (follow=='all')) :
        following_ids=client.api.friends.ids.get(screen_name=screen_name)
        followers_ids=client.api.followers.ids.get(screen_name=screen_name)
        ids1 = following_ids.data['ids']
        ids2 = followers_ids.data['ids']
        ids = list(set(ids1+ids2))
        target = client.api.users.show.get(screen_name=screen_name)
        ids.append(target.data['id'])
        print('number of',follow,': ', len(ids))    

    if not ids:
        print('done')
        return

    id=ids[0]
    ids.pop(0)
        
    number_of_tweets=client.api.users.show.get(id=id).data['statuses_count']
    print(num,': getting ',id, ' timeline, number of tweets: ', number_of_tweets)
       
    pages = int(number_of_tweets/20)+1

    if (pages>1):
            
        if (pages>30):
            print('troppi Tweet, prendo solo i 600 più recenti')
            pages=30
            
        for i in range(1,pages+1):
            print(id, '<----------------------------')
                
            try:
                data=client.api.statuses.user_timeline.get(id=id, page=i)
        
                try: 
                    with open(file_name) as data_file:
                        old_data = json.load(data_file)
                        data1 = old_data + data.data
                    with open(file_name, 'w') as outfile:
                        json.dump(data1, outfile)
            
                except Exception as err:
                    with open(file_name, 'w') as outfile:
                        json.dump(data.data, outfile)

                    
            except Exception as err:
                print(err, '\n')
                print("Skippo utente id=",id, ' perchè profilo privato')
                num=num+1
                return getFollowTimelines(screen_name,file_name,follow,ids,num)
        
        num=num+1
        return getFollowTimelines(screen_name,file_name,follow,ids,num)
                    
    else:
        try:
            data=client.api.statuses.user_timeline.get(id=id)
                
            try: 
                with open(file_name) as data_file:
                    old_data = json.load(data_file)
                    data1 = old_data + data.data
                with open(file_name, 'w') as outfile:
                    json.dump(data1, outfile)
            
            except Exception as err:
                with open(file_name, 'w') as outfile:
                    json.dump(data.data, outfile)

        except Exception as err:
            print(err, '\n')
            print("Skippo utente id=",id, ' perchè profilo privato')
            num=num+1
            return getFollowTimelines(screen_name,file_name,follow,ids,num)                    
    
    num=num+1
    return getFollowTimelines(screen_name,file_name,follow,ids,num)

