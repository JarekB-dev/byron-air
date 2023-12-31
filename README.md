# $${\color{gold}ByronAir \space Airline}$$

## **Python Command Line Ticket Booking System**

> This application is Python based Flight ticket booking system. A user is able to book tickets from a wide range of European destinations. User can specify name, number of bags and select desired flight. Booking creates a reservation number which can be retrieved later to check booking details.
> All bases and created bookings are available in this [Spreadsheet](https://docs.google.com/spreadsheets/d/13a70DgGfpnCKCHinh6Xt_CvlNsL3aNJ22Z5P98DCp1c/edit?usp=sharing).

### [Live Site](https://byron-air-b087f2b64028.herokuapp.com/)

### [Repository](https://github.com/JarekB-dev/byron-air)

## Table of Contents

1. [Preplanning](#preplanning)
2. [Features to Implement](#features)
3. [Technologies Used](#technologies)
4. [Testing](#testing)
5. [Bugs](#bugs)
6. [Deployment](#deployment)
7. [Content](#content)
8. [Acknowledgments](#acknowledgments)

<a name="preplanning"></a>

# $${\color{orange}Preplanning \space Phase}$$

## Flow

As an employee in the airline industry, I decided to create an airline ticket booking system for my third project. My first step in developing the ByronAir application was to come up with the general logic the application will follow. Using Lucid, I created a flow chart that helped me visualize what the application needs to do. This enabled me to think of the various features and functions the application should have, and the order in which they should be executed. It also gave me a clear understanding of how the different parts of the application interact with each other.

![Lucid Chart](assets/images/flow_chart.png)

### Flow of Creating a Booking

When user run the application, below screen is presented:

![Main Menu](assets/images/main_menu.png)

> User can choose to Make a Booking or Retrieve already created Reservation.

If user would like to make a booking, then below screen is shown.

![Country List](assets/images/country_list.png)

> User can choose Country of Departure/Arrival and proceed to select desired Airport of Departure/Arrival.

After choosing Departure/Arrival Airport user is being asked to provide date of Departure with screen below:

![Departure Date](assets/images/departure_date.png)

> User have to input date in DD/MM/YYYY format and date must be in the future, otherwise error will be shown and user asked to try again.

User is being presented with three available flights with random hours and random prices.

![Flights details](assets/images/flight_details.png)

> User have to choose one of three options. Any input other than 1,2,3 will cause error and ask user to try again.

Succesfully selecting available flight will prompt the user to next screen, which will ask for Name and total number of passengers.

![Passenger Details](assets/images/pax_details.png)

> User needs to choose name that must contain two parts: first and last name. Name cannot contain any digits or error will be shown. User can add total number of 10 passengers. Number more than 10 will cause error.

Last step when application will ask for Users input is number of check-in bags.

![Check in Bags](assets/images/check_in_bags.png)

> User can select only 3 check-in bags per passenger. Each bag costs 25€ and is being added to total booking price. Number of bags more than allowed will print error to the User.

Finally, user is being presented with all provided inputs in form of Table. All details are added to Booking worksheet with randomly generated Reservation Number.

![Reservation](assets/images/reservation.png)

> User can write down Reservation Number to Retrieve booking later. Any key will get User back to Main Menu.

### Retrieving Reservation

From the Main Menu if user select option 2 then is being presented with screen to input Reservation Number.

![Reservation Number](assets/images/reservation_number.png)

> User must provide number that already exists in the worksheet, otherwise error will be shown. Reservation number can be all lowercase or mixed as it is being converted to all Uppercase to match Reservation Number column.

After providing application with correct Reservation Number, all details are being pulled from worksheet containing data from rows of the reservation.

![Retrieve Reservation](assets/images/retrieve_reservation.png)

> All information shown to the user match previously inputted data. User can input any key to go back to Main Menu.

### Google Sheets

- I have created Google Sheet to pull Countries/Airports information as well as adding Reservations created by the User.

- Spreadsheet contains 17 Worksheets with European Countries and Airports inside them.

- First Worksheet labeled "Bookings" contains all bookings information created by the User. Those information can be retrieved by the User via inputting Reservation Number in the application.

<a name="features"></a>

# $${\color{orange}Features \space to \space Implement}$$

- Get access to Ryanair flight database:

  > Instead of creating random flights with random hours, I would like to link my application to flights live data for user to choose from. Still thinking about prices as these seem to depend on to many factors.

- Give User access to edit created Booking:

  > At the moment application allows only to view created Booking, however in the future I am planning to enable users the possibility to edit booking details(with some restrictions), then price of the booking will be updated and old booking deleted and new booking created in the spreadsheet.

- Expand options to select seats and link external website to book parking depending on the location:

  > At the moment application does not allow users to select desired seats. I would like to create system similar to Ryanair, where price depends on the seats row or legroom. Also creating external dummy website with parkings in different locations would enhance user experience - New spreadsheet to pull parking locations, prices etc.

- Booking confirmation to email.
  > Currently, Booking is only being created in the spreadsheet and Reservation Number is being presented to the User - if number will be forgotten, then there is no way to retrieve booking. I am planning to send all booking information to user email after creating one.

<a name="technologies"></a>

# $${\color{orange}Technology \space Used}$$

### [Python](<https://en.wikipedia.org/wiki/Python_(programming_language)>)

Used to create the application

### [Heroku](https://heroku.com)

Used to deploy and host the application

### [Github](https://github.com)

Used to store the code

### [Gitpod](https://gitpod.io)

IDE used for creating the application

### [Git](https://en.wikipedia.org/wiki/Git)

Used for version control

### [Google Sheets/Drive API](https://developers.google.com/sheets/api/reference/rest)

Used for storing bookings and importing airport data

<a name="testing"></a>

# $${\color{orange}Testing}$$

## Testing Phase

### Error Handling

| Test                                                                            | Result        |
| ------------------------------------------------------------------------------- | ------------- |
| User tries to enter non existing value in the Main Menu or no value             | Error Handled |
| User tries to enter nonexistant number or letter in Country list                | Error Handled |
| User tries to enter nonexistant number or letter in Airport list                | Error Handled |
| User tries to set the same Departure and Arrival airport                        | Error Handled |
| User tries to set date in incorrect format or date from the past                | Error Handled |
| User tries to select non existing flight, input letter or input no value        | Error Handled |
| User tries to enter just 1 part of the name, name containing digits or no value | Error Handled |
| User tries to enter more than 10 of total passengers or no value                | Error Handled |
| User tries to set number of Check-in bags more than allowed or input no value   | Error Handled |

### Bookings

All information - if valid - is being correctly added to the 'bookings' worksheet in below format:

![Booking Format](assets/images/booking-worksheet.png)

and with correct data presented to the user as below:

![Reservation Details](assets/images/reservation_details.png)

### CI Linter

I have used Python code checker provided by Code Institute [Link](https://pep8ci.herokuapp.com/). Result shown below:

![CI Linter](assets/images/ci_linter.png)

> Most errors are due to how LOGO is being created and couple of too long lines which are because of amount of data some statements are trying to pull.

<a name="bugs"></a>

# $${\color{orange}Bugs}$$

During development of the application I have encountered multiple bugs, most of them have been resolved:

- User was trying to set the same departure and arrival airport.

  > This bug has been resolved for adding extra argument to flight direction function that check if both arguements are the same and if so then print an error.

- User was not able to choose Country/Airport by index number but by Country/Airport name.

  > To make it easier for the user to select Airport or country I wanted to make sure that those can be selected by entering index number. Method enumerate() came in handy as it allowed me to iterate over worksheet titles and assign them index numbers.

- User was able to type during typing_input function.

  > Adding return statement to typing_input prevented user to insert characters during typing effect function and input is being added after function is completed.

- User was able to choose date from the past.

  > This would make no sense to book flight tickets for past dates and had to resolve it with statement if current date < inputted date in date_of_departure function.

- User was able to see booking worksheet on Country list.
  > In this case setting [1:] came in handy to start iteration from second worksheet effectively skipping first Bookings worksheet.

### Unfixed bugs

- Currently I have a problem when User is trying to input too long name, then Reservation Details table is displayed incorrectly in the console due to 80 character width.

<a name="deployment"></a>

# $${\color{orange}Deployment}$$

- Navigate to heroku.com & log in.

- Click "new" and create a new App.

- Give the application a name and then choose your region and Click "Create app".

- On the next page click on the Settings tab to adjust the settings.

- Click on the 'config vars' button.

- Supply a KEY of PORT and it's value of 8000. Then click on the "add" button.

- Add data from CREDS.json to link Google Sheet.

- Buildpacks now need to be added.

- These install future dependancies that we need outside of the requirements file.

- Select Python first and then node.js and click save.

$${\color{red}Make \space sure \space they \space are\space in\space this\space order\space !!!}$$

- Then go to the deploy section and choose your deployment method.

- To connect with github select github and confirm.

- Search for your repository select it and click connect.

- You can choose to either deploy using automatic deploys which means heroku will rebuild the app everytime you push your changes.

- For this option choose the branch to deploy and click enable automatic deploys.

- This can be changed at a later date to manual.

- Manual deployment deploys the current state of a branch.

- Click deploy branch.

- We can now click on the open App button above to view our application.

<a name="content"></a>

# $${\color{orange}Content}$$

### [ASCIIART.EU](https://www.asciiart.eu/)

> Used for the logo and luggage art.

### Code Institute

> Project created in line with course content and within project 3 scope and partially inspired by project 3 walkthrough.

### w3 schools

> Used to reference Python Structure

### Youtube

> Youtuber [b001](https://www.youtube.com/@b001) and his explanations helped me a lot with syntax problems and for loops.

### Stack Overflow

> Used to resolve issues with clearing terminal as well as Aiports/Countries indexing problem.

<a name="acknowledgments"></a>

# $${\color{orange}Acknowledgments}$$

### Derek McAuley

My Mentor that provided me with helpful tips, amazing feedback and continuous support during this course.

### Code Instutute Community

Great community that is always willing to help with any issues course participants are facing. I am very honored to be part of it.
