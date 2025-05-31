var unread_msg_count = 0;
$('#id-inbox-link').click(function(e){
    $('#id-inbox-conv-div').removeClass('d-none');
    unread_msg_count = 0;
    $('#id-unread-count').html('');
});

// var ws = new WebSocket('ws://127.0.0.1:8000/ws/nibedok-message/');
var ws = new WebSocket('ws://16.171.41.180:80/ws/nibedok-message/');

ws.onmessage = function(event){
    response=JSON.parse(event.data);
    console.log(response);
    console.log("Inbx "+response.status);
    if(response.status=='connected'){
        unread_msg_count = response.unread_msg_count;
        if($('#id-inbox-conv-div').hasClass('d-none')){
            if(unread_msg_count > 0){
                $('#id-unread-count').html(unread_msg_count);
            }
        }
        $('#id-inbox-conv-div').html(response.html);
        ws.send(JSON.stringify({'task':'add_group'}));
    }
    else if(response.status=='msg_received'){
        if($('#id-inbox'+response.sender_channel_group_name)){
            $('#id-inbox'+response.sender_channel_group_name).remove();
            if(unread_msg_count > 0){
                unread_msg_count-=1;
            }
        }
        if($('#id-inbox-conv-div').hasClass('d-none')){
            unread_msg_count+=1;
            $('#id-unread-count').html(unread_msg_count);
        }
        var new_msg = '<a class="text-dark text-decoration-none" href="'+response.sender_url+'"><div class="bg-secondary-subtle" id="id-inbox'+response.sender_channel_group_name+'"><span class="h5 text-capitalize">'+response.sender_first_name+' '+response.sender_last_name+' </span><span><small>'+response.delivered_at+'</small></span><p>'+response.text+'</p><hr></div></a>';
        $('#id-inbox-conv-div').prepend(new_msg);
    }
}