#goal contract

#take username and password, and result
#take referee usermane and passord, and result
#if user result == referee result && result is negative, then send money to the recipient
#elif user result == referee result && result is positive then send money to the user
#elif (user result != referee result) && (incline result is positive or default is positive or default is to the referee result & its is positive) then send money to recipient

#submission limit = 10 days? default
#help limit = 10days? default

contract_end = ['10/10/2020'] # the goal must be completed by
submission_end = ['10d']      # how long the referee and user have to submit their evaluation
distrubution = ['20d']        # how long after the contract until the money is distributed (note: once send the money cannot be returned)

wager = [100]                 # the money which is lost if the contract is not completed - this is stored in the contract

user = ['Name']
user_password = ['hashedUserPassword']

referee = ['RefereeName']
referee_password = ['hashaedRefereePassword']

referee2 = ['Referee2Name'] # The tie-breaker. Defaults to Incline.
referee2_password = ['hashedRefereepassword'] 

class Contract():
    distribution = '10d'
    def __init__(self, user, userpass, ref, refpass, recipient_key, end_date, wager) -> None:
        self.user = user
        self.userpass = userpass
        self.ref = ref
        self.refpass = refpass
        self.recipient = recipient_key
        self.end_date = end_date
        self.wager = wager
    
