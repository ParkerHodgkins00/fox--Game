import random
import customtkinter as ctk

# Initialize the main app window
app = ctk.CTk()
app.title("4x4 Button Grid")
app.geometry("600x650")  # Increased height for reset button

# Initialize Array of Letters
currentIndex = 0
letters = ["f", "f", "f", "f", "f", "o", "o", "o", "o", "o", "o", "x", "x", "x", "x", "x"]
board = [["-" for _ in range(4)] for _ in range(4)]
random.shuffle(letters)
numTries=0

# Dictionary to store buttons
buttons = {}
hasStarted = False


def get_three_letter_words(grid, row, col):
    directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (1, 1),  # Diagonal Down-Right
        (-1, 1), # Diagonal Up-Right
        (0, -1), # Left
        (-1, 0), # Up
        (1, -1), # Diagonal Down-Left
        (-1, -1) # Diagonal Up-Left
    ]
    
    words = []
    rows, cols = len(grid), len(grid[0])
    
    for dr, dc in directions:
        word = ""
        r, c = row, col
        
        for _ in range(3):
            if 0 <= r < rows and 0 <= c < cols:
                word += grid[r][c]
                r += dr
                c += dc
            else:
                break
        
        if len(word) == 3:
            words.append((word, (dr, dc)))
    
    return words

def changeButtonColor(x, y, d):
    for i in range(3):
        buttons[(y, x)].configure(fg_color="red", hover_color="red")
        x += d[1]
        y += d[0]

def checkForFox(b):
    for i in range(len(b)):
        for j in range(len(b[i])):
            if board[j][i] == "f":
                answer = get_three_letter_words(b, j, i)
                for k in range(len(answer)):
                    if answer[k][0].lower() == "fox":
                        changeButtonColor(i, j, answer[k][1])

# Function to handle button click
def button_clicked(row, col):
    global currentIndex, hasStarted
    if board[col][row] == "-":
        button = buttons[(col, row)]
        board[col][row] = letters[currentIndex]
        button.configure(text=letters[currentIndex], hover_color="green", fg_color="green")  # Change the text when clicked
        currentIndex += 1
        checkForFox(board)
        hasStarted = True

# Function to reset the board
def reset_board():
    global currentIndex, board, letters, numTries, numTriesLabel, hasStarted
    currentIndex = 0
    letters = ["f", "f", "f", "f", "f", "o", "o", "o", "o", "o", "o", "x", "x", "x", "x", "x"]
    random.shuffle(letters)
    board = [["-" for _ in range(4)] for _ in range(4)]

    # Reset buttons
    for row in range(4):
        for col in range(4):
            buttons[(col, row)].configure(text=board[col][row], fg_color="gray", hover_color="darkblue")
            
              # Reset text and color

    if(hasStarted):
        numTries += 1
        hasStarted = False
    numTriesLabel.configure(text=f"Number of tries: {numTries}")

def reset_board_diagonal():
    global currentIndex, board, letters, numTries, numTriesLabel, hasStarted
    currentIndex = 0
    letters = ["f", "f", "f", "f", "f", "o", "o", "x", "x", "x", "x", "x"]
    random.shuffle(letters)
    board = [["-" for _ in range(4)] for _ in range(4)]
    board[0][3] = "o"
    board[1][2] = "o"
    board[2][1] = "o"
    board[3][0] = "o"
    

    # Reset buttons
    for col in range(4):
        for row in range(4):
            buttons[(col, row)].configure(text=board[col][row], fg_color="gray", hover_color="darkblue")
            tmp = (col, row)
            if tmp == (0, 3) or tmp == (1,2) or tmp == (2,1) or tmp == (3,0):
                buttons[tmp].configure(fg_color="green",hover_color="green")
              # Reset text and color

    if(hasStarted):
        numTries += 1
        hasStarted = False
    numTriesLabel.configure(text=f"Number of tries: {numTries}")

# Create a 4x4 grid of buttons
for row in range(4):
    for col in range(4):
        btn = ctk.CTkButton(app, text=board[col][row], fg_color="gray",
                            command=lambda r=row, c=col: button_clicked(r, c))
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        buttons[(col, row)] = btn  # Store the button in a dictionary

# Add Reset Button
reset_btn = ctk.CTkButton(app, text="Reset Board", fg_color="blue", hover_color="darkblue", 
                          text_color="white", command=reset_board)
reset_btn.grid(row=5, column=1, padx=5, pady=5)

reset_btn_Os = ctk.CTkButton(app, text="Reset Board Hard", fg_color="blue", hover_color="darkblue", 
                          text_color="white", command=reset_board_diagonal)
reset_btn_Os.grid(row=5, column=2, padx=5, pady=5)


numTriesLabel = ctk.CTkLabel(app, text=f"Number of tries: {numTries}")
numTriesLabel.grid(row=6, column=0, columnspan=4, pady=10)

# Make grid cells expand with window resize
for i in range(4):
    app.grid_columnconfigure(i, weight=1)
    app.grid_rowconfigure(i, weight=1)

# Run the app
app.mainloop()
