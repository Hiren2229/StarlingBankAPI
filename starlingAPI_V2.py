import json
import requests
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.cbook as cbook


class StarlingBankAPI:
    

    ''' Make sure you change the URL and Auth code while using it because
        for production base url and auth code is diffrent'''
    def __init__(self, base_url, auth_code):
        self.base_url = 'https://api-sandbox.starlingbank.com' #For sandBox only for Demo data
        self.auth_code = 'Bearer Your Startlin Bank API key'

    def get_sandbox_accounts(self):
        account_dict = {}
        url = self.base_url+'/api/v2/accounts'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.auth_code
        }
        response = requests.get(url, headers=headers)
        account_data = response.json()
        return account_data


    def get_account_balance(self, account_uid):
        if account_uid:
            balance_details = requests.get(self.base_url+'/api/v2/accounts/'+account_uid+'/balance', 
                                headers= {'Content-Type': 'application/json','Authorization': self.auth_code}).json()

            clearedBalance = balance_details.get('clearedBalance') if balance_details.get('clearedBalance') else None
            if clearedBalance:
                clearedBalance = clearedBalance.get('minorUnits')
            effectiveBalance = balance_details.get('effectiveBalance') if balance_details.get('effectiveBalance') else None
            if effectiveBalance:
                effectiveBalance = effectiveBalance.get('minorUnits')
            pendingTransactions = balance_details.get('pendingTransactions') if balance_details.get('pendingTransactions') else None
            if pendingTransactions:
                pendingTransactions = balance_details.get('minorUnits')                
            acceptedOverdraft = balance_details.get('acceptedOverdraft') if balance_details.get('acceptedOverdraft') else None
            if acceptedOverdraft:
                acceptedOverdraft = acceptedOverdraft.get('minorUnits')
            totalEffectiveBalance = balance_details.get('totalEffectiveBalance') if balance_details.get('totalEffectiveBalance') else None
            if totalEffectiveBalance:
                totalEffectiveBalance = totalEffectiveBalance.get('minorUnits')

            df = pd.DataFrame(columns=['clearedBalance', 'effectiveBalance', 'pendingTransactions', 'acceptedOverdraft', 'totalEffectiveBalance'])
            data_dict = {
                    'clearedBalance' : clearedBalance,
                    'effectiveBalance' : effectiveBalance,
                    'pendingTransactions' : pendingTransactions,
                    'acceptedOverdraft' : acceptedOverdraft,
                    'totalEffectiveBalance' : totalEffectiveBalance
                }
            new_row = pd.DataFrame(data_dict, index=[0])
            BalanceMatrix = pd.concat([df,new_row], ignore_index=True)
            return BalanceMatrix

    def get_bank_identifires(self, account_uid):
        if account_uid:
            identifiers = requests.get(self.base_url+'/api/v2/accounts/'+account_uid+'/identifiers', 
                                headers= {'Content-Type': 'application/json','Authorization': self.auth_code}).json()
            df = {
                'account_num' : [identifiers['accountIdentifier']],
                'short_code' : [identifiers['bankIdentifier']]
            }
            data_frame = pd.DataFrame(df)
            return data_frame

    def get_date_numbers(self):
        list_of_months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
        current_date = datetime.now()
        return {'year' : str(current_date.year), 
                'month' : list_of_months[current_date.month - 1]}

    def get_account_spednig_insights(self, account_uid):
        if account_uid:
            dates = self.get_date_numbers()
            url = self.base_url+'/api/v2/accounts/'+account_uid+'/spending-insights/country?year='+dates['year']+'&month='+dates['month']
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(url, headers=headers).json()
            return response

    def get_spending_category(self, account_uid):
        if account_uid:
            dates = self.get_date_numbers()
            url = self.base_url+'/api/v2/accounts/'+account_uid+'/spending-insights/spending-category?year='+dates['year']+'&month='+dates['month']
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(url, headers=headers).json()
            categories = response['breakdown']
            data_list = []
            for categ in categories:
                data_list.append(categ)
            df = pd.DataFrame(data_list)
            return df

    def account_holder_details(self):
        url_account_holder = self.base_url+'/api/v2/account-holder'
        url_name = self.base_url+'/api/v2/account-holder/name'
        headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
        account_holder = requests.get(url_account_holder, headers=headers).json()
        AH_name = requests.get(url_name, headers=headers).json()
        data = {
            'accountHolderName' : [AH_name['accountHolderName']],
            'accountHolderType' : [account_holder['accountHolderType']],
            'accountHolderUid' : [account_holder['accountHolderUid']]
        }
        df_account_holder = pd.DataFrame(data)
        return df_account_holder

    def get_reccuring_card_payment(self, account_uid):
        if account_uid:
            url = self.base_url+'/api/v2/accounts/'+account_uid+'/recurring-payment'
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(url, headers=headers).json()
            return response

    def get_transaction_details(self, account_uid, category_uid, create_date):
        if account_uid and category_uid:
            current_datetime = datetime.now()
            iso8601_string = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            encoded_string = create_date.replace(":", "%3A")
            url = self.base_url+'/api/v2/feed/account/'+account_uid+'/category/'+category_uid+'?changesSince='+encoded_string
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(url, headers=headers).json()
            transaction_data = []
            income_transaction = []
            expence_trasaction = []
            paid_to = {}
            receive_from = {}


            for feed in response['feedItems']:                
                receit_data ='https://api-sandbox.starlingbank.com'+'/api/v2/feed/account/'+account_uid+'/category/'+feed['categoryUid']+'/'+feed['feedItemUid']+'/receipt'
                receits = requests.get(receit_data, headers=headers)
                if receits:
                    for receit in receits:
                        pass

                transaction_time = feed.get('transactionTime')
                sattledAt = feed.get('SattledAt')
                updateAt = feed.get('updatedAt')
                if transaction_time:
                    transaction_time = datetime.strptime(transaction_time, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=None)
                if sattledAt:
                    sattledAt = datetime.strptime(sattledAt, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=None)
                if updateAt:
                    updateAt = datetime.strptime(updateAt, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=None)

                amount_receit = self.base_url+'/api/v2/feed/account/'+account_uid+'/category/'+feed['categoryUid']+'/'+feed['feedItemUid']  
                receit = requests.get(amount_receit, headers=headers).json()
                amount = receit.get('amount').get('minorUnits')/100
                currency = receit.get('amount').get('currency')
                sourceAmount = receit.get('sourceAmount').get('currency')
                data_feed = {
                            'transactionTime' : str(transaction_time) if transaction_time else None,
                             'updatedAt' : str(updateAt) if updateAt else None,
                             'sattledAt' : str(sattledAt) if sattledAt else None,
                             'spendingCategory' : feed.get('spendingCategory'),
                             'categoryID' : feed.get('categoryUid'),
                             'Direction' : feed.get('direction'), 
                             'amount' : amount, 
                             'currency' : currency, 
                             'source': feed.get('source'),
                             'status' : feed.get('status'),
                             'counterPartyName' : feed.get('counterPartyName'),
                             'counterPartyType' : feed.get('counterPartyType'),
                             'reference' : feed.get('reference'),
                             'country' : feed.get('country'),
                             'sourceAmount': sourceAmount}
                if feed.get('direction') == 'IN':
                    income_transaction.append(data_feed)
                    party_name = feed.get('counterPartyName')
                    amount = feed.get('amount').get('minorUnits')/100
                    data_dict = {'party_name': party_name,
                    'Amount Paid' : amount,
                     'Currency' : feed.get('amount').get('currency'),
                     'Transaction Time' : str(transaction_time) if transaction_time else None, 
                     'Spending Category' : feed.get('spendingCategory')}
                    if party_name in receive_from.keys():
                        current_list = receive_from[party_name]
                        upated_list = current_list + [data_dict]
                        receive_from.update({
                                party_name : upated_list
                            })
                    else:
                        receive_from.update({
                                party_name : [data_dict]
                            })
                if feed.get('direction') == 'OUT':
                    expence_trasaction.append(data_feed)
                    party_name = feed.get('counterPartyName')
                    rec_dict = {'party_name': party_name,
                    'Amount Paid' : amount,
                     'Currency' : feed.get('amount').get('currency'),
                     'Transaction Time' : str(transaction_time) if transaction_time else None, 
                     'Spending Category' : feed.get('spendingCategory')}
                    if party_name not in paid_to.keys():
                        amount = feed.get('amount').get('minorUnits')/100
                        paid_to.update({party_name : [rec_dict]})
                    else:
                        party_name = feed.get('counterPartyName')
                        existing_list_exe = paid_to.get(party_name)
                        updated_list = existing_list_exe+[rec_dict]
                        paid_to.update({
                                party_name : updated_list
                            })
                transaction_data.append(data_feed)

            df = pd.DataFrame([(k, d) for k, v in receive_from.items() for d in v], columns=['Type', 'Details'])
            payee_wise_receive = pd.concat([df.drop(['Details'], axis=1), df['Details'].apply(pd.Series)], axis=1)

            df = pd.DataFrame([(k, d) for k, v in paid_to.items() for d in v], columns=['Type', 'Details'])
            paid_to_expence = pd.concat([df.drop(['Details'], axis=1), df['Details'].apply(pd.Series)], axis=1)

            
            transaction_df = pd.DataFrame(transaction_data)
            income_df = pd.DataFrame(income_transaction)
            expence_df = pd.DataFrame(expence_trasaction)

            data_frames = {
                'payee_expence' : payee_wise_receive,
                'paid_to_expence' : paid_to_expence,
                'all_transactions' : transaction_df,
                'income_transactions' : income_df, 
                'expence_trasaction' : expence_df,
            }
            return data_frames 

    def get_transaction_between(self,account_uid, category_uid, account_create_date):
        if account_uid:
            current_datetime = datetime.now()
            iso8601_string_end_date = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            encoded_string_end_date = iso8601_string_end_date.replace(":", "%3A")
            account_crate_date = account_create_date.replace(':','%3A')
            url = self.base_url+'/api/v2/feed/account/'+account_uid+'/category/'+category_uid+'/transactions-between?minTransactionTimestamp='+account_crate_date+'&maxTransactionTimestamp='+encoded_string_end_date
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(url, headers=headers).json()
            return response

    def get_settled_transactions(self, account_uid, category_uid, account_create_date):
        if account_uid:
            current_datetime = datetime.now()
            iso8601_string_end_date = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            encoded_string_end_date = iso8601_string_end_date.replace(":", "%3A")
            account_crate_date = account_create_date.replace(':','%3A')
            url = self.base_url+'/api/v2/feed/account/'+account_uid+'/settled-transactions-between?minTransactionTimestamp='+account_crate_date+'&maxTransactionTimestamp='+encoded_string_end_date
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(url, headers=headers).json()
            return response

    def get_account_statment(self, account_uid):
        if account_uid:
            statment_download = self.base_url+'/api/v2/accounts/'+account_uid+'/statement/download?yearMonth=2023-05'
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(statment_download, headers=headers)
        return response

    def get_profile_picture(self, account_uid):
        if account_uid:
            url = self.base_url+'/api/v2/account-holder/'+account_uid+'/profile-image'
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(url, headers=headers)
        return response

    def get_saving_goals(self, account_uid):
        if account_uid:
            url = self.base_url+'/api/v2/account/'+account_uid+'/savings-goals'
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(url, headers=headers)
            savings = response.json()
            data_list = []
            for saving in savings['savingsGoalList']:
                data_dict = {
                    'name': saving['name'],
                    'target': saving['target']['minorUnits'],
                    'totalSaved': saving['totalSaved']['minorUnits'],
                    'savedPercentage': saving['savedPercentage'],
                    'savingsGoalUid': saving['savingsGoalUid']
                }
                data_list.append(data_dict)
            sacing_df = pd.DataFrame(data_list)
            return sacing_df

    def get_monthly_spend(self, account_uid):
        if account_uid:
            date = datetime.now()
            list_of_months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
            month = date.month
            year = date.year 
            data_list = []
            breadDown_dict = {}
            list_df = []
            for month in range(month):
                each_month =  list_of_months[month]
                url = self.base_url+'/api/v2/accounts/'+account_uid+'/spending-insights/counter-party?year='+str(year)+'&month='+each_month
                headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
                respose = requests.get(url, headers=headers).json() 
                spending_df = pd.DataFrame({ 'Time Frame':[respose.get('period')],
                                                    'Total Spend' : [respose.get('totalSpent')],
                                                    'Total Received' : [respose.get('totalReceived')],
                                                    'Net Spend' : [respose.get('netSpend')],
                                                    'Tota Spend Net Out' : [respose.get('totalSpendNetOut')],
                                                    'Total Received Net In' : [respose.get('totalReceivedNetIn')],
                                                    'Direction' : [respose.get('direction')]}, index=[0])
                data_list.append(spending_df)
                if respose.get('breakdown'):
                        withTimeFrame = respose.get('breakdown')
                        df = pd.DataFrame(withTimeFrame)
                        df['Time Frame'] = respose.get('period')
                        list_df.append(df)

            result_df = pd.concat(data_list, ignore_index=True)
            combined_df = pd.concat(list_df, ignore_index=True)
            return {'MonthlySpend' : result_df, 'MonthlySpendBreakDown': combined_df}

    def get_payment_orders(self, account_uid, category_uid):
        if account_uid:
            url = self.base_url+'/api/v2/payments/local/account/'+account_uid+'/category/'+category_uid+'/standing-orders'
            headers = {'Content-Type': 'application/json','Authorization': self.auth_code}
            response = requests.get(url, headers=headers).json()
        return True

