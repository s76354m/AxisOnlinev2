import streamlit as st
from app.frontend.dashboard import Dashboard

if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run() 