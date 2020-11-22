from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("addcard", views.add_card, name="add_card"),
    path("card/<int:id>", views.view_card, name="view_card"),
    path("card/<int:id>/edit", views.edit_card, name="edit_card"),
    path("card/<int:id>/copy", views.copy_card, name="copy_card"),
    path("calendar/", views.get_calendar, name="calendar"),
    path("calendar/<int:selected_year>/<int:selected_month>", views.get_calendar, name="calendar_month"),
    path("date/<int:year>/<int:month>/<int:day>", views.get_date, name="date"),
    path("card/<int:id>/add-date", views.add_date, name="add_date"),
    path("card/<int:id>/hidecompleted", views.hide_completed, name="hide_completed"),
    path("card/<int:id>/showcompleted", views.show_completed, name="show_completed"),
    path("addcard/<int:current_year>/<int:current_month>/<int:next_day>/<int:check_date>", views.add_card, name="add_card_to_date"),
    path("profile", views.get_profile, name="profile"),

    # API Paths

    path("card/<int:id>/favorite", views.favorite_card, name="favorite"),
    path("item/<int:id>", views.act_item, name="act_item"),
    path("item/<int:id>/edit", views.edit_item, name="edit_item"),
    path("item/<int:id>/status", views.get_item_status, name="get_item_status"),
    path("card/<int:id>/archive", views.archive_card, name="archive")
    ]