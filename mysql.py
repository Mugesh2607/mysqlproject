import mysql.connector

def create_table(cursor):
    tablequery = """CREATE TABLE IF NOT EXISTS game_results (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            player1_name VARCHAR(50),
                            player2_name VARCHAR(50),
                            round_number INT,
                            player1_choice VARCHAR(50),
                            player2_choice VARCHAR(50),
                            result VARCHAR(50)
                            )"""
    cursor.execute(tablequery)

def player_choice():
    while True:
        choice = input("Enter your choice (stone, paper, scissors): ").lower()
        if choice in ['stone', 'paper', 'scissors']:
            return choice
        else:
            print("Invalid choice. Please choose again.")

def winner(player1_choice, player2_choice):
    if player1_choice == player2_choice:
        return "It's a tie!"
    elif (player1_choice == 'stone' and player2_choice == 'scissors') or \
         (player1_choice == 'scissors' and player2_choice == 'paper') or \
         (player1_choice == 'paper' and player2_choice == 'stone'):
        return "Player 1 wins!"
    else:
        return "Player 2 wins!"

def main():
    conn = mysql.connector.connect(host="localhost", user="root", password="Mugesh735", database="Game1")
    cursor = conn.cursor()

    create_table(cursor)

    player1_name = input("Enter name for Player 1: ")
    player2_name = input("Enter name for Player 2: ")

    player1_score = 0
    player2_score = 0

    for round_number in range(1, 7):
        print(f"\nRound {round_number}:")
        player1_choice_input = player_choice()
        player2_choice_input = player_choice()
        print(f"{player1_name} choose: {player1_choice_input}")
        print(f"{player2_name} choose: {player2_choice_input}")
        
        result = winner(player1_choice_input, player2_choice_input)
        print(result)

        if result == "Player 1 wins!":
            player1_score += 1
        elif result == "Player 2 wins!":
            player2_score += 1

        
        insert = "INSERT INTO game_results (player1_name, player2_name, round_number, player1_choice, player2_choice, result) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert, (player1_name, player2_name, round_number, player1_choice_input, player2_choice_input, result))
        conn.commit()

    print("\nFinal Score:")
    print(f"{player1_name}: {player1_score}")
    print(f"{player2_name}: {player2_score}")
    cursor.close()
    conn.close()

main()
