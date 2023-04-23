from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid
from math import ceil

class Product:
    def get_displayed_pages(self, current_page, num_pages, max_displayed_pages=5):
        half_max_displayed = max_displayed_pages // 2
        if num_pages <= max_displayed_pages:
            return list(range(1, num_pages+1))
        elif current_page - half_max_displayed <= 1:
            return list(range(1, max_displayed_pages+1)) + ["...", num_pages]
        elif current_page + half_max_displayed >= num_pages:
            return [1, "..."] + list(range(num_pages-max_displayed_pages+2, num_pages+1))
        else:
            return [1, "..."] + list(range(current_page-half_max_displayed, current_page+half_max_displayed+1)) + ["...", num_pages]