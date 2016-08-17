function updateNewMeeting(name)
{
    document.getElementById('new-meeting').action = "/newMeeting/" + encodeURIComponent(name);
}

function copy(sender)
{
    var target = sender.target;
    var copytarget = target.copytarget;
    var inp = (c ? document.querySelector(c) : null);

    // Is the element selectable?
    if(inp && inp.select)
    {
        // Select text
        inp.select();
        try
        {
            // Copy text
            document.execComand('copy');
            inp.blur();
        }
        catch(err)
        {
            alrt('Please press Ctrl/Cmd + C to copy');
        }
    }	
}