staring = StarlingBankAPI(base_url=None, auth_code=None)
accounts = staring.get_sandbox_accounts()
account_holder = staring.account_holder_details()
for account in accounts['accounts']:
    account_uid = account['accountUid']
    category_uid = account['defaultCategory']
    spending_breakdown = staring.get_spending_category(account_uid)
    profile_pic = staring.get_profile_picture(account_holder['accountHolderUid'].iloc[0])
    saving_goal = staring.get_saving_goals(account_uid)
    monthly_spent = staring.get_monthly_spend(account_uid)
    card_reccuring_payments = staring.get_reccuring_card_payment(account_uid)
    balance = staring.get_account_balance(account_uid)
    payment_order = staring.get_payment_orders(account_uid, category_uid)
    transaction_matrix = staring.get_transaction_details(account_uid, category_uid, account['createdAt'])
    bank_data = staring.get_bank_identifires(account_uid)
    AllTransactions = transaction_matrix['all_transactions']
    Income = transaction_matrix['income_transactions']
    Expence = transaction_matrix['expence_trasaction']
    PaidToWiseExpence = transaction_matrix['payee_expence']
    PayeeWiseIncome = transaction_matrix['paid_to_expence']
    MonthlySpent = monthly_spent['MonthlySpend']
    MonthlySpentBreakDown = monthly_spent['MonthlySpendBreakDown']
    print(balance, MonthlySpent, MonthlySpentBreakDown, AllTransactions, Income, Expence, account_holder, bank_data, spending_breakdown, saving_goal, PaidToWiseExpence, PayeeWiseIncome)

    