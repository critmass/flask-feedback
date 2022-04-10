from tkinter import CURRENT
from flask import Flask, render_template, request, flash, redirect, session

from models import User, db, connect_db

app = Flask(__name__)

CURRENT_USER_KEY="curr_user"