from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
import csv
import os

# File to store attendee data
FILE_NAME = "attendees.csv"
FEEDBACK_FILE = "feedback.csv"

# Ensure the CSV files exist with headers
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

def sign_in():
    name = nameEntry.get().strip()
    email = emailEntry.get().strip()

    if not name:
        message_label.config(text="Error: Name is required!", fg="white")
        return

    if not email:
        message_label.config(text="Error: You did not enter an email!", fg="white")
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
    
    # Update attendee count
    update_attendee_count()

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
                feedback_text.insert(END, "Invalid CSV format. Ensure 'Rating' and 'Comments' columns are present.\n")
                return

            for row in csv_reader:
                feedback_text.insert(END, f"Rating: {row['Rating']} - {row['Comments']}\n")

        if feedback_text.get("1.0", "end").strip() == "":
            feedback_text.insert(END, "No feedback yet!\n")

    except FileNotFoundError:
        feedback_text.insert(END, "Error: feedback.csv file not found.\n")

    # Call the average rating update after loading feedback
    update_average_rating()

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

# Function to update the average rating from feedback.csv file
def update_average_rating():
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
                    # Ignore invalid ratings
                    if 1 <= rating <= 5:
                        ratings.append(rating)
                except ValueError:
                    continue

        # Calculate and display the average rating if there are valid ratings
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            average_rating_var.set(f"{avg_rating:.1f}")
        else:
            average_rating_var.set("N/A")

    except FileNotFoundError:
        average_rating_var.set("N/A")
    except Exception:
        average_rating_var.set("Error")

# Main Window
root = Tk()
root.title("MSA Jummah Sign-In")
root.geometry("600x600+650+10")
root.resizable(False, False)

# Constants for Fonts
BUTTON_FONT = "Times 15 bold"
LABEL_FONT = "Arial 12 bold"

# Main Frame
mainFrame = Frame(root, bg="#D84040")

# Frame for Header
headerFrame = Frame(mainFrame, bg="#1D1616", width=600, height=40)
headerFrame.pack(side=TOP, fill=X)
Label(headerFrame, text="Jummah Sign-In", font=LABEL_FONT, bg="#1D1616", fg="white").pack(side=LEFT, padx=10, pady=5)

# Footer Frame
footerFrame = Frame(mainFrame, bg="#8E1616", width=600, height=70)
footerFrame.pack(side=BOTTOM, fill=X)

# Content Area
contentFrame = Frame(mainFrame, bg="#D84040")
contentFrame.pack(fill=BOTH, expand=True)

# Main Screen Widgets
app_label = Label(contentFrame, text="UH MSA Jummah Sign-In", font="Times 20 bold", bg="#D84040")
app_label.pack(pady=20)

line_label = Label(contentFrame, text="_" * 50, font="Times 15", bg="#D84040")
line_label.pack(pady=5)

welcomeLabel = Label(contentFrame, text="\u0627\u0644\u0633\u0644\u0627\u0645 \u0639\u0644\u064a\u0643\u0645, welcome to Jummah", font="Times 16 bold", bg="#D84040")
welcomeLabel.pack(pady=10)

requestLabel = Label(contentFrame, text="Please Sign-In.", font="Times 15 bold", bg="#D84040")
requestLabel.pack(pady=10)

# Button Frame
buttonFrame = Frame(contentFrame, bg="#D84040")
buttonFrame.pack(pady=20)

# Top Row Buttons
topButtonFrame = Frame(buttonFrame, bg="#D84040")
topButtonFrame.pack(pady=10)

signin_button = Button(topButtonFrame, text="Sign In", font=BUTTON_FONT, bg="#EEEEEE", bd=5, width=16, height=2, command=lambda: show_frame(signInFrame))
signin_button.pack(side=LEFT, padx=10)

view_attendees_button = Button(topButtonFrame, text="View Attendees", font=BUTTON_FONT, bg="#EEEEEE", bd=5, width=16, height=2, command=lambda: show_frame(adminFrame))
view_attendees_button.pack(side=LEFT, padx=10)

# Middle Row Buttons
midButtonFrame = Frame(buttonFrame, bg="#D84040")
midButtonFrame.pack(pady=10)

feedback_button = Button(midButtonFrame, text="Feedback", font=BUTTON_FONT, bg="#EEEEEE", bd=5, width=16, height=2, command=lambda: show_frame(feedbackFrame))
feedback_button.pack(side=LEFT, padx=10)

viewfeedback_button = Button(midButtonFrame, text="View Feedback", font=BUTTON_FONT, bg="#EEEEEE", bd=5, width=16, height=2, command=lambda: show_frame(feedbackViewFrame))
viewfeedback_button.pack(side=LEFT, padx=10)

# Exit Button
exit_button = Button(buttonFrame, text="Exit", font=BUTTON_FONT, bg="#EEEEEE", bd=5, width=16, height=2, command=on_exit)
exit_button.pack(pady=10)

# Sign In Frame
signInFrame = Frame(root, bg="#D84040")

# Header for Sign In
signInHeaderFrame = Frame(signInFrame, bg="#1D1616", width=600, height=40)
signInHeaderFrame.pack(side=TOP, fill=X)
Label(signInHeaderFrame, text="Sign In", font=LABEL_FONT, bg="#1D1616", fg="white").pack(side=LEFT, padx=10, pady=5)

# Footer for Sign In
signInFooterFrame = Frame(signInFrame, bg="#8E1616", width=600, height=70)
signInFooterFrame.pack(side=BOTTOM, fill=X)

# Sign In Content
signInContentFrame = Frame(signInFrame, bg="#D84040")
signInContentFrame.pack(fill=BOTH, expand=True)

Label(signInContentFrame, text="Sign In", font="Times 20 bold", bg="#D84040").pack(pady=20)
Label(signInContentFrame, text="Name:", font="Times 15", bg="#D84040").pack(anchor="w", padx=50)
nameEntry = Entry(signInContentFrame, font="Times 15", width=30)
nameEntry.pack(pady=5, padx=50)

Label(signInContentFrame, text="UH Email:", font="Times 15", bg="#D84040").pack(anchor="w", padx=50)
emailEntry = Entry(signInContentFrame, font="Times 15", width=30)
emailEntry.pack(pady=5, padx=50)

Button(signInContentFrame, text="Sign In", font=BUTTON_FONT, bg="#EEEEEE", width=12, command=sign_in).pack(pady=10)

message_label = Label(signInContentFrame, text="", font="Times 15 bold", bg="#D84040", fg="white")
message_label.pack(pady=10)

SignInExitButton = Button(signInFooterFrame, text="Back to Main Menu", font=BUTTON_FONT, bg="#EEEEEE", command=lambda: show_frame(mainFrame))
SignInExitButton.pack(pady=10)

# Admin Frame (View Attendees)
adminFrame = Frame(root, bg="#D84040")

# Header for Admin
adminHeaderFrame = Frame(adminFrame, bg="#1D1616", width=600, height=40)
adminHeaderFrame.pack(side=TOP, fill=X)
Label(adminHeaderFrame, text="View Attendees", font=LABEL_FONT, bg="#1D1616", fg="white").pack(side=LEFT, padx=10, pady=5)

# Footer for Admin
adminFooterFrame = Frame(adminFrame, bg="#8E1616", width=600, height=70)
adminFooterFrame.pack(side=BOTTOM, fill=X)

# Admin Content
adminContentFrame = Frame(adminFrame, bg="#D84040")
adminContentFrame.pack(fill=BOTH, expand=True)

# Top content area with label and count
adminTopFrame = Frame(adminContentFrame, bg="#D84040")
adminTopFrame.pack(fill=X, pady=10)

Label(adminTopFrame, text="Attendee List", font="Times 20 bold", bg="#D84040").pack(side=LEFT, padx=20)

# Attendee Count Display
attendeeCountFrame = Frame(adminTopFrame, bg="#1D1616", bd=2, relief="solid")
attendeeCountFrame.pack(side=RIGHT, padx=20)

Label(attendeeCountFrame, text="Attendees", font="Times 12 bold", bg="#1D1616", fg="white").pack(pady=5, padx=10)

attendee_count_var = StringVar(value="0")
attendee_count_label = Label(attendeeCountFrame, textvariable=attendee_count_var, font="Times 16 bold", bg="#1D1616", fg="white")
attendee_count_label.pack(pady=5, padx=10)

# Bordered Frame for Attendee Text Widget
attendees_text_frame = Frame(adminContentFrame, bg="#1D1616", bd=2, relief="solid")
attendees_text_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

# Text widget to display attendees with a bold border
attendees_text = Text(attendees_text_frame, font="Times 12", width=60, height=15, bg="white", bd=0)
attendees_text.pack(padx=5, pady=5, fill=BOTH, expand=True)

# Admin Buttons
adminButtonFrame = Frame(adminFooterFrame, bg="#8E1616")
adminButtonFrame.pack(pady=10)

loadAttendeesButton = Button(adminButtonFrame, text="Load Attendees", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=view_attendees)
loadAttendeesButton.pack(side=LEFT, padx=10)

AdminExitButton = Button(adminButtonFrame, text="Back to Main Menu", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=lambda: show_frame(mainFrame))
AdminExitButton.pack(side=LEFT, padx=10)

# Feedback Frame
feedbackFrame = Frame(root, bg="#D84040")

# Header for Feedback
feedbackHeaderFrame = Frame(feedbackFrame, bg="#1D1616", width=600, height=40)
feedbackHeaderFrame.pack(side=TOP, fill=X)
Label(feedbackHeaderFrame, text="Feedback", font=LABEL_FONT, bg="#1D1616", fg="white").pack(side=LEFT, padx=10, pady=5)

