const loginForm = document.getElementById('loginForm');
const bookForm = document.getElementById('bookForm');
const bookList = document.getElementById('bookList');

// Check for stored token
const accessToken = localStorage.getItem('access_token');

async function fetchBooks() {
    const response = await fetch('http://127.0.0.1:8000/api/books/', {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    });
    const books = await response.json();
    displayBooks(books);
}

function displayBooks(books) {
    bookList.innerHTML = '';
    books.forEach(book => {
        const bookItem = document.createElement('div');
        bookItem.textContent = `${book.title} by ${book.author} (Genre ID: ${book.genre}, Read: ${book.read_status})`;
        bookList.appendChild(bookItem);
    });
}

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://127.0.0.1:8000/api/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access); // Store the access token
        localStorage.setItem('refresh_token', data.refresh); // Optionally store the refresh token
        bookForm.style.display = 'block'; // Show the book form
        fetchBooks(); // Fetch books after login
    } else {
        alert('Login failed');
    }
});

bookForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const genre = document.getElementById('genre').value;
    const read_status = document.getElementById('read_status').checked;

    const response = await fetch('http://127.0.0.1:8000/api/books/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            title,
            author,
            genre,
            read_status,
            user: 1  // Adjust as necessary
        })
    });

    if (response.ok) {
        fetchBooks();  // Refresh the book list
        bookForm.reset();  // Reset the form
    } else {
        alert('Failed to add book');
    }
});

// If the token exists, fetch books
if (accessToken) {
    bookForm.style.display = 'block';
    fetchBooks();
}