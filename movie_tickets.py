import streamlit as st

# Initialize movie data and session state
if "movies" not in st.session_state:
    st.session_state.movies = [
        {"name": "Avengers", "price": 200, "rating": "U", "seats": 50},
        {"name": "Joker", "price": 250, "rating": "A", "seats": 30},
        {"name": "Pushpa 2", "price": 300, "rating": "UA", "seats": 40}
    ]

def show_movies():
    st.subheader("🎬 Available Movies")
    for i, movie in enumerate(st.session_state.movies, start=1):
        st.write(f"{i}. {movie['name']}** | Price: ₹{movie['price']} | Rating: {movie['rating']} | Seats Left: {movie['seats']}")

def calculate_bill(no_of_tickets, price):
    subtotal = no_of_tickets * price
    gst = subtotal * 0.05  # 5% GST
    total = subtotal + gst
    return subtotal, gst, total

def book_tickets(choice_index, no_of_tickets, ages=None):
    movie = st.session_state.movies[choice_index]

    if no_of_tickets > 6:
        st.error("❌ Booking rejected! You can book a maximum of 6 tickets at once.")
        return

    if no_of_tickets > movie["seats"]:
        st.error(f"❌ Booking rejected! Only {movie['seats']} seats available for {movie['name']}.")
        return

    if movie["rating"] == "A":
        if ages is None or len(ages) != no_of_tickets:
            st.error("❌ Number of ages entered doesn’t match number of tickets!")
            return
        if any(age < 18 for age in ages):
            st.error("❌ One or more viewers are under 18. Booking rejected for 'A' rated movie.")
            return

    # Booking successful
    subtotal, gst, total = calculate_bill(no_of_tickets, movie["price"])
    movie["seats"] -= no_of_tickets

    st.success("✅ Booking Confirmed!")
    st.write(f"*Movie:* {movie['name']}")
    st.write(f"*Tickets Booked:* {no_of_tickets}")
    st.write(f"*Subtotal:* ₹{subtotal:.2f}")
    st.write(f"*GST (5%):* ₹{gst:.2f}")
    st.write(f"*Total Amount:* ₹{total:.2f}")
    st.write(f"*Remaining Seats:* {movie['seats']}")

# UI layout
st.title("🎟 Movie Ticket Booking System")

show_movies()

movie_names = [movie['name'] for movie in st.session_state.movies]
selected_movie = st.selectbox("Select a movie", movie_names)
choice_index = movie_names.index(selected_movie)

no_of_tickets = st.number_input("Enter number of tickets to book", min_value=1, max_value=10, step=1)

movie_rating = st.session_state.movies[choice_index]['rating']
ages = None

if movie_rating == "A":
    st.info("🔞 This is an 'A' rated movie. Viewer(s) must be 18 or older.")
    age_input = st.text_input(f"Enter the ages of {no_of_tickets} viewer(s), separated by spaces")
    if age_input:
        try:
            ages = list(map(int, age_input.strip().split()))
        except ValueError:
            st.error("⚠ Please enter valid integer ages.")

if st.button("Book Tickets"):
    book_tickets(choice_index, no_of_tickets, ages)
