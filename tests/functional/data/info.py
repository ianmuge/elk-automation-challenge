
from munch import Munch

es_bank_accounts = Munch()
es_bank_accounts.file = 'data/accounts.json'
es_bank_accounts.index = 'bank'
es_bank_accounts.type = 'account'
es_bank_accounts.entries = 1000
