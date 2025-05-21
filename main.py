from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
import csv
import os

# File to store attendee data
FILE_NAME = "attendees.csv"
FEEDBACK_FILE = "feedback.csv"


# Ensure the CSV file exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "UH Email"])

if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Rating", "Comments"])

# Helper Functions
def show_frame(frame_to_show):
    for frame in [mainFrame, signInFrame, adminFrame, feedbackFrame, feedbackViewFrame]:
        frame.pack_forget()
    frame_to_show.pack(fill="both", expand=True)

def load_image(file_path):
    try:
        return PhotoImage(file=file_path)
    except TclError:
        return None  # Return None if the image file is not found

def sign_in():
    name = nameEntry.get().strip()
    email = emailEntry.get().strip()

    if not name:
        message_label.config(text="Error: Name is required!", fg="white")
        return

    if not email:
        message_label.config(text="Error: You did not enter a email!", fg="white")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, email])

    message_label.config(text="Sign-in successful!", fg="white")
    nameEntry.delete(0, END)
    emailEntry.delete(0, END)

def view_attendees():
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        attendees = list(reader)

    attendees_text.delete(1.0, END)
    if len(attendees) <= 1:
        attendees_text.insert(END, "No attendees yet!")
    else:
        for attendee in attendees[1:]:
            attendees_text.insert(END, f"Name: {attendee[0]}, UH Email: {attendee[1]}\n")

def on_exit():
    if messagebox.askyesno("Confirm Exit", "Only MSA officers are allowed to close the app. Are you sure you want to exit?", icon='warning'):
        root.quit()


