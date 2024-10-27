import streamlit as st
from database import Database

# Initialize database connection
db = Database()

# Set page configuration
st.set_page_config(page_title="College Event Management System", page_icon=":tada:", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .main-title {
            font-size: 36px;
            color: #2E86C1;
            font-weight: bold;
            text-align: center;
        }
        .section-title {
            font-size: 24px;
            color: #2874A6;
            font-weight: bold;
            margin-top: 20px;
        }
        .event-card {
            background-color: #F2F4F4;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        .register-button {
            background-color: #28B463;
            color: white;
            border-radius: 5px;
        }
        .admin-section {
            background-color: #EAECEE;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("<h1 class='main-title'>College Event Management System</h1>", unsafe_allow_html=True)

# Login Section
st.sidebar.title("Login")
user_role = st.sidebar.selectbox("Select Role", ["User", "Admin"])

if user_role == "Admin":
    username = st.sidebar.text_input("Username", type="text")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login as Admin"):
        if db.authenticate_admin(username, password):
            st.session_state["is_admin"] = True
            st.success("Admin access granted.")
        else:
            st.error("Invalid admin credentials.")
else:
    st.session_state["is_admin"] = False

# Display Events
st.markdown("<h2 class='section-title'>Upcoming Events</h2>", unsafe_allow_html=True)
events = db.get_events()
if events:
    for event in events:
        with st.container():
            st.markdown(f"<div class='event-card'><h3>{event['title']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Description:</strong> {event['description']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Date:</strong> {event['date']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Location:</strong> {event['location']}</p>", unsafe_allow_html=True)
            if not st.session_state["is_admin"]:
                if st.button("Register", key=event['id']):
                    with st.form(f"registration_form_{event['id']}"):
                        name = st.text_input("Name")
                        roll_number = st.text_input("Roll Number")
                        email = st.text_input("Email")
                        if st.form_submit_button("Submit"):
                            db.register_user(event['id'], name, roll_number, email)
                            st.success("Registered successfully!")
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No events available at the moment.")

# Admin Section
if st.session_state.get("is_admin"):
    st.markdown("<h2 class='section-title'>Admin Dashboard</h2>", unsafe_allow_html=True)
    with st.expander("Add New Event"):
        title = st.text_input("Event Title")
        description = st.text_area("Description")
        date = st.date_input("Date")
        location = st.text_input("Location")
        if st.button("Add Event"):
            db.add_event(title, description, date, location)
            st.success("Event added successfully!")

    st.markdown("<div class='admin-section'>", unsafe_allow_html=True)
    st.subheader("Manage Existing Events")
    for event in events:
        st.write("Title:", event["title"])
        if st.button("Update Event", key=f"update_{event['id']}"):
            pass
        if st.button("Delete Event", key=f"delete_{event['id']}"):
            db.delete_event(event['id'])
            st.success("Event deleted.")
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("View Participants"):
        for event in events:
            st.subheader(f"Participants for {event['title']}")
            participants = db.get_participants(event['id'])
            for participant in participants:
                st.text(f"Name: {participant['name']}, Roll No: {participant['roll_number']}, Email: {participant['email']}")

# Footer
st.markdown("<hr><p style='text-align: center;'>Developed for college purposes - College Event Management System (CEMS)</p>", unsafe_allow_html=True)
