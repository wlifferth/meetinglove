function copy(sender)
{
    // Select text
    sender.select();
    try
    {
        // Copy text
        document.execCommand('copy');
        sender.blur();
    }
    catch(err)
    {
        alert('Please press Ctrl/Cmd + C to copy');
    }	
}

var meetingKey = "{{ meetingKey }}";
var adminKey = "{{ adminKey }}";
var arbMeetingTime;
var returnValue;
// Turn the unordered list with id "meetingTimeList" into a bootstrap datetimepicker
$(document).ready(function () {
    $('#datetimepicker').datetimepicker({
        inline: true,
        sideBySide: true,
        stepping: 5
    });
});

// Fetch all the dates to instantiate the list
$.ajax({
    dataType: "json",
    type: 'POST',
    url: $SCRIPT_ROOT + "/getMeetingTimes",
    data: {
        meetingKey: meetingKey
    },
    success: function(result) {
        renderMeetingTimes(result.meetingTimes);
    }
});
function addMeetingTime() {
    var newMeetingTime = $('#datetimepicker').data('DateTimePicker').date().format('YYYY-MM-DD hh:mm:ss');
    $.ajax({
        dataType: "json",
        type: 'POST',
        url: $SCRIPT_ROOT + "/addMeetingTime",
        data: {
            meetingKey: meetingKey,
            adminKey: adminKey,
            meetingTime: newMeetingTime
        },
        success: function(result) {
            renderMeetingTimes(result.meetingTimes);
        }
    });
}
function renderMeetingTimes(meetingTimes) {
    $('#meetingTimeList').empty();
    meetingTimes.forEach(function(meetingTime, index, array){
        $('#meetingTimeList').append("<li class='timeListing' id='" + meetingTime[1] + "'>" + meetingTime[0] + "<i class='glyphicon glyphicon-remove deleteButton' onclick='deleteMeetingTime(\"" + meetingTime[1] + "\")' ></i></li>")
    });
}
function deleteMeetingTime(meetingTimeKey) {
    $('#' + meetingTimeKey).remove();
    $.ajax({
        dataType: "json",
        type: 'POST',
        url: $SCRIPT_ROOT + "/deleteMeetingTime",
        data: {
            meetingKey: meetingKey,
            adminKey: adminKey,
            meetingTimeKey: meetingTimeKey
        },
        success: function(result) {
            renderMeetingTimes(result.meetingTimes);
        }
    });
}