def submit_feedback():
    rating = rating_var.get()
    comments = comments_entry.get("1.0", END).strip()

    if rating == 0:
        messagebox.showerror("Error", "Please select a rating!")
        return

    # Save feedback to CSV
    with open(FEEDBACK_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([rating, comments])  # Saves the selected number (1-5) and the comment

    messagebox.showinfo("Success", f"Feedback submitted! You rated: {rating} stars.")

    # Reset inputs
    rating_var.set(0)
    comments_entry.delete("1.0", END)


def load_feedback():
    feedback_text.delete("1.0", END)
    try:
        with open('feedback.csv', mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            if 'Rating' not in csv_reader.fieldnames or 'Comments' not in csv_reader.fieldnames:
                feedback_text.insert(END, "Invalid CSV format. Ensure 'Rating' and 'Comment' columns are present.\n")
                return

            for row in csv_reader:
                feedback_text.insert(END, f"Rating: {row['Rating']} - {row['Comments']}\n")

        if feedback_text.get("1.0", "end").strip() == "":
            feedback_text.insert(END, "No attendees yet!\n")

    except FileNotFoundError:
        feedback_text.insert(END, "Error: feedback.csv file not found.\n")

    # Call the average rating update after loading feedback
    update_average_rating()

# Main Window
root = Tk()
root.title("MSA Jummah Sign-In")
root.geometry("600x600+650+10")
root.resizable(False, False)

# Main Frame
mainFrame = Frame(root, bg="#D84040")
mainFrame.pack(fill="both", expand=True)

# Load Images
MSAImage = load_image(os.path.join("icons", "MSAIcon.png"))
clipboardImage = load_image(os.path.join("icons", "Clipboard.png"))
feedbackImage = load_image(os.path.join("icons", "Feedback2.png"))

# Constants for Fonts
BUTTON_FONT = "Times 15 bold"
LABEL_FONT = "Comic 12 bold"

# Frame for Image and Text
topLeft = Frame(mainFrame, bg="#1D1616")
topLeft.pack(side="top", anchor="nw", padx=10, pady=10)

# Display Image and Text
if MSAImage:
    imageLabel = Label(topLeft, image=MSAImage, bg="#1D1616")
    imageLabel.pack(side="left", padx=5)

text_label = Label(topLeft, text="Jummah Sign-In", font=LABEL_FONT, bg="#1D1616", fg="white", justify="center")
text_label.pack(side="left", padx=2)

# Frame for Footer
footer = Frame(mainFrame, bg="#8E1616", width=800, height=100, bd=2, relief="solid")
footer.place(x=0, y=530)

# Main Screen Widgets
app_label = Label(mainFrame, text="UH MSA Jummah Sign-In", font="Times 20 bold", bg="#D84040")
app_label.place(relx=0.5, y=80, anchor="center")

line_label = Label(mainFrame, text="_" * 100, font="Times 15", bg="#D84040")
line_label.place(relx=0.5, y=110, anchor="center")

welcomeLabel = Label(mainFrame, text="\u0627\u0644\u0633\u0644\u0627\u0645 \u0639\u0644\u064a\u0643\u0645, welcome to Jummah", font="Times 16 bold", bg="#D84040")
welcomeLabel.place(relx=0.5, y=140, anchor="center")

requestLabel = Label(mainFrame, text="Please Sign-In.", font="Times 15 bold", bg="#D84040")
requestLabel.place(relx=0.5, y=170, anchor="center")

# Buttons
signin_button = Button(mainFrame, text="Sign In", font=BUTTON_FONT, bg="#EEEEEE", bd=5, width=16, height=2, command=lambda: show_frame(signInFrame))
signin_button.place(x=70, y=210)

view_attendees_button = Button(mainFrame, text="View Attendees", font=BUTTON_FONT, bg="#EEEEEE", bd=5, width=16, height=2, command=lambda: show_frame(adminFrame))
view_attendees_button.place(x=330, y=210)

feedback_button = Button(mainFrame, text = "Feedback", font = BUTTON_FONT, bg = "#EEEEEE", bd = 5, width = 16, height = 2, command = lambda: show_frame(feedbackFrame))
feedback_button.place(x=70, y=300)

viewfeedback_button = Button(mainFrame, text = "View Feedback", font = BUTTON_FONT, bg = "#EEEEEE", bd = 5, width = 16, height = 2, command = lambda: show_frame(feedbackViewFrame))
viewfeedback_button.place(x=330, y=300)

exit_button = Button(mainFrame, text="Exit", font=BUTTON_FONT, bg="#EEEEEE", bd=5, width=16, height=2, command=on_exit)
exit_button.place(x=200, y=390)

# Sign In Frame
signInFrame = Frame(root, bg="#D84040")
if MSAImage:
    topLeft2 = Frame(signInFrame, bg="#1D1616")
    topLeft2.pack(side="top", anchor="nw", padx=10, pady=10)
    MSAImageLabel = Label(topLeft2, image=MSAImage, bg="#1D1616")
    MSAImageLabel.pack(side="left", padx=5)
    MSAImage_label = Label(topLeft2, text="Sign In", font=LABEL_FONT, bg="#1D1616", fg="white", justify="center")
    MSAImage_label.pack(side="left", padx=2)

Label(signInFrame, text="Sign In", font="Times 20 bold", bg="#D84040").pack(pady=20)
Label(signInFrame, text="Name:", font="Times 15", bg="#D84040").pack(anchor="w", padx=50)
nameEntry = Entry(signInFrame, font="Times 15", width=30)
nameEntry.pack(pady=5, padx=50)

Label(signInFrame, text="UH Email:", font="Times 15", bg="#D84040").pack(anchor="w", padx=50)
emailEntry = Entry(signInFrame, font="Times 15", width=30)
emailEntry.pack(pady=5, padx=50)

Button(signInFrame, text="Sign In", font=BUTTON_FONT, bg="#EEEEEE", width=12, command=sign_in).pack(pady=10)

footer = Frame(signInFrame, bg="#8E1616", width=800, height=100, bd=2, relief="solid")
footer.place(x=0, y=530)

message_label = Label(signInFrame, text="", font="Times 15 bold", bg="#D84040")
message_label.pack()

SignInExitButton = Button(signInFrame, text="Back to Main Menu", font=BUTTON_FONT, command=lambda: show_frame(mainFrame))
SignInExitButton.place(x=200, y=550)

# Admin Frame
adminFrame = Frame(root, bg="#D84040")
if clipboardImage:
    topLeft3 = Frame(adminFrame, bg="#1D1616")
    topLeft3.pack(side="top", anchor="nw", padx=10, pady=10)
    clipImageLabel = Label(topLeft3, image=clipboardImage, bg="#1D1616")
    clipImageLabel.pack(side="left", padx=5)
    clipImage_label = Label(topLeft3, text="View Attendees", font=LABEL_FONT, bg="#1D1616", fg="white", justify="center")
    clipImage_label.pack(side="left", padx=2)

# Right Frame for Attendee Count in Admin View (Similar to Average Rating Frame)
attendeeCountFrame = Frame(adminFrame, bg="#1D1616", width=150, height=150, bd=2, relief="solid")
attendeeCountFrame.pack(side="right", anchor="n", padx=10, pady=20)

# Title for Attendee Count
Label(attendeeCountFrame, text="Attendees", font="Times 12 bold", bg="#1D1616", fg="white").pack(pady=5)

# Attendee Count Display (Smaller Font)
attendee_count_var = StringVar(value="0")
attendee_count_label = Label(attendeeCountFrame, textvariable=attendee_count_var, font="Times 16 bold", bg="#1D1616", fg="white")
attendee_count_label.pack(pady=10)

# Function to update the attendee count
def update_attendee_count():
    # Get the text content from the attendees_text widget
    attendee_list = attendees_text.get("1.0", "end").strip().split('\n')

    # Check for the "No attendees yet!" message and return 0 if present
    if "No attendees yet!" in attendee_list:
        attendee_count_var.set("0")
        return

    # Filter out empty lines and count actual attendees
    attendee_list = [attendee for attendee in attendee_list if attendee]
    attendee_count_var.set(str(len(attendee_list)))


# Attendee List Label
Label(adminFrame, text="Attendee List", font="Times 20 bold", bg="#D84040").pack(pady=20)

# Bordered Frame for Attendee Text Widget
attendees_text_frame = Frame(adminFrame, bg="#1D1616", bd=2, relief="solid")
attendees_text_frame.pack(pady=10, padx=20)

# Text widget to display attendees with a bold border
attendees_text = Text(attendees_text_frame, font="Times 12", width=60, height=19, bg="white", bd=0)
attendees_text.pack(padx=5, pady=5)

footer = Frame(adminFrame, bg="#8E1616", width=800, height=100, bd=2, relief="solid")
footer.place(x=0, y=530)

loadAttendeesButton = Button(adminFrame, text="Load Attendees", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=view_attendees)
loadAttendeesButton.place(x=320, y=550)

# Update the attendee count when the attendees are loaded
loadAttendeesButton.config(command=lambda: [view_attendees(), update_attendee_count()])

AdminExitButton = Button(adminFrame, text="Back to Main Menu", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=lambda: show_frame(mainFrame))
AdminExitButton.place(x=80, y=550)

#Feedback Frame
feedbackFrame = Frame(root, bg="#D84040")
if feedbackImage:
    topLeft4 = Frame(feedbackFrame, bg="#1D1616")
    topLeft4.pack(side="top", anchor="nw", padx=10, pady=10)
    feedbackImageLabel = Label(topLeft4, image=feedbackImage, bg="#1D1616")
    feedbackImageLabel.pack(side="left", padx=5)
    feedbackImage_Label = Label(topLeft4, text="Feedback", font=LABEL_FONT, bg="#1D1616", fg = "white", justify="center")
    feedbackImage_Label.pack(side="left", padx=2)

Label(feedbackFrame, text="Rate the Khutbah", font="Times 20 bold", bg="#D84040").pack(pady=20)

# Rating System
rating_var = IntVar()
ratings_frame = Frame(feedbackFrame, bg="#D84040")
ratings_frame.pack()
for i in range(1, 6):
    ttk.Radiobutton(ratings_frame, text=f"{i}", variable=rating_var, value=i).pack(side="left", padx=5)

# Comments Section with Thinner Bordered Frame
Label(feedbackFrame, text="Additional Comments (Optional):", font="Times 15", bg="#D84040").pack(pady=10)

# Thinner Bordered Frame for Comments Section
comments_frame = Frame(feedbackFrame, bg="#1D1616", bd=1, relief="solid")
comments_frame.pack(pady=5, padx=20)

# Text widget for comments with border
comments_entry = Text(comments_frame, font="Times 12", width=50, height=5, bg="white", bd=0)
comments_entry.pack(padx=5, pady=5)

# Submit Button
ttk.Button(feedbackFrame, text="Submit Feedback", command=submit_feedback).pack(pady=10)

footer = Frame(feedbackFrame, bg="#8E1616", width=800, height=100, bd=2, relief="solid")
footer.place(x=0, y=530)

feedbackExitButton = Button(feedbackFrame, text="Back to Main Menu", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=lambda: show_frame(mainFrame))
feedbackExitButton.place(x=200, y=550)

# Feedback View Frame
feedbackViewFrame = Frame(root, bg="#D84040")

# Top section with optional image
if feedbackImage:
    topLeft4 = Frame(feedbackViewFrame, bg="#1D1616")
    topLeft4.pack(side="top", anchor="nw", padx=10, pady=10)
    feedbackImageLabel = Label(topLeft4, image=feedbackImage, bg="#1D1616")
    feedbackImageLabel.pack(side="left", padx=5)
    feedbackImage_label = Label(topLeft4, text="View Feedback", font=LABEL_FONT, bg="#1D1616", fg="white", justify="center")
    feedbackImage_label.pack(side="left", padx=2)

# Right Frame for Average Ratings in Feedback View (Smaller Size)
averageRatingFrame = Frame(feedbackViewFrame, bg="#1D1616", width=150, height=150, bd=2, relief="solid")
averageRatingFrame.pack(side="right", anchor="n", padx=10, pady=20)

# Title for Average Rating
Label(averageRatingFrame, text="Avg. Rating", font="Times 12 bold", bg="#1D1616", fg="white").pack(pady=5)

# Average Rating Display (Smaller Font)
average_rating_var = StringVar(value="N/A")
average_rating_label = Label(averageRatingFrame, textvariable=average_rating_var, font="Times 16 bold", bg="#1D1616",
                             fg="white")
average_rating_label.pack(pady=10)


# Function to update the average rating from feedback.csv file
def update_average_rating():
    global average_rating_var
    ratings = []

    try:
        # Read the feedback.csv file
        with open('feedback.csv', mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            # Check if 'Rating' column exists
            if 'Rating' not in csv_reader.fieldnames:
                print("Error: 'Rating' column not found in CSV file.")
                average_rating_var.set("N/A")
                return

            # Extract ratings and validate them
            for row in csv_reader:
                try:
                    rating = int(row['Rating'].strip())
                    # Ignore "No attendees yet!" by skipping ratings with 0
                    if 1 <= rating <= 5:
                        ratings.append(rating)
                    else:
                        print(f"Ignored rating: {rating}")
                except ValueError:
                    print(f"Non-integer rating ignored: {row['Rating']}")
                    continue

        # Calculate and display the average rating if there are valid ratings
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            average_rating_var.set(f"{avg_rating:.1f}")
            print(f"Average rating calculated: {avg_rating:.1f}")
        else:
            print("No valid ratings found.")
            average_rating_var.set("N/A")

    except FileNotFoundError:
        print("Error: feedback.csv file not found.")
        average_rating_var.set("File not found")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        average_rating_var.set("Error")

# Heading label
Label(feedbackViewFrame, text="Feedback List", font="Times 20 bold", bg="#D84040").pack(pady=20)

# Bordered Frame for Feedback Display
feedback_text_frame = Frame(feedbackViewFrame, bg="#1D1616", bd=1, relief="solid")
feedback_text_frame.pack(pady=10, padx=20)

# Text widget to display feedback with border
feedback_text = Text(feedback_text_frame, font="Times 12", width=60, height=19, bg="white", bd=0)
feedback_text.pack(padx=5, pady=5)

# Footer styling (matches adminFrame)
footer = Frame(feedbackViewFrame, bg="#8E1616", width=800, height=100, bd=2, relief="solid")
footer.place(x=0, y=530)

# Buttons: Load Feedback & Return to Main Menu
loadFeedbackButton = Button(feedbackViewFrame, text="Load Feedback", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=load_feedback)
loadFeedbackButton.place(x=320, y=550)

feedbackExitButton = Button(feedbackViewFrame, text="Back to Main Menu", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=lambda: show_frame(mainFrame))
feedbackExitButton.place(x=80, y=550)


root.mainloop()
