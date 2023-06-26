# Planner

## Live Preview

[YouTube Video](https://youtu.be/55Ie7KpHt9s)

## Overview

For my capstone project, I built a to-do list manager I called Planner. The web application allows the user to create and manage various lists, connect those lists to dates, and then edit and cross off items on lists. There are three main components to the application:

- Cards (the lists)
- Items (elements in a card)
- Calendar

Planner, as per project requirements, uses Django on the back-end with four models, JavaScript on the front end, and is  mobile-responsive.

## Components

### Cards
The web application collects lists submitted by the user in a format known to the app as a Card. Cards have numerous different functions such as duplicating, favoriting, and archiving. On the **Card View**, you can add Items to each card, then interact with those Items.

### Items

The elements assigned to a Card are known as Items. On the **Card View**, Items can be edited and marked as complete.

### Calendar

The Calendar displays the typical calendar details but also shows the Cards associated with specific dates. If a date has Cards associated with it, users can navigate directly to those cards by clicking on the drop-down.

The user can also navigate to the **Day View** to view the cards there. They can also opt to add a card to that date from that view.

Finally, while by default the Calendar shows the current month, it allows navigation to other months and uses the ```calendar``` module to generate the months, days, and years.

## The Project

### Index

The Index page displays all favorited cards. Users can then click on the card titles to further interact with the cards.

### Navigation Bar

The Navigation Bar is fully mobile-responsive. There's a link to the user (if logged in), login/register links, Calendar link, Add Card, and a drop-down list that features all active cards.

The View Card drop-down list features a search bar that filters the cards. 

### Adding Cards

Upon registration, the first thing a User will do is create a Card. The **Add Card** functionality takes in two text inputs, the Card Title and Card Description, as well as the ability to add it to a **Date**. 

If you are creating a card from scratch, the **Date** drop-down fields are disabled, and will become enabled upon the appropriate checkbox being clicked. The drop-down fields pulls in the current date and automatically selects the next day. The *Days* dropdown is also dynamic, adjusting itself to the proper date range when certain months are selected. For example, it will adjust to 31 days for December and 30 days if November is selected.

Furthermore, the submit button is disabled as long as the Card Title field is empty.

### Card View

The **Card View** is where most of the application takes place. Under the title and description, the card containss an input field where users can add Items to the Card, and the Submit button for that form is disabled as long as the Add Item field is empty.

The card also contains a settings option in the top right which offers more functionality.

#### Items

Upon hovering, Items offer two options - marking item as complete and editing the item. When users mark the item as complete, it turns the item to a strike-through. When users edit the item, they can edit in the page without having to go to a different page. This functionality uses JavaScript to submit the edit once complete.

#### Card Settings

Cards offer several different functions.

**Edit Card**

With this option, users can edit the Card Title and Card Description, as well as deleting dates that the Cards are associated with.

**Favorite/Unfavorite Card**

Favoriting a card allows the user to view that card on the Index page. This action uses JavaScript to change the setting options to "Unfavorite" once a user has favorited the card, and vice versa.

**Copy Card**

Copying a Card allows you to duplicate the card. You can also elect to copy or not copy the various elements of the Card. For example, you can choose to copy the items or not. And if the Card is associated with dates, you can choose which dates to copy as well as add a new date.

**Add Date**

The **Add Date** opens up a Modal which allows you to select a new date to add. As with the date functionality in the **Add Card** view, it pulls in tomorrow's date automatically, but users can change it if they want.

**Hide/Show Complete Items**

By default, cards show completed items, but users can select this option on a per-card basis in order to hide completed items from view.

**Archive/Restore Card**

Users can opt to archive cards. This will hide the cards from all views except for the profile page. You can technically still access an Archived Card by clicking on your username, but unless a card is restored, you cannot Favorite them or Add new Dates to them. You can Copy or Edit them, however. This setting uses JavaScript to change the Card status on the backend, and to flip the setting options to "Restore", and vice versa.

### All Cards Page

By clicking on your username, you can view all of your cards and access them, in case you need to restore them.

### Calendar View

The **Calendar View** utilizes the Python ```calendar``` module to help generate the calendar dates. Each day of the month submits a tuple that contains the day, month, year, as well as the list of Cards that are associated with it. By default, the **Calendar View** always portrays the current month, but navigating the arrow buttons on either side of the calendar allow users to click through and look at other months.

Then, the front end is a fully mobile-responsive page that, in a medium or larger view, looks like a typical calendar, with the current day highlighted. If a day has cards associated with it, it lists a drop-down that links to each card.

In a mobile view, it reverts from the traditional calendar view to a list of the dates. In this view, no drop-down appears, instead being replaced by text that says how many cards are associated with that date.

Each day has a hyperlink to its own page. A list of all the cards associated with that date appear. Furthermore, users can add a card from this view. This function uses the same exact ```views.py``` code as the Add Card view, except instead of having the date function disabled by default, it is automatically set to the date view.



## Distinction from other projects in Web 50

I believe this web application took many of the concepts and tools I learned in this course and not only enforced these learnings, but built upon them.

- Sufficiently Distinct

While we built a simple to do list in the course video, I believe this is distinct enough from that, as it allows you to have multiple to do lists and attach these lists to different dates

- More Complex

I believe that this project is more complex because of all of the different tools the user has at their disposal when it comes to the cards. Also, the coding itself has required learning more outside of this course in order to complete. Here are some examples:

- Search Filter using JavaScript

The Search Filter was not a way we utilized JavaScript at all in the course - while the code looks pretty simple, it took a bit of research to figure out how to make this work; I learned how the ```indexOf``` function worked and how to use the return value of ```indexOf``` to determine if the string existed.

- Utilizing the 'include' notation to factor out common elements in a page.

Some of the more complicated elements was repeated multiple times in the code. For example, the date functionality that automatically pulled in tomorrow's date was quite complicated, so in order to optimize the code, I found the ```{% include %}``` function which I do not believe we specifically utilized in previous projects. Thus, I was able to essentially plug and play, saving time.

- Clicking on the + button in **Day View** to take you to the **Add Card** view and **Add Card** from scratch use the same ```views.py``` function but have slightly different functionality.

Using keyword parameters, I was able to make the ```add_card``` function serve two different paths. I do not believe we touched on keyword parameters at all in the course, so this flexibility allowed me to get more use out of this particular function.

- ```calendar``` module

The calendar was a massive undertaking on both the back-end and front-end. For one, the ```calendar``` module was entirely new to me and there was a lot of trial and error to figure out exactly how to output the objects. Furthermore, the ```datetime``` module received extensive usage here.

I finally figured out a list of tuples, each entry on the list representing a day, was a solid way to distinguish each day and then have the front-end utilize the tuple to interpret and spit out the right code for the calendar.

On the front-end, I had to take the learning about mobile-responsiveness to a new personal level. The traditional table-like calendar was clearly not going to work on mobile, so I learned how to collapse it and display something completely different in the mobile view.

## Function by Function Description

```index```

This function represents the homepage, and returns the favorite cards plus their respective items.

```get_profile```

This function is used to grab all cards (so users can view their archived cards and make changes to them)

```add_card```

This function adds the cards the user submits. By default, it pulls in the current date in order to automatically fill in the date fields in the submission form with the next day's date, but also takes in parameters to customize the date field if the user chooses to add a card from a particular view.


```view_card```

This function grabs from three different models - ```Card```, ```Item```, and ```Date```. The latter two models are filtered based on the user and the card.

```edit_card```

This function enables the user to edit the title, description, and delete dates from the respective card. 

```copy_card```

This function allows the user to create a new card based on the settings of another card. The user can select which elements of the card to copy over - like the dates or items, and can even add a new item as well.

```verify_user```

This function confirms if the user has the permission to see the card.

```get_card_list```

This function returns a ```QuerySet``` of the cards created by the logged-in user.

```add_date```

This function adds a new date to the ```Date``` model that's associated with a card of the User's choosing.

```act_item```

This function returns the item's active status via a ```JsonResponse``` object.

```edit_item```

This function allows the user to edit the text of an item, and uses an ```HttpResponseRedirect``` to refresh the page to show the edit.

```favorite_card```

This function allows the user to favorite and unfavorite a card via the JavaScript ```fetch``` method. It returns a ```JsonResponse``` object.

```archive_card```

This function allows the user to archive and restore a card via the JavaScript ```fetch``` method. It returns a ```JsonResponse``` object. It also unfavorites the card if the card is archived.

```hide_completed``` and ```show_completed```

These two functions hide/show the items in a card. Like ```edit_item```, it uses ```HttpResponseRedirect``` to refresh the page after updating.

```get_item_status```

This function returns the item's active status via a ```JsonResponse``` object.

```get_user```

This function returns a ```User``` object of the logged-in user.

```get_default_date```

This function returns a ```dict``` of the elements needed to generate the default date for the date fields.

```get_months```

This function returns a ```tuple``` of months - both the month number and month name are included.

```get_calendar```

This function generates the calendar. For the days in the calendar, it returns a list of ```tuples```, one for each day in the selected month, that contains the year, month, day, day of week (as an ```int```), if it's a Saturday/Sunday (in order to create a new line), day of week (as a ```str```), # of cards associated with this date, and the ```Card``` objects themselves.

Furthermore, this function also returns the next month and previous month so users can navigate.

```get_date```

This function is for the date view, and allows the user to view all cards in a date.

```register```, ```login```, ```logout```

Pretty standard registration and login/logout functions.
