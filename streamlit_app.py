import streamlit as st
from app import db, create_app
from app.models import User, Candidate, Vote

# Initialize your Flask app (without running it)
flask_app = create_app()

# Use Streamlit for the frontend
st.title("Political Adjectives Voting App")

# Example: Display candidates and allow voting
candidates = Candidate.query.all()
for candidate in candidates:
    st.header(candidate.name)
    st.write("Current Votes: ", candidate.votes.count())

    # Allow users to submit votes
    if st.button(f"Vote for {candidate.name}"):
        user = User.query.first()  # Replace with actual logged-in user logic
        vote = Vote(user=user, candidate=candidate)
        db.session.add(vote)
        db.session.commit()
        st.success(f"Your vote for {candidate.name} has been recorded!")

# Display the results
st.write("Current voting results:")
for candidate in candidates:
    st.write(f"{candidate.name}: {candidate.votes.count()} votes")
