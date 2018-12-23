# RFID + database testing for a future project.

import hashlib as hl
import sqlite3

# Connect to database
db = sqlite3.connect('data.db')
cursor = db.cursor()


# This is just for testing. Going to make a seperate part in database for it at a later date.
master = "d4a336181cb927c39d066787764b5b93806b78e50a9b1318f2436f53e27ab45230b36d60e23f8cadc1b938681f4d2a14271aeb74518269f244be0937c974b06b"


def exit(): # Exit function.
	db.close()
	quit()


def new_card(): # Adds a new card to the database.
	card = input("Please scan your card: ")

	card_hash = hl.sha512(card.encode()) # Covert card number to SHA512 hash.
	card_dig = card_hash.hexdigest() # Make the hash readable.

	cursor.execute('''SELECT card FROM cards WHERE card = ?''', (card_dig,)) # See if the card hash is in the database.
	all_cards = cursor.fetchone()


	if all_cards == None: # If the hash isnt in the database:
		cursor.execute('''INSERT INTO cards(card) VALUES(?)''', (card_dig,)) # Add the new card hash.
		db.commit()
		print("New card added!")


	else: # If the card hash is in the database or anything that isn't a "None" return:
		cursor.execute('''DELETE FROM cards WHERE card = ? ''', (card_dig,)) # Delete the card hash from the database.
		print("Card deleted!")


	card_check()


def card_check(): # Check the card to see if it is valid.
	card = input(">> ")

	if card == "quit":
		exit()

	print("Checking card...")

	# Hash the card value to check against the hashed versions in the database.
	card_hash = hl.sha512(card.encode())
	card_dig = card_hash.hexdigest()


	if card_dig == master:
		print("Unlocked!")
		new_card()


	try: # See if card hash is in the database:
		cursor.execute('''SELECT card FROM cards WHERE card = ?''', (card_dig,))
		all_cards = cursor.fetchone()

		if all_cards == None: # If the card hash is not in the database:
			print("Error!")


		elif all_cards[0] == card_dig and all_cards[0] != master: # If the card is in the database and it is not the master card:
			print("Unlocked!")
	

	except ValueError:
		print("Error!")


def main():
	while True:
		card_check()


if __name__ == "__main__":
        main()

db.close()