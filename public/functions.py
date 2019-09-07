from django.utils import timezone

# def email(subject,text):
#     # this is how we emailing






def salam(user):
    string = ''
    username = user.username
    dateTime = timezone.now()
    for i in range(len(username)):
        string = string+username[i]
        if i == 0:
            string = string+str(dateTime.year)
        if i == 1:
            string = string+str(dateTime.month)
        if i == 2:
            string = string+str(dateTime.day)
        if i == 3:
            string = string + str(dateTime.hour)

    return string