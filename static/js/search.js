function submitSearch(){
    alert("Search");
    $('#id-search-form').submit();
}
$('#id-search-input').click(function(e){
    $('#id-search-div').removeClass('d-none');
});
var search_input_len = 0;
$('#id-search-input').keyup(function(evnt){
    search_input_len = $(this).val().length;
    var keyw = $(this).val();
    // alert(search_input_len,keyw);
    if(evnt.keyCode == 8){
        // alert(search_input_len,keyw);
    }
    if(search_input_len >= 3){
        $.ajax({
            method:'GET',
            data:{'keywords':keyw},
            url:"{% url 'search-results-suggestions' %}",
            success:function(response){
                var response_arr = JSON.parse(response);
                console.log(response_arr.results.length);
                $('#id-search-div').html('');
                var res_link = '';
                for(let i=0; i<response_arr.results.length; i++){
                    res_link += '<p class="my-1"><a class="ms-2 fw-bold text-dark text-decoration-none" href="'+response_arr.results[i].url+'">'+response_arr.results[i].title+'</a></p><hr>'
                }
                $('#id-search-div').append(res_link);
                $('#id-search-div').append('<p class="text-center my-1"><a class="text-dark" href="javascript:void(0);" onclick="submitSearch()">See More...</a></p>');
            }
        });
    }
    else{
        $('#id-search-div').html('');
    }
});