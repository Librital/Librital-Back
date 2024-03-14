# from googlesearch import search
#
# query = "Hunger Games"
# for result in search(query, num_results=1, lang="es"):
#     print("Title:", result)

import requests


def get_book_cover_image(title):
    base_url = "http://covers.openlibrary.org/b/id/"

    # Search for the book by title
    search_url = f"http://openlibrary.org/search.json?q={title}"
    response = requests.get(search_url)

    # Check if the response is successful
    if response.status_code == 200:
        # Get the first result
        result = response.json().get('docs', [])[0]

        # Check if the result has an 'cover_i' attribute
        if 'cover_i' in result:
            cover_id = result['cover_i']
            image_url = f"{base_url}{cover_id}-L.jpg"
            return image_url

    # Return None if no cover image is found
    return None


if __name__ == "__main__":
    # Replace 'Your Book Title' with the actual book title
    book_title = 'Los juegos del hambre balada de pajaro'

    # Get the book cover image URL
    cover_image_url = get_book_cover_image(book_title)

    if cover_image_url:
        print(f"Book Title: {book_title}")
        print(f"Cover Image URL: {cover_image_url}")
    else:
        print(f"No cover image found for '{book_title}'.")











