from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

BOOKS = [
    {"id": 1, "title": "Python Cơ Bản", "author": "Nguyễn Văn A", "year": 2021, "category": "Lập trình", "available": True},
    {"id": 2, "title": "Flask Web", "author": "Trần Thị B", "year": 2022, "category": "Lập trình", "available": False},
    {"id": 3, "title": "Dế Mèn Phiêu Lưu Ký", "author": "Tô Hoài", "year": 1941, "category": "Văn học", "available": True},
    {"id": 4, "title": "Sapiens", "author": "Yuval Harari", "year": 2011, "category": "Lịch sử", "available": True},
]


def find_book(book_id):
    return next((b for b in BOOKS if b["id"] == book_id), None)


@app.route("/")
def index():
    total = len(BOOKS)
    available = sum(1 for b in BOOKS if b["available"])
    return render_template("index.html", total=total, available=available)


@app.route("/books")
def books():
    category = request.args.get("category")
    categories = sorted({b["category"] for b in BOOKS})
    result = [b for b in BOOKS if b["category"] == category] if category else BOOKS
    return render_template("books.html", books=result, categories=categories, current=category)


@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = find_book(book_id)
    if book is None:
        abort(404, description=f"Không có sách với ID = {book_id}")
    return render_template("book_detail.html", book=book)


@app.route("/api/books")
def api_books():
    return jsonify(BOOKS)


@app.route("/api/books/<int:book_id>")
def api_book(book_id):
    book = find_book(book_id)
    if book is None:
        return jsonify({"error": f"Không có sách với ID = {book_id}"}), 404
    return jsonify(book)


@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Không tìm thấy tài nguyên"}), 404
    return render_template("404.html", message=e.description), 404


if __name__ == "__main__":
    app.run(debug=True)