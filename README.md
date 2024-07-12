# CrowdSync

CrowdSync is a Flask-based web application designed to help users find and explore events such as concerts, sports, arts, theater, and comedy shows in their area. The project leverages the Ticketmaster API to fetch and display event information based on user inputs. The project is deployed at [CrowdSync](https://crowdsync.pythonanywhere.com/).

## Features

- **Search Events:** Users can search for events by entering a city or zipcode, date range, and query (e.g., artist, event, or venue).
- **Event Details:** View detailed information about each event, including the event name, venue, address, dates, and a link to purchase tickets.
- **Pagination:** Navigate through search results with pagination support.
- **Responsive Design:** The application is designed to be user-friendly and responsive.

## Project Structure

- `app.py`: Main Flask application file that handles routing, form validation, and session management.
- `ticketmasterapi.py`: Module that interfaces with the Ticketmaster API to fetch event data and process it.
- `templates/`: Directory containing HTML templates for the home and results pages.
  - `home.html`: Template for the search form.
  - `results.html`: Template for displaying search results.
- `static/`: Directory containing static files such as CSS and images.

## Usage
#### For using the deployed project
1. Navigate to the CrowdSync homepage.
2. Enter the required details in the search form:
  -City or Zipcode
  -Start Date (MM/DD/YYYY)
  -End Date (MM/DD/YYYY)
  -Query (e.g., artist, event, or venue)
3. Click the "Search" button to view events matching your criteria.
4. Use the pagination controls to navigate through the results.
5. Click on an event card to open the Ticketmaster page for more details and to purchase tickets.

## Setup
#### For running locally / deployed site is down
1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/crowdsync.git
   cd crowdsync
2. **Install dependencies:**
   Ensure you have Python and pip installed. Then run:
   ```sh
   pip install -r requirements.txt
3. **Set up environment variables:**
   Create a .env file in the root directory and add your Ticketmaster API credentials:
   ```sh
   API_KEY=your_ticketmaster_api_key
   API_SECRET=your_ticketmaster_api_secret
4. **Run the application:**
   ```sh
   python app.py
   The application will be accessible at http://127.0.0.1:5000/.

Feel free to explore and enjoy finding events with CrowdSync! If you have any questions or need assistance feel free to checkout the presentation and please don't hesitate to reach out.
