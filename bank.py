

def bank_account(balance=0, rate=0):
	return {
		"balance": balance,
		"rate": rate,
		"dept_start_date": None,
	}

def loan(entity):
	return {}


bank_ = {
	"name": "WORLD_BANK",
	"owner": "WORLD",
	"accounts": {
		"world": bank_account(1_000_000_000_000, 9999),
		"company": {},
		"person": {}
	},
	"loans": {
		"company": {},
		"person": {}
	}
}
