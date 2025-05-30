// notification and inbox loader starts
$('#id-notification-link').click(function(e){
    $('#id-notification-div').removeClass('d-none');
});
// var notif_inbox_ws = new WebSocket('ws://127.0.0.1:8000/ws/nibedok-notification-inbox/');
var notif_inbox_ws = new WebSocket('ws://16.171.41.180//ws/nibedok-notification-inbox/');

function updateNotifRead(){
    // alert("Update Notif");
    notif_inbox_ws.send(JSON.stringify({'task':'update_notif_read'}));
}
var curr_notif_count = 0;

notif_inbox_ws.onmessage=function(ev){
    console.log(JSON.parse(ev.data));
    var data = JSON.parse(ev.data)
    var status = data.status
    console.log(status);
    if(status == 'connected'){
        notif_inbox_ws.send(JSON.stringify({'task':'send_notification'}));
    }
    else if(status=='sent_notification'){
        curr_notif_count = data.notif_count;
        if(curr_notif_count > 0){
            $('#id-notif-span').html(curr_notif_count);
        }
        var msgs = '';
        for(i=0;i<data.msg_details.length;i++){
            msgs += '<p id="notif'+data.msg_details[i].id+'" class="bg-dark-subtle ps-2"><a class="text-dark text-decoration-none" href="'+data.msg_details[i].url+'">'+data.msg_details[i].msg+'</a></p><hr>';
        }
        $('#id-notif-msg-div').append(msgs);
        $('#id-notification-link').on('click',function(evn){
            $('.bg-dark-subtle').removeClass('bg-dark-subtle');
            if(curr_notif_count > 0){
                updateNotifRead();
            }
            $('#id-notif-span').html('');
            curr_notif_count = 0;
        });
        notif_inbox_ws.send(JSON.stringify({'task':'add_group'}));
    }
    else if(status=='updated_notif'){
        console.log(data.msg)
        if($('#notif'+data.id)){
            $('#notif'+data.id).remove();
            if(curr_notif_count > 0){
                curr_notif_count -= 1;
            }
        }
        var new_notif = '<p id="notif'+data.id+'" class="bg-dark-subtle ps-2"><a class="text-dark text-decoration-none" href="'+data.url+'">'+data.msg+'</a></p><hr>';
        $('#id-notif-msg-div').prepend(new_notif);
        if(!$("#id-notification-div").hasClass('d-none')){
            updateNotifRead();
        }
        else{
            $('#id-notif-span').html(curr_notif_count+1);
        }
    }
}

// notification and inbox loader ends