# Footer for Feedback
feedbackFooterFrame = Frame(feedbackFrame, bg="#8E1616", width=600, height=70)
feedbackFooterFrame.pack(side=BOTTOM, fill=X)

# Feedback Content
feedbackContentFrame = Frame(feedbackFrame, bg="#D84040")
feedbackContentFrame.pack(fill=BOTH, expand=True)

Label(feedbackContentFrame, text="Rate the Khutbah", font="Times 20 bold", bg="#D84040").pack(pady=20)

# Rating System
rating_var = IntVar()
ratings_frame = Frame(feedbackContentFrame, bg="#D84040")
ratings_frame.pack(pady=10)

# Better looking rating system with stars
for i in range(1, 6):
    ttk.Radiobutton(ratings_frame, text=f"{i} ★", variable=rating_var, value=i).pack(side="left", padx=10)

# Comments Section
Label(feedbackContentFrame, text="Additional Comments (Optional):", font="Times 15", bg="#D84040").pack(pady=10)

# Bordered Frame for Comments Section
comments_frame = Frame(feedbackContentFrame, bg="#1D1616", bd=1, relief="solid")
comments_frame.pack(pady=5, padx=20)

# Text widget for comments with border
comments_entry = Text(comments_frame, font="Times 12", width=50, height=5, bg="white", bd=0)
comments_entry.pack(padx=5, pady=5)

# Submit Button
submitFeedbackButton = Button(feedbackContentFrame, text="Submit Feedback", font=BUTTON_FONT, bg="#EEEEEE", command=submit_feedback)
submitFeedbackButton.pack(pady=20)

# Feedback Exit Button
feedbackExitButton = Button(feedbackFooterFrame, text="Back to Main Menu", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=lambda: show_frame(mainFrame))
feedbackExitButton.pack(pady=10)

# Feedback View Frame
feedbackViewFrame = Frame(root, bg="#D84040")

# Header for Feedback View
feedbackViewHeaderFrame = Frame(feedbackViewFrame, bg="#1D1616", width=600, height=40)
feedbackViewHeaderFrame.pack(side=TOP, fill=X)
Label(feedbackViewHeaderFrame, text="View Feedback", font=LABEL_FONT, bg="#1D1616", fg="white").pack(side=LEFT, padx=10, pady=5)

# Footer for Feedback View
feedbackViewFooterFrame = Frame(feedbackViewFrame, bg="#8E1616", width=600, height=70)
feedbackViewFooterFrame.pack(side=BOTTOM, fill=X)

# Feedback View Content
feedbackViewContentFrame = Frame(feedbackViewFrame, bg="#D84040")
feedbackViewContentFrame.pack(fill=BOTH, expand=True)

# Top content area with label and average rating
feedbackViewTopFrame = Frame(feedbackViewContentFrame, bg="#D84040")
feedbackViewTopFrame.pack(fill=X, pady=10)

Label(feedbackViewTopFrame, text="Feedback List", font="Times 20 bold", bg="#D84040").pack(side=LEFT, padx=20)

# Average Rating Display
averageRatingFrame = Frame(feedbackViewTopFrame, bg="#1D1616", bd=2, relief="solid")
averageRatingFrame.pack(side=RIGHT, padx=20)

Label(averageRatingFrame, text="Avg. Rating", font="Times 12 bold", bg="#1D1616", fg="white").pack(pady=5, padx=10)

average_rating_var = StringVar(value="N/A")
average_rating_label = Label(averageRatingFrame, textvariable=average_rating_var, font="Times 16 bold", bg="#1D1616", fg="white")
average_rating_label.pack(pady=5, padx=10)

# Bordered Frame for Feedback Display
feedback_text_frame = Frame(feedbackViewContentFrame, bg="#1D1616", bd=1, relief="solid")
feedback_text_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

# Text widget to display feedback with border
feedback_text = Text(feedback_text_frame, font="Times 12", width=60, height=15, bg="white", bd=0)
feedback_text.pack(padx=5, pady=5, fill=BOTH, expand=True)

# Feedback View Buttons
feedbackViewButtonFrame = Frame(feedbackViewFooterFrame, bg="#8E1616")
feedbackViewButtonFrame.pack(pady=10)

loadFeedbackButton = Button(feedbackViewButtonFrame, text="Load Feedback", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=load_feedback)
loadFeedbackButton.pack(side=LEFT, padx=10)

feedbackViewExitButton = Button(feedbackViewButtonFrame, text="Back to Main Menu", font=BUTTON_FONT, bg="#EEEEEE", width=16, command=lambda: show_frame(mainFrame))
feedbackViewExitButton.pack(side=LEFT, padx=10)

# Start with the main frame
show_frame(mainFrame)

root.mainloop()