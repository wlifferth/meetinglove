function updateNewMeeting(name)
{
    document.getElementById('new-meeting').action = "/newMeeting/" + encodeURIComponent(name);
}

