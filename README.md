# Anima Database

Video Demo - https://youtu.be/jb5oi7GI-fc

## Introduction
The Anima Database is a full-stack web application designed to serve as a comprehensive platform for anime enthusiasts. Similar to IMDb but focused solely on anime, our database contains information on anime titles released up to the year 2020. Users can explore, search, filter, and sort through a vast collection of anime entries.

## Features
- **Database Information**: Comprehensive information on anime titles released up to the year 2020.
- **Searching, Sorting, and Filtering**: Users can easily search for specific anime titles, sort them by various criteria, and apply filters based on genres, release year, etc.
- **Genres**: Categorization of anime titles into various genres for easy navigation.
- **Responsive Design**: Ensures a seamless user experience across different devices and screen sizes.
- **Additional Features**: TBD based on project progress and feedback.

## Technologies Used
- **Django**: Python web framework for building the backend server and handling data with Django models.
- **SQLite3**: Lightweight relational database management system used for storing anime information.
- **HTML/CSS**: Frontend development for creating the user interface and styling elements.
- **Jinja**: Template engine for generating dynamic HTML content in Django templates.
- **JavaScript**: Adds interactivity and dynamic behavior to the frontend.
- **Bootstrap**: Frontend framework for responsive and mobile-first design.

## Project Scope and Responsibilities
This project is a solo endeavor, encompassing both frontend and backend development.

### Responsibilities:
- **Backend Development**: Implementation of Django models, API endpoints, and business logic.
- **Frontend Development**: Designing and coding HTML/CSS templates, integrating with Django templates, and adding interactivity using JavaScript.
- **Database Management**: Setting up SQLite3 database, defining schemas, and managing data migration.
- **User Authentication**: Implementation of secure user authentication using Django's built-in authentication system.
- **Deployment**: Deploying the application to a web hosting platform for public access.

## Project Outcome Expectations
- **Good Outcome**: Core features implemented, including searching, sorting, and filtering functionalities, with a clean and functional frontend interface.
- **Better Outcome**: Database updated with additional anime titles beyond 2020, enhanced frontend design, and some extra features added based on feasibility.
- **Best Outcome**: A scalable and fully-featured Anima Database with an extensive collection of anime titles, polished frontend design, and robust backend architecture, capable of handling a growing user base.

## Additional Notes
- Regular testing and iteration will be conducted throughout the development process to ensure the quality and reliability of the application.
- Continuous learning and research will be undertaken to address any technical challenges and explore opportunities for improvement.

# The Anime Database - Creation


The journey of developing The Anime Database began with the acquisition of a CSV file containing extensive data about various anime titles. This CSV file, sourced from [here](https://github.com/cckuqui/anime-db/blob/master/datasets/myanimelist.csv), served as the cornerstone of the project's database.

### Data Conversion and Model Creation

To integrate this data into the Django framework, a custom script named `load_data` was developed. This script parsed the CSV file and loaded its contents into Django models. The decision to use Django models over direct SQL queries was made to streamline the development process and avoid the complexities of database optimizations. Leveraging Django's robust ORM (Object-Relational Mapping) provided a more intuitive and Pythonic approach to interacting with the database.

### Framework Selection and Development Tools

Choosing Django as the web framework was a strategic decision based on its widespread adoption in the industry and its similarity to Flask, a framework already familiar to the project developer. Furthermore, Django's extensive documentation and active community support ensured a smooth learning curve. 

To expedite development tasks and enhance productivity, AI tools such as ChatGPT were employed. These tools assisted in generating boilerplate HTML and CSS code, as well as aiding in content writing and grammar correction. This AI-driven approach significantly reduced the time spent on repetitive tasks, allowing more focus on core development objectives.

### Frontend Development and User Experience

With the backend infrastructure in place, attention turned towards crafting an intuitive and visually appealing frontend interface. The `layout.html` template served as the foundation, providing a consistent layout across all webpages. HTML, CSS, and JavaScript were employed to create dynamic and responsive user interfaces.

Key features of the website include a search functionality embedded within the navigation bar, enabling users to quickly locate their desired anime titles. Sorting and filtering options further enhance the browsing experience, allowing users to refine their search results based on various criteria such as genre and release year.

### Dynamic Content Presentation and Navigation

The homepage of The Anime Database greets users with curated lists of top anime titles and showcases the worst-rated anime, offering a glimpse into the diverse range of content available. Additionally, users can explore top anime from three different genres, providing further insights into popular trends within the anime community.

Dynamic loading mechanisms ensure a seamless browsing experience, allowing users to load additional anime titles on-demand without compromising initial loading times. Anime cards, arranged in a visually appealing layout, can be scrolled horizontally, providing an immersive browsing experience.

### Conclusion and Future Directions

The development of The Anime Database represents a culmination of efforts to create a user-centric platform for anime enthusiasts. By leveraging Django's powerful features and integrating AI-driven development tools, the project aims to deliver a seamless and engaging experience for users.

Moving forward, the project will continue to evolve, with plans to incorporate additional features and enhancements based on user feedback and emerging trends in the anime community. The Anime Database endeavors to remain a valuable resource for anime enthusiasts worldwide, fostering a community-driven approach to discovering and celebrating the diverse world of anime.

