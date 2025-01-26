import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


st.write(f"{st.session_state.bot.chat_history}")