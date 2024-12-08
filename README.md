Welcome to My First Project!
I admit that I'm not great at naming projects, but I'll provide a brief explanation of what this project is about and what I did.

This project showcases some of my skills in Python and SQL. Let me tell you a bit about why I decided to create it.

The Malaysian government offers university students a RM100 discount on books from Popular Book Store. However, finding the books I want can be quite challenging because the website contains a large list of books to scroll through.

To address this, I decided to leverage my web scraping skills. The goal was to collect all the Chinese books available at Popular Book Store and convert the data into an Excel file for easier access.

Here's how I did it:

I used Selenium to automate the process of opening the browser and searching for the term 《大众书局》 (Great China Books).
Since the site predominantly shows books in English and Malay, I made the script scroll down automatically to reveal all Chinese books. The "load more" button at the bottom of the page keeps the content hidden unless you scroll. This process took about 10 minutes because there are so many books.
Once the page was fully loaded, I used BeautifulSoup (BS4) to scrape the titles and prices of the books.
Finally, I used Pandas to export the data into a CSV file, which is saved in the same directory as the script.
At the end of this process, you'll get a CSV file containing the titles and prices of all the books, making it much easier to view the available Chinese books.

