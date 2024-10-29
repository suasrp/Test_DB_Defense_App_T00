# app.py
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///databrokers.db')
Session = sessionmaker(bind=engine)
session = Session()

class DataBroker(Base):
    __tablename__ = 'databrokers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    opt_out_url = Column(String(200), nullable=False)
    notes = Column(Text, nullable=True)

# Create the database table if it doesn't exist
Base.metadata.create_all(engine)

# Streamlit app
st.title("Data Broker Tracker")

# Add new broker
with st.form(key='add_broker_form'):
    name = st.text_input("Broker Name")
    opt_out_url = st.text_input("Opt-Out URL")
    notes = st.text_area("Notes")
    submit_button = st.form_submit_button(label='Add Broker')

    if submit_button:
        new_broker = DataBroker(name=name, opt_out_url=opt_out_url, notes=notes)
        session.add(new_broker)
        session.commit()
        st.success("Broker added successfully!")

# Display existing brokers
st.subheader("Existing Data Brokers")
brokers = session.query(DataBroker).all()
for broker in brokers:
    st.write(f"{broker.name} - [Opt-Out]({broker.opt_out_url})")
    if st.button(f"Delete {broker.name}", key=broker.id):
        session.delete(broker)
        session.commit()
        st.success(f"{broker.name} deleted successfully!")

# Close the session
session.close()
