import streamlit as st
import json
import os

LIBRARY_FILE = "library.json"

def load_library():
    """Load the library from a JSON file if it exists."""
    if os.path.exists(LIBRARY_FILE):
        try:
            return json.load(open(LIBRARY_FILE, 'r'))
        except json.JSONDecodeError:
            st.error("Error loading library data. Starting with an empty library.")
            return []
    return []

def save_library(library):
    """Save the library to a JSON file."""
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file)
    st.success("Library saved to file.")

# Initialize library in session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Sidebar navigation for different features
menu = st.sidebar.radio(
    "Select an option",
    ["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics", "Save Library"]
)

# Add a Book
if menu == "Add a book":
    st.header("Add a Book")
    with st.form(key="add_book_form"):
        title = st.text_input("Enter the book title")
        author = st.text_input("Enter the author")
        year = st.number_input("Enter the publication year", min_value=0, step=1, format="%d")
        genre = st.text_input("Enter the genre")
        read_input = st.selectbox("Have you read this book?", ("Yes", "No"))
        submit_button = st.form_submit_button("Add Book")
    if submit_button:
        read = True if read_input.lower() == "yes" else False
        book = {
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read
        }
        st.session_state.library.append(book)
        st.success("Book added successfully!")

# Remove a Book
elif menu == "Remove a book":
    st.header("Remove a Book")
    title_remove = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        removed = False
        for book in st.session_state.library:
            if book.get("title", "").lower() == title_remove.lower():
                st.session_state.library.remove(book)
                removed = True
                st.success("Book removed successfully!")
                break
        if not removed:
            st.error("Book not found!")

# Search for a Book
elif menu == "Search for a book":
    st.header("Search for a Book")
    search_by = st.radio("Search by:", ("Title", "Author"))
    query = st.text_input(f"Enter the {search_by.lower()}:")
    if st.button("Search"):
        if search_by == "Title":
            matches = [book for book in st.session_state.library if query.lower() in book.get("title", "").lower()]
        else:
            matches = [book for book in st.session_state.library if query.lower() in book.get("author", "").lower()]
        if matches:
            st.subheader("Matching Books:")
            for idx, book in enumerate(matches, start=1):
                # Use get() to safely access "read" with a default value of False
                status = "Read" if book.get("read", False) else "Unread"
                st.write(f"{idx}. {book.get('title')} by {book.get('author')} ({book.get('year')}) - {book.get('genre')} - {status}")
        else:
            st.info("No matching books found!")

# Display All Books
elif menu == "Display all books":
    st.header("Your Library")
    if st.session_state.library:
        for idx, book in enumerate(st.session_state.library, start=1):
            # Use get() for the "read" key
            status = "Read" if book.get("read", False) else "Unread"
            st.write(f"{idx}. {book.get('title')} by {book.get('author')} ({book.get('year')}) - {book.get('genre')} - {status}")
    else:
        st.info("No books in the library!")

# Display Statistics
elif menu == "Display statistics":
    st.header("Library Statistics")
    total_books = len(st.session_state.library)
    if total_books == 0:
        percentage_read = 0
    else:
        read_books = sum(1 for book in st.session_state.library if book.get("read", False))
        percentage_read = (read_books / total_books) * 100
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.1f}%")

# Save Library to File
elif menu == "Save Library":
    st.header("Save Library")
    if st.button("Save Library to file"):
        save_library(st.session_state.library